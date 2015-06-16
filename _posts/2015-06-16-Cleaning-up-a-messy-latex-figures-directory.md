---
layout: post
title: Cleaning up a messy latex figure directory
---

Example: you have worked on a project for a few weeks/months/years
and over that time you have changed which figures are used. This generally
leaves a trail of unused files which now you want to remove. The simple answer
is to find all occurances of `includegraphics` and check if it exists in your
image collection (for me I use `./img`), then delete the rest. Here we will
provide some tools to faciliatet this.

Firstly we define what we want to find is the `figurename.png` in:

    \begin{figure}
    \centering
    \includegraphics[]{figurename.png}
    \caption{}
    \label{}
    \end{figure}

## Getting the figures used in the latex file

This can be as simple as first `grep` for lines with figrues in them, then pipe
the output into another grep matching only the contents of the `{}`
paranthesis`.  This method was inspired by [this SO
post](http://unix.stackexchange.com/questions/108250/print-the-string-between-two-parentheses)
and takes the form:

    grep "includegraphics" *.tex | grep -oP "\{\K[^}]+"

For our nice example above, this will produce `figurename.png` as expected.
Unfortunately life isn't ever simple and we often split the filename over two
lines. This neccesitates a more involved approach. I personally found it easier
to write a simple python script which follows the following logic: find
`includegraphics`, then find and print the inside of the next set of
paranthesis. For example something like

{% highlight python %}
#!/usr/bin/python

""" Find figs based on includegraphics in tex docs and prints the file names"""

import sys

filename = sys.argv[1]

with open(filename, "r") as f:
    lines = f.read()

parts = lines.split("includegraphics")
files = []
for p in parts[1:]:
    files.append(p[1+p.find("{"): p.find("}")])

files = sorted(files, key=lambda s: s.lower())

for f in files:
    print f
{% endhighlight %}

I will assume now this is saved in an exuctable `print_tex_figs` which takes
as it's only argument the tex file of interest.

## Diff the figures in the file, with the image directory

Now all we need to do is a simple diff:

    vimdiff <(print_text_flags somefile.tex) <(ls -1 img/)

Note we use the `-1` flag to ensure that `ls` prints one file per line. This
will give a vimdiff view of the files in the tex file, and those existing in
the image. In theory you could automate deleting the unused files, but this is
generally a bad idea as there is no garuntee that these files aren't used in
some other way.
