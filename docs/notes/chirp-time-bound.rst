Chirp-time bounds
#################

:date: 2019-10-08

The duration of a Compact Binary Coalescense signal is roughly given by the
chirp-time bound, a conservative estimate of the time spent in band (inspiral
and merge ringdown). Here is a figure of the chirp-time bound as a function of
the chirp mass and mass ratio for a non-spinning system.

.. image:: /images/chirp_time_bound.png

The script to generate the figure, which makes use of bilby for simple
conversions, is cwgiven here:

.. code-block:: python

   import matplotlib.pyplot as plt
   import numpy as np
   from bilby.gw import conversion
   import lal
   import lalsimulation as lalsim


   def chirp_mass_and_mass_ratio_to_component_masses(chirp_mass, mass_ratio):
       mtotal = conversion.chirp_mass_and_mass_ratio_to_total_mass(
           chirp_mass, mass_ratio)
       (mass_1, mass_2) = conversion.total_mass_and_mass_ratio_to_component_masses(
           mass_ratio, mtotal)

       return mass_1, mass_2


   flow = 20
   a_1 = 0.
   a_2 = 0.
   tilt_1 = 0.
   tilt_2 = 0.

   N = 100
   chirp_mass = np.linspace(10, 100, 2 * N)
   mass_ratio = np.linspace(0.125, 1, N)

   chirp_times = []
   for mc in chirp_mass:
       for q in mass_ratio:
           mass_1, mass_2 = chirp_mass_and_mass_ratio_to_component_masses(
               mc, q)
           chirp_times.append(lalsim.SimInspiralChirpTimeBound(
               flow, mass_1 * lal.MSUN_SI, mass_2 * lal.MSUN_SI,
               a_1 * np.cos(tilt_1), a_2 * np.cos(tilt_2)))


   X, Y = np.meshgrid(chirp_mass, mass_ratio, indexing='ij')
   Z = np.array(chirp_times).reshape((2 * N, N))
   fig, ax = plt.subplots()
   p = ax.pcolormesh(X, Y, Z)
   ax.colorbar(label="Chirp-time bound")
   CS = ax.contour(X, Y, Z, levels=[0.25, 0.5, 1.0, 2.0, 4.0], colors='w')
   ax.clabel(CS, CS.levels, inline=True, fmt="%r")
   ax.set_xlabel(r"$\mathcal{M} [M_{\odot}]$")
   ax.set_ylabel(r"$q$")
   fig.savefig("chirp_time_bound")
