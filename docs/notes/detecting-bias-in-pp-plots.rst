Detecting a bias using a pp plot
################################

:date: 2019-05-01

Parameter-parameter plots (pp-plots), see `Cook, Gelman, and Rubin (2012)
<https://amstat.tandfonline.com/doi/abs/10.1198/106186006X136976>`_ provide a
method to test data simulation and data analysis software for biases.

A question I couldn't find an easy answer to (or perhaps didn't look hard enough)
is "how many events do I need to include to detect a bias of x%?"

To test this quantitatively, here is a script which generates a number of bilby
posteriors for a simple Gaussian problem


.. code-block:: python

   #!/usr/bin/env python
   """ Generates posteriors for a simple Gaussian problem"""
   from __future__ import division
   import bilby
   import numpy as np


   class SimpleGaussianLikelihood(bilby.Likelihood):
       def __init__(self, data):
           """
           A very simple Gaussian likelihood

           Parameters
           ----------
           data: array_like
               The data to analyse
           """
           self.data = data
           self.N = len(data)
           self.parameters = {'mu': None, 'sigma': None}

       def log_likelihood(self):
           bias_factor = 2e-4
           mu = self.parameters['mu'] + bias_factor
           sigma = self.parameters['sigma']
           res = self.data - mu
           return -0.5 * (np.sum((res / sigma)**2) + self.N * np.log(2 * np.pi * sigma**2))


   outdir = 'outdir'
   mu_min = 4
   mu_max = 5
   sigma_min = 0.01
   sigma_max = 0.02
   priors = dict(mu=bilby.core.prior.Uniform(mu_min, mu_max, 'mu'),
                 sigma=bilby.core.prior.Uniform(sigma_min, sigma_max, 'sigma'))

   run_idx = np.random.randint(1000)
   for i in range(500):
       label = f'gaussian_{run_idx}_{i}'
       mu = np.random.uniform(mu_min, mu_max)
       sigma = np.random.uniform(sigma_min, sigma_max)
       injection_parameters = dict(mu=mu, sigma=sigma)
       data = np.random.normal(mu, sigma, 100)
       likelihood = SimpleGaussianLikelihood(data)
       result = bilby.run_sampler(
           likelihood=likelihood, priors=priors, sampler='pymultinest', npoints=500,
           injection_parameters=injection_parameters, outdir=outdir, label=label,
           check_point=False)
       #result.plot_corner()


On running, this iteratively draws a population-level value for the mean and
standard deviation, draws a set of corresponding data, then performs parameter
estimation. Repeating a number of times (here set to 500), the results are
logged in the output directory.

Most notably, in the likelihood, I have intentionally biased the analysis
software. Adding a constant value of 0.0002 to the mean. In terms of P.E., this
amounts to a bias in the inferred mu. The size of the bias can be quantified by
comparing with the typical width of the posterior, which in this case is about
0.0015, so I will refer to this as a roughly 13.3% bias.

Taking 500 events, and generating a pp plot (script to do this included at the
end of this post), we get this PP plot

.. image:: /images/pp_plots/N500_pp.png

The bias is evident: the mu parameter clearly deviates from the 90% C.I. shown
in grey. But, could we have been so confident with say 100 events? Or, for this
13.3% bias, what number of events would still pass the pp test?

To investigate this, in the figure below I'm plotting the join pvalue (computed
by calculating a pvalue for each parameter then combining them using the Fisher
method) as a function of the number of samples. The samples are ordered so
expect correlations here. But, the key is that the the p-value hovers in the
0.01 - 1 range until more than 200 events before plunging. Above 300 events,
it clearly identifies that there is a bias, but with just 100 events one would
not see a bias.

.. image:: /images/pp_plots/pvalue_nevents.png


As a rough fule of thumb, it seems to me that to confidently detect a bias at
the X% level, one needs at least a few times 10X, to be safe, perhaps 100X is
more appropriate.

.. code-block:: python

   # make_pp_plots.py
   """ Code used to generat pp plots """
   import glob
   import os

   import numpy as np
   import matplotlib.pyplot as plt
   from bilby.core.result import read_in_result, make_pp_plot
   import tqdm

   directory = "outdir"

   results_files = []
   glob_string = os.path.join(directory, "*result*json")
   results_files = glob.glob(glob_string)

   results = []
   for f in tqdm.tqdm(results_files):
       results.append(read_in_result(f))

   results_u = []
   mu_stds = []
   for r in results:
       if r._posterior is not None:
           results_u.append(r)
           mu_stds.append(np.std(r.posterior['mu']))
       else:
           print("Result {} incomplete".format(r.label))
   if len(results_u) < len(results):
       print("Results incomplete, truncating to {}".format(len(results_u)))
       results = results_u
   else:
       print("Results complete")

   print("Mean standard deviation of mu = {}".format(np.mean(mu_stds)))

   # Create pp plot for all results
   basename = f"N{len(results)}"
   fig, pvals = make_pp_plot(results, filename=f"{basename}_pp.png")

   # Create p-value as a function of n
   combined_pvalues = []
   nevents = range(0, len(results), 5)
   for n in tqdm.tqdm(nevents):
       _, pvals = make_pp_plot(results[:n], save=False)
       combined_pvalues.append(pvals.combined_pvalue)
   fig, ax = plt.subplots()
   ax.loglog(nevents, combined_pvalues, '-x')
   ax.set_xlabel("Number of events")
   ax.set_ylabel("p-value")
   fig.savefig("pvalue_nevents")



