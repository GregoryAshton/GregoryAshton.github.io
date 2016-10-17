---
layout: default
title: Projects
---
# PhD. research: Pulsar timing noise, models and implications

I am currently a PhD candidate enrolled at the mathematics department of the
[University of
Southamtpon](http://www.southampton.ac.uk/maths/postgraduate/research_students/ga7go8.page).
Under the supervision of D.I. Jones (UoS) and Reinhard Prix (Albert Einstein
Institute, Hannover), I am researching the phenomena of timing noise observed
in [pulsars](http://en.wikipedia.org/wiki/Pulsar). Pulsars are observed by
astronomers as periodic sources of electromagnetic radiation. The frequency of
pulsations is extremely rapid ~ 1 Hz which when combined with other evidence
suggests the source must be a rapidly rotating [neutron
star](http://en.wikipedia.org/wiki/Neutron_star). It is understood that a
highly magnetized neutron star will produce a beam of radiation which is swung
out like a lighthouse - if this passes over the earth we see the neutron star
as a pulsar pulsing at the rotation frequency.


 Pulsars are second only to atomic clocks for their stability. Pulsar astonomers
demonstrate this by stacking up pulse profiles as used by Joy Division in 
their 1979 record *Unknown Pleaures*:

<center>
<a href="http://en.wikipedia.org/wiki/PSR_B1919%2B21">
<img src="http://upload.wikimedia.org/wikipedia/en/b/b5/Unknownpleasures.jpg" 
     alt="Joy Division Unknown Pleasures album cover" height="300">
</a>
</center>

Pulsars will spin-down due to torques from the electromagnetic radiation and
possibly gravitational torques. This means the pulsar clock effectively gets
slower, but in a determinstic way which can be modelled. Once this spin-down
and [other terms](http://adsabs.harvard.edu/abs/2006MNRAS.369..655H) has been
taken into account we are left with a residual which measures the pulsar stability.
If pulsars *were* perfect clocks, then all the erros would be the result of
imperfect measurements. Provided these measurements are uncorrelated, then 
the residuals would look like random white noise about the origin as illustrated
here:
<center>
<img src="/research/img/UncorrelatedNoise.png" 
     alt="" height="300">
</a>
</center>
Note this is intended as an illustration and is *not* real data. I have used the
[matplotlib xkcd](http://matplotlib.org/xkcd/examples/showcase/xkcd.html) style
for fun. 

Unfortunately, for almost every pulsar we instead find 'structure' in the residual
which is named *timing noise*. This structure appears over long time scales 
(many years of observation): below we provide an illustration from one of the
many models used to explain timing-noise (a random walk in the phase):

<center>
<img src="/research/img/CorrelatedNoise.png" 
     alt="" height="300">
</a>
</center>

Timing-noise has many features, but perhaps the most insightful is that found
by [Hobbs et al. 2010](http://adsabs.harvard.edu/abs/2010MNRAS.402.1027H): over
sufficiently long time scales (~years), the residuals tend to admit
quadi-periodic features. This suggests there is some mechanism responsible for
the deviations which operates over time scales of years. 

Many models have been proposed to explain this, my projects aims to update our
current understanding of timing-noise and apply statistical method to evaluate
the current models. In addition we try to understand the importance of timing
noise for gravitational waves from pulsars. 

