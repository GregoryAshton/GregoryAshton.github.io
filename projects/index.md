---
layout: default
title: Projects
---

# Projects

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

