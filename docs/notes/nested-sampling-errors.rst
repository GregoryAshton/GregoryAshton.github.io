Nested sampling errors
######################

:date: 2018-07-31

Nested samplers estimate the evidence :math:`P(d | I)` along with providing
sampler with which to estimate the posterior. Typically, they provide the
log-evidence along with an estimate of the error. We test out these errors for
a few easy-to-use samplers by comparing to a case that can be solved
analytically.

Analytic problem
----------------

We usually think of a likelihood of some data :math:`x` given some model
parameters. For example, a normal likelihood is denoted 

.. math::

    P(x; \mu, \sigma) = \frac{1}{\sqrt{2\pi\sigma^2}}e^{\frac{(x-\mu)^2}{2\sigma^2}}


Consider then the case when :math:`x=0`, the mean is unknown, but variance is
known, :math:`\sigma=1`, i.e. the likelihood is given by :math:`P(x=0; \mu,
\sigma=1)`.  If the prior is specified as :math:`\mu` is uniform between a
minimum and maximum value then the evidence is given by

.. math::

    Z = \frac{1}{\mu_{max} - \mu_{min}}
    \int_{\mu_{min}}^{\mu_{max}} \frac{1}{\sqrt{2\pi}}e^{\frac{\mu^{2}}{2}} d\mu

The evidence :math:`Z`, here is :math:`P(x=0)`.

This evidence is easy to calculate analytically, provided the prior range is
sufficiently large that the likelihood is negligibally small at the edges. If
so, then the integral is unity and hence

.. math::

    Z = \frac{1}{\mu_{max} - \mu_{min}}

Testing samplers
----------------

We can test this out by plugging the likelihood and prior into a few nested
samplers. We'll do this using `tupak <https://monash.docs.ligo.org/tupak/>`_.
Here is a the core of the code which defines the likelihood and priors. We
then define a function to compute :math:`f = log(\mu_{max}-\mu_{min}) + log(Z)`.
If the sampler was perfectly accurate, then :math:`f=0`.

.. code-block:: python

    class GaussianLikelihood(tupak.Likelihood):
        """ Simple likelihood passed into tupak """
        def __init__(self):
            self.parameters = {'mu': None, 'sigma': None}

        def log_likelihood(self):
            mu = self.parameters['mu']
            sigma = self.parameters['sigma']
            return -0.5 * ((mu / sigma)**2 +
                           np.log(2 * np.pi * sigma**2))


    likelihood = GaussianLikelihood()
    priors = dict(mu=tupak.core.prior.Uniform(-5, 5, 'mu'),
                  sigma=1)

    prior_factor = np.log(priors['mu'].maximum - priors['mu'].minimum)


    def single_run(npoints, sampler):
        result = tupak.run_sampler(
            likelihood=likelihood, priors=priors, sampler=sampler, npoints=npoints,
            outdir='outdir', label='test{}'.format(idx), verbose=False, clean=True)
        test_val = prior_factor + result.log_evidence
        return [test_val, result.log_evidence_err]


We now run this 2000 times for different samplers and different numbers of live
points. Each time, we record :math:`log(Z)` and the estimated errors from the
sampler. At the bottom of this note you'll find the full script. So far, we've
looked at `dynesty <https://dynesty.readthedocs.io/en/latest/>`_, `nestle
<https://github.com/kbarbary/nestle>`_ and `pymultinest
<https://github.com/JohannesBuchner/PyMultiNest>`_. Here is a table comparing
the results. The npoints here is the number of live points (different names
are used for each package) while mean_err is the mean of quoted error on the
log evidence provided by the sampler.

.. table::

    +-----------+-------+---------+-------+--------+
    |  sampler  |npoints| mean_f  | std_f |mean_err|
    +===========+=======+=========+=======+========+
    |pymultinest|    100| 0.001666|0.09905| 0.09370|
    +-----------+-------+---------+-------+--------+
    |pymultinest|    250| 0.002221|0.06184| 0.05936|
    +-----------+-------+---------+-------+--------+
    |pymultinest|    500| 0.001909|0.04405| 0.04201|
    +-----------+-------+---------+-------+--------+
    |dynesty    |    100|-0.004549|0.09638| 0.08438|
    +-----------+-------+---------+-------+--------+
    |dynesty    |    250| 0.000784|0.06181| 0.05164|
    +-----------+-------+---------+-------+--------+
    |dynesty    |    500|-0.001006|0.04316| 0.03566|
    +-----------+-------+---------+-------+--------+
    |nestle     |    100| 0.003573|0.10052| 0.09370|
    +-----------+-------+---------+-------+--------+
    |nestle     |    250| 0.001101|0.06394| 0.05941|
    +-----------+-------+---------+-------+--------+
    |nestle     |    500| 0.002233|0.04456| 0.04199|
    +-----------+-------+---------+-------+--------+


Note that in each case we are use the default arguments form tupak as of
v0.2.1. For pymultinest and nestle, this is pretty much the libarary defaults,
for dynesty, it is tuned and uses the rwalk method of sampling new points.

A few quick takeaways. (i) For the same number of live points they all
perform comparably (i.e. have approximately similar errors). (ii) The quoted
errors are consistent with the measured standard deviation.

To give a sense for what the distribution of :math:`f` looks like, here are
Gaussian KDE for the dynesty sampler results

.. image:: /images/dynesty_test.png


Scripts
-------
Here is the full script to generate the data


.. code-block:: python

    """
    Script to generate monte carlo results testing the accurarcy of different
    nested samplers
    """
    import numpy as np
    import tupak
    import os
    import sys

    # Sets up a label to avoid file collisions when running in paralell
    if len(sys.argv) > 1:
        idx = sys.argv[1]
    else:
        idx = 0


    class GaussianLikelihood(tupak.Likelihood):
        """ Simple likelihood passed into tupak """
        def __init__(self):
            self.parameters = {'mu': None, 'sigma': None}

        def log_likelihood(self):
            mu = self.parameters['mu']
            sigma = self.parameters['sigma']
            return -0.5 * ((mu / sigma)**2 +
                           np.log(2 * np.pi * sigma**2))


    likelihood = GaussianLikelihood()
    priors = dict(mu=tupak.core.prior.Uniform(-5, 5, 'mu'),
                  sigma=1)

    prior_factor = np.log(priors['mu'].maximum - priors['mu'].minimum)


    def single_run(npoints, sampler):
        result = tupak.run_sampler(
            likelihood=likelihood, priors=priors, sampler=sampler, npoints=npoints,
            outdir='outdir', label='test{}'.format(idx), verbose=False, clean=True)
        test_val = prior_factor + result.log_evidence
        return [test_val, result.log_evidence_err]


    repeats = 1000

    for sampler in ['nestle', 'dynesty', 'pymultinest']:
        for npoints in [250]:
            filename = 'results/{}_{}.txt'.format(sampler, npoints)
            results = []
            for i in range(repeats):
                results.append(single_run(npoints, sampler))
                os.system('rm outdir/pymultinest_test{}* -r'.format(idx))
            with open(filename, 'a+') as f:
                for r in results:
                    f.write('{} {}\n'.format(*r))


Here is the script used to generate the table and figures

.. code-block:: python

    import matplotlib.pyplot as plt
    import numpy as np
    import glob
    from scipy.stats import gaussian_kde
    import pandas as pd
    import pytablewriter

    df = pd.DataFrame(columns=['sampler', 'npoints', 'mean_f', 'std_f', 'mean_err'])


    def make_output_plot(sampler, df):
        fig, ax = plt.subplots()
        xsmooth = np.linspace(-0.3, 0.3, 1000)
        files = np.sort(glob.glob('results/{}*txt'.format(sampler)))
        for file in files:
            values, errs = np.loadtxt(file).T
            print("Found {} results for {}".format(len(values), file))
            kde = gaussian_kde(values)
            label = file.rstrip('.txt').replace('_', ' ').lstrip('results/')
            npoints = label.split(' ')[1]
            ax.plot(xsmooth, kde(xsmooth), label=npoints)

            df = df.append(dict(
                sampler=sampler, npoints=npoints,
                mean_f=np.mean(values),
                std_f=np.std(values),
                mean_err=np.mean(errs)), ignore_index=True)

        ax.set_xlabel('$f = \mathrm{ln}(Z) + \mathrm{ln}(\mu_{max} - \mu_{min})$')
        ax.set_ylabel('Histogram density')
        ax.set_title(sampler)
        ax.legend(loc=1, fontsize=12, labelspacing=1, title='N points')
        ax.grid()
        ax.set_xlim(-0.3, 0.3)
        ax.set_ylim(0, 10)
        fig.savefig('{}_test'.format(sampler))
        return df


    samplers = ['pymultinest', 'dynesty', 'nestle']
    for sampler in samplers:
        df = make_output_plot(sampler, df)

    writer = pytablewriter.RstGridTableWriter()
    writer.from_dataframe(df)
    writer.write_table()
