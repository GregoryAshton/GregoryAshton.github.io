Title: Some useful latex helper tools
Date: 2015-12-18
Category: 
Tags: 
Slug: Some-useful-latex-helper-tools
Authors: Greg Ashton

In this post I will descrive, mostly so I can recall in future, how a script I
wrote operates. The script, `print-tex-elements` can be found
[here](https://github.com/ga7g08/Scripts/blob/master/print-tex-elements) and
can be used to pull out useful information from a `.tex` file. 

Firstly, put this file somewhere on your `PYTHONPATH`, I keep a `Scripts` 
directory for such single-use scripts. Now for some example usage:

### Print all the labels
Calling 
{% highlight bash %}
print-tex-elements -l
{% endhighlight %}

prints *all* of the latex labels. 

### Print a subset of the labels

If you use keys to distinguish the type of labels e.g. 

{% highlight latex %}
\label{eqn: equation number one}
{% endhighlight %}

then we can just print the equation labels by giving `eqn` as the argument.
For example:

{% highlight bash %}

print-tex-elements -l fig
Printing label elements in test.tex:
305  -> fig: template jumps
474  -> fig: narrow-band example
544  -> fig: conv
605  -> fig: sliding window
663  -> fig: mismatch Tobs
663  -> fig: mismatch Tobs
{% endhighlight %}

Note that the repeated label here would be underlined, I just can't work out
how to show this. The numbers give the line number of the **first** occurance.


### Print all the figures

We can print the figure names using

{% highlight bash %}
print-tex-elements -f
Printing includegraphics elements in test.tex:
329  -> template_jumps
489  -> narrow-band_examples
556  -> S5_conv_mismatch
619  -> sliding_window
669  -> Crab_mismatch_Tobs
{% endhighlight %}

### Print all the citations

We can print the citation keys

{% highlight bash %}
print-tex-elements -c
{% endhighlight %}


For citations, repeated citations are removed. 

and
