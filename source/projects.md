# Projects

In this page, I collect various miscellaneous coding projects I have been
involved in.

* [Python for Science](https://github.com/GregoryAshton/Python-for-science-programming) A set of workbooks to introduce python for scientific programming

* [koala_html](https://github.com/GregoryAshton/koala_html) A package to quickly create html pages from collections of images

* [kookaburra](https://github.com/GregoryAshton/kookaburra) A python package
for profile-domain timing of radio pulsars

* [parallel_bilby](https://git.ligo.org/lscsoft/parallel_bilby) A python package to leverage slurm-based HPC clusters. Enables scaling inference jobs up to many hundreds of cores.

* [bilby_pipe](https://git.ligo.org/lscsoft/bilby_pipe) A python package for
automating the job of running multiple jobs on LIGO Data Grid clusters.

* [bilby](https://git.ligo.org/lscsoft/bilby) A python package providing a user
  friendly interface to perform parameter estimation. It is primarily designed
and built for inference of compact binary coalescence events in interferometric
data, but it can also be used for more general problems.

* [PyFstat](https://github.com/PyFstat/PyFstat) A python
  package containing various methods to run continuous gravitational wave
  searches. Includes glitch-robust, MCMC-based, and transient work.

* [Bayes Bimodal Test](https://github.com/ga7g08/BayesBimodalTest) A simple
  python module using the emcee MCMC software to perform a Bayesian model
  comparison of bimodality.

* [GitCheck](https://github.com/ga7g08/GitCheck): A python appindicator which
  provides a visual check of the status of git repos. This builds on some of
  the functionality of [batchgit](https://github.com/maxhebditch/batchgit) by
  Max Hebditch.

<div style="text-align:center">
<a href="https://github.com/ga7g08/GitCheck">
<img src="https://raw.githubusercontent.com/ga7g08/CheckGit/master/demo.png"
     alt="GitCheck demo"
     align="middle"
     style="width:450px">
</a>
</div>

* [GetTrainTimes](https://github.com/ga7g08/GetTrainTimes): a command-line
  tool to quickly get train times from the national rail (UK) website.

<div style="text-align:center">
<a href="https://github.com/ga7g08/GetTrainTimes">
<img src="https://raw.githubusercontent.com/ga7g08/GetTrainTimes/master/demo.png"
     alt="GetTrainTimes demo"
     align="middle"
     style="width:450px">
</a>
</div>

* [pyweather](https://github.com/ga7g08/pyweather): a command-line tool to
  quickly get a visual (ASCII) forecast of the weather for (almost) any location.

<div style="text-align:center">
<a href="https://github.com/ga7g08/pyweather">
<img src="https://raw.githubusercontent.com/ga7g08/pyweather/master/Budapest_demo.png"
     alt="pyweather demo"
     align="middle"
     style="width:450px">
</a>
</div>

* [Using the Google maps API to study average driving speeds around the
   globe](https://github.com/ga7g08/GoogleMapsAPI_experiment).
   To see the results [have a look here](https://github.com/ga7g08/GoogleMapsAPI_experiment/blob/master/Results.md)

* [Printing latex elements](https://github.com/ga7g08/Scripts/blob/master/print_tex_elemnts):
  This isn't so much a project as a useful script. Often in cleaning up latex
  docs I trawl through the document searching for occurances of say
  `includegraphics`. This script will simply print the elements (for example
  in `\label{eqn: an equation}` the element would be `eqn: an equation`) to the
  command line. It takes multiple files and if unspecified will search for 
  proper tex files to use. It has default flags of `-f` to find figures and 
  `-l` to find labels, but you can specify whatever you want with `-o`. For
  example

``` 
    $ print_tex_elements somearticle.tex -o cite
```

  might for example produce

    Einstein1916
    Newton1675

