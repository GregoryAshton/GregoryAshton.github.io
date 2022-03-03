```python
!pip install bilby lalsuite
```

    Requirement already satisfied: bilby in /home/greg/bilby (1.1.5)
    Requirement already satisfied: lalsuite in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (7.3)
    Requirement already satisfied: dynesty<1.1 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (1.0.1)
    Requirement already satisfied: emcee in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (3.1.1)
    Requirement already satisfied: corner in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (2.2.1)
    Requirement already satisfied: numpy in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (1.22.1)
    Requirement already satisfied: matplotlib>=2.1 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (3.5.1)
    Requirement already satisfied: scipy>=1.5 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (1.7.3)
    Requirement already satisfied: pandas in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (1.4.0)
    Requirement already satisfied: dill in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (0.3.4)
    Requirement already satisfied: tqdm in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (4.62.3)
    Requirement already satisfied: h5py in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (3.6.0)
    Requirement already satisfied: tables in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (3.7.0)
    Requirement already satisfied: astropy in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (5.0.1)
    Requirement already satisfied: attrs in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from bilby) (21.4.0)
    Requirement already satisfied: ligo-segments in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from lalsuite) (1.4.0)
    Requirement already satisfied: python-dateutil in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from lalsuite) (2.8.2)
    Requirement already satisfied: lscsoft-glue in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from lalsuite) (3.0.1)
    Requirement already satisfied: six in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from dynesty<1.1->bilby) (1.16.0)
    Requirement already satisfied: fonttools>=4.22.0 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from matplotlib>=2.1->bilby) (4.29.1)
    Requirement already satisfied: cycler>=0.10 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from matplotlib>=2.1->bilby) (0.11.0)
    Requirement already satisfied: pyparsing>=2.2.1 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from matplotlib>=2.1->bilby) (3.0.7)
    Requirement already satisfied: pillow>=6.2.0 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from matplotlib>=2.1->bilby) (9.0.0)
    Requirement already satisfied: packaging>=20.0 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from matplotlib>=2.1->bilby) (21.3)
    Requirement already satisfied: kiwisolver>=1.0.1 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from matplotlib>=2.1->bilby) (1.3.2)
    Requirement already satisfied: pyerfa>=2.0 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from astropy->bilby) (2.0.0.1)
    Requirement already satisfied: PyYAML>=3.13 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from astropy->bilby) (5.4.1)
    Requirement already satisfied: pyRXP in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from lscsoft-glue->lalsuite) (3.0.1)
    Requirement already satisfied: pyOpenSSL in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from lscsoft-glue->lalsuite) (21.0.0)
    Requirement already satisfied: pytz>=2020.1 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from pandas->bilby) (2021.3)
    Requirement already satisfied: cryptography>=3.3 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from pyOpenSSL->lscsoft-glue->lalsuite) (3.3.1)
    Requirement already satisfied: cffi>=1.12 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from cryptography>=3.3->pyOpenSSL->lscsoft-glue->lalsuite) (1.15.0)
    Requirement already satisfied: pycparser in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from cffi>=1.12->cryptography>=3.3->pyOpenSSL->lscsoft-glue->lalsuite) (2.21)
    Requirement already satisfied: numexpr>=2.6.2 in /home/greg/anaconda3/envs/testing/lib/python3.9/site-packages (from tables->bilby) (2.8.1)



```python
import lalsimulation as lalsim
import lal
import bilby
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

solar_mass = bilby.core.utils.constants.solar_mass
parsec = bilby.core.utils.constants.parsec
```

# Generating time domain waveforms and projecting them onto the detectors

In this notebook, I'll demonstrate how to use `lalsimulation` to generate a time-domain waveform and how to then use `bilby` to calculate the response of an interferometer.

## Setting a few things up

To get started, let's define some properties of the data we want to simulate. This is the sampling frequency, duration and the amount of time before and after the trigger time (roughly speaking, the peak of the 2,2 mode).



```python
sampling_frequency = 4096
deltaT = 1 / sampling_frequency
duration = 4
post_trigger_duration = 0.5
pre_trigger_duration = duration - post_trigger_duration
```

## Generate a waveform

Now, we'll use `lalsim.SimInspiralChooseTDWaveform` to generate the plus and cross polarization


```python
# Define the parameters in SI units
m1 = 30 * solar_mass
m2 = 30 * solar_mass
S1x, S1y, S1z = 0, 0, 0
S2x, S2y, S2z = 0, 0, 0
distance = 50e6 * parsec
inclination = 0
phiRef = 0
longAscNodes = 0
eccentricity = 0
meanPerAno = 0
LALParams = lal.CreateDict()

# Get the approximant number from the name
waveform_approximant = "IMRPhenomT"
approximant = lalsim.GetApproximantFromString(waveform_approximant)

# Estimate a minimum frequency required to ensure the waveform covers the data
# Note the 0.95 is a fudge factor as SimInspiralChirpStartFrequencyBound includes
# only the leading order Newtonian coefficient.
f_min = 0.95 * lalsim.SimInspiralChirpStartFrequencyBound(pre_trigger_duration, m1, m2)
if lalsim.SimInspiralGetSpinFreqFromApproximant(approximant) == lalsim.SIM_INSPIRAL_SPINS_FLOW:
    f_ref = f_min
else:
    f_ref = 20

h_plus_timeseries, h_cross_timeseries = lalsim.SimInspiralChooseTDWaveform(
    m1, m2, S1x, S1y, S1z, S2x, S2y, S2z, distance, inclination, phiRef, 
    longAscNodes, eccentricity, meanPerAno, deltaT, f_min, f_ref, LALParams,
    approximant
)
```

## Extract the data


```python
h_plus = h_plus_timeseries.data.data
h_cross = h_cross_timeseries.data.data
h_plus_time = np.arange(len(h_plus)) * h_plus_timeseries.deltaT + float(h_plus_timeseries.epoch)
h_cross_time = np.arange(len(h_cross)) * h_cross_timeseries.deltaT + float(h_cross_timeseries.epoch)
```

## Project onto the Hanford interferometer


```python
ra = 1.2
dec = -3.1
geocent_time = 1126259462.1
psi = 0.5
H1 = bilby.gw.detector.get_empty_interferometer("H1")

plus_polarization_tensor = bilby.gw.utils.get_polarization_tensor(ra, dec, geocent_time, psi, "plus")
f_plus = np.einsum('ij,ij->', H1.detector_tensor, plus_polarization_tensor)

cross_polarization_tensor = bilby.gw.utils.get_polarization_tensor(ra, dec, geocent_time, psi, "cross")
f_cross = np.einsum('ij,ij->', H1.detector_tensor, cross_polarization_tensor)

strain = f_plus * h_plus + f_cross * h_cross
strain_time = h_plus_time
```

## Plot the data


```python
plt.plot(strain_time, strain)
plt.ylabel("Strain")
plt.xlabel(f"GPS time [s]")
plt.show()
```


    
![png](waveform_projection_files/waveform_projection_11_0.png)
    


From the plot above (or by inspecting `strain` and `strain_time`), we see that `SimInspiralChooseTDWaveform` outputs the strain on a grid of times with sampling frequency `1/deltaT`, but that the duration is determined by `f_min` and that peak of the 2,2 mode occurs at `0`.

We can translate this to the time measured by a detector by simply adding `geocent_time`, e.g.


```python
strain_detector_time = strain_time + geocent_time
```

But, we'll want to compare our predicted strain with a timeseries of detector data which will be sampled on a different grid (even if the sampling frequency is identical, we would not expect a sampled timeseries to align with the peak of the 2,2 mode!). To convert, we can interpolate.

## Interpolate onto a sampled data grid



```python
n = sampling_frequency * duration
data_start_time = int(geocent_time) - pre_trigger_duration
data_detector_time = np.arange(n) / sampling_frequency + data_start_time 
h_interp = interp1d(strain_detector_time, strain, fill_value=0, bounds_error=False)(data_detector_time)
```


```python
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(15, 6))
ax1.plot(data_detector_time - geocent_time, h_interp)
ax1.plot(strain_detector_time - geocent_time, strain, "--")
ax1.set_ylabel("Strain")
ax1.set_xlabel(f"GPS time - {geocent_time} [s]")
ax2.plot(data_detector_time - geocent_time, h_interp, label="Interpolated")
ax2.plot(strain_detector_time - geocent_time, strain, "--", label="Strain")
ax2.set_ylabel("Strain")
ax2.set_xlabel(f"GPS time - {geocent_time} [s]")
ax2.set_xlim(-0.1, 0.1)
ax2.legend()
plt.show()
```


    
![png](waveform_projection_files/waveform_projection_17_0.png)
    


## Putting it all together into a single function


```python
def get_gw_waveform(time, parameters, waveform_approximant, reference_frequency, bilby_detector, fudge=0.95):

    # Extract information about the time series
    deltaT = time[1] - time[0]
    duration = time[-1] - time[0]
    nearest_trigger_idx = np.argmin(np.abs(time - parameters["geocent_time"]))
    pre_trigger_duration = time[nearest_trigger_idx] - time[0]
    
    # Get the approximant number from the name
    approximant = lalsim.GetApproximantFromString(waveform_approximant)

    # Estimate a minimum frequency required to ensure the waveform covers the data
    # Note the 0.95 is a fudge factor as SimInspiralChirpStartFrequencyBound includes
    # only the leading order Newtonian coefficient.
    f_min = 0.95 * lalsim.SimInspiralChirpStartFrequencyBound(pre_trigger_duration, m1, m2)
    
    # Check if the reference frequency is used, if not use f_min
    if lalsim.SimInspiralGetSpinFreqFromApproximant(approximant) == lalsim.SIM_INSPIRAL_SPINS_FLOW:
        f_ref = f_min
    elif reference_frequency == "fmin":
        f_ref = f_min
    else:
        f_ref = reference_frequency
        
    params, _ = bilby.gw.conversion.convert_to_lal_binary_black_hole_parameters(parameters)

    iota, spin_1x, spin_1y, spin_1z, spin_2x, spin_2y, spin_2z = bilby.gw.conversion.bilby_to_lalsimulation_spins(
        theta_jn=params["theta_jn"], phi_jl=params["phi_jl"], tilt_1=params["tilt_1"], tilt_2=params["tilt_2"],
        phi_12=params["phi_12"], a_1=params["a_1"], a_2=params["a_2"], mass_1=params["mass_1"], mass_2=params["mass_2"],
        reference_frequency=f_ref, phase=params["phase"])

    if "zenith" in params and "azimuth" in params:
        params["ra"], params["dec"] = bilby.gw.utils.zenith_azimuth_to_ra_dec(
            params['zenith'], params['azimuth'], params["geocent_time"], inputs.reference_frame)

    longAscNodes = 0
    eccentricity = 0
    meanPerAno = 0
    LALParams = lal.CreateDict()

    h_plus_timeseries, h_cross_timeseries = lalsim.SimInspiralChooseTDWaveform(
        m1, m2, S1x, S1y, S1z, S2x, S2y, S2z, distance, inclination, phiRef, 
        longAscNodes, eccentricity, meanPerAno, deltaT, f_min, f_ref, LALParams,
        approximant
    )

    plus_polarization_tensor = bilby.gw.utils.get_polarization_tensor(ra, dec, geocent_time, psi, "plus")
    f_plus = np.einsum('ij,ij->', H1.detector_tensor, plus_polarization_tensor)

    cross_polarization_tensor = bilby.gw.utils.get_polarization_tensor(ra, dec, geocent_time, psi, "cross")
    f_cross = np.einsum('ij,ij->', H1.detector_tensor, cross_polarization_tensor)


    h_plus = h_plus_timeseries.data.data
    h_cross = h_cross_timeseries.data.data
    h_plus_time = np.arange(len(h_plus)) * h_plus_timeseries.deltaT + float(h_plus_timeseries.epoch)

    h = f_plus * h_plus + f_cross * h_cross
    t = h_plus_time + geocent_time

    h_interp = interp1d(t, h, fill_value=0, bounds_error=False)(time)
    if h_interp[0] == 0:
        raise ValueError("Generated waveform was too short")
    return h_interp


```


```python
parameters = dict(
    mass_1=36., mass_2=29., a_1=0.4, a_2=0.3, tilt_1=0.5, tilt_2=1.0,
    phi_12=1.7, phi_jl=0.3, luminosity_distance=2000., theta_jn=0.4, psi=2.659,
    phase=2.8, geocent_time=1126259642.413, ra=1.375, dec=-1.2108
)

for waveform in ["IMRPhenomT", "SEOBNRv4T", "TEOBResumS"]:
    w = get_gw_waveform(data_detector_time, parameters, waveform, "fmin", H1)
    plt.plot(data_detector_time - geocent_time, w, label=waveform)
plt.xlim(-0.1, 0.05)
plt.ylabel("Strain")
plt.xlabel(f"GPS time - {geocent_time} [s]")
plt.legend()
plt.show()
```


    
![png](waveform_projection_files/waveform_projection_20_0.png)
    


## Time the generation


```python
prior = bilby.gw.prior.BBHPriorDict()
prior["geocent_time"] = bilby.core.prior.Uniform(geocent_time - 0.1, geocent_time + 0.1)
```

    08:59 bilby INFO    : No prior given, using default BBH priors in /home/greg/bilby/bilby/gw/prior_files/precessing_spins_bbh.prior.



```python
%%timeit
_ = get_gw_waveform(data_detector_time, prior.sample(), "SEOBNRv4T", 20, H1, fudge=0.95)

```

    415 ms ± 7.58 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)



```python
%%timeit
_ = get_gw_waveform(data_detector_time, prior.sample(), "IMRPhenomT", 20, H1, fudge=0.95)
```

    5.82 ms ± 96.9 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)



```python
%%timeit
_ = get_gw_waveform(data_detector_time, prior.sample(), "IMRPhenomD", 20, H1, fudge=0.95)
```

    6.57 ms ± 182 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

