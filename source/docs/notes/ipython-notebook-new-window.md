Title: ipython notebook new window
Date: 2015-01-09
Category: 
Tags: 
Slug: ipython-notebook-new-window
Authors: Greg Ashton

Using Google chrome on Ubuntu 14.04, by default the command

    $ ipython notebook 

will open a notebook server in any existing chrome instance. This
can be a pain if you work across several workspaces. Instead, we
can tell `ipython` to always open in a new window so you don't
have to trawl through your workspaces to locate the new notebook
server. 

To do this first locate the default profile:

    $ ipython profile locate

In this directory will be a file `ipython_notebook_config.py`; if this
does not exist then run `ipython profile create` to generate the default
configuration files. This file specifies all the configuration settings
on starting up any notebooks, for more details see 
[the docs](http://ipython.org/ipython-doc/1/config/overview.html)

 
Open up `ipython_notebook_config.py` and add the line

    c.NotebookApp.browser = u'/usr/bin/google-chrome %s --new-window'

New notebook instances will now generate a new browser window. 
