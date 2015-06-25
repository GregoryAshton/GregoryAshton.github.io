---
layout: post
title: Ipython NBConvert latex template to hide code
---

In this work I will detail a method to produce a latex pdf from an ipython
notebook and selectively hide the code. This was explained to me at the
Next-Generation Computational Workshop Summer academy hosted by the University
of Southampton in June 2015. In particular thanks to Min RK and Ian Hawke for
help. The materials for the course were hosted [here](https://github.com/jupyter/ngcm-tutorial)
and a [this](https://github.com/jupyter/ngcm-tutorial/blob/master/Day-2/nbconvert_templates/Nbconvert%20templates.ipynb)
is a particuarly useful notebook which detailed the exersize prompting this
work.

The basic idea is to create a 
[template](http://ipython.org/ipython-doc/1/interactive/nbconvert.html) used by
the converter, for more information about the templates see [Jinja2
documentation](http://jinja.pocoo.org/docs/dev/templates/). This template instructs
the converter to selectively hide code cells.

## The template

Create a file called `hidecode.tplx` containing:

    ((*- extends 'article.tplx' -*))
    
    ((* block input_group *))
        ((*- if cell.metadata.get('nbconvert', {}).get('show_code', False) -*))
            ((( super() )))
        ((*- endif -*))
    ((* endblock input_group *))

Now if this template exists in the local directory of the notebook that you
wish to convert we can simply operate with

    $ ipython nbconvert --to pdf --template hidecode Example.ipynb

## Adding the template to a default path

If you intend to use the converter from multiple locations then instead of
porting a copy of this to each place (providing an absolute path should work, but
I have not had success) we can place it in a default location and instruct 
the converter to search there for templates.

We will be editing the ipython profile: to find which one you are using you can
run

    $ ipython profile locate

Usually this will produce 

    /home/user/.ipython/profile_default

If not you can populate a profile with `ipython profile create`. 

The general gist is to create or edit the file
`/path/to/profile/ipython_nbconvert_ config.py` with the following lines:

    c = get_config() 
    c.LatexExporter.template_path = ['.', "/home/user/.ipython"]

Both lines will exist if you autopopulated the profile, but the second you will
need to remove the comment and add the second element of the list: this is 
were we will place the file `hidecode.tplx`. Once you have placed `hidecode.tplx`
in the directory corresponding to the second element of the aforementioned list,
then we can simply run:

    $ ipython nbconvert --to pdf --template hidecode Example.ipynb

From any directory and it will find the hidecode template.

## Using the template

The template allows you to select which code blocks to display. By default all
code-blocks are hidden, to show one change the meta-data to

    {
      "nbconvert": {
        "show_code": true
      },
    }

a value of `false` or no value will result in the code being hidden when producing
a pdf.

