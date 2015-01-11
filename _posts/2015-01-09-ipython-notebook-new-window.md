---
layout: post
title: Opening ipython notebooks in a new window
---

Using Google chrome on Ubuntu 14.04, by default the command

    $ ipython notebook 

will open a notebook server in any existing chrome instance. This
can be a pain if you work across several workspaces. Instead, we
can tell `ipython` to always open in a new window so you don't
have to trawl through your workspaces to locate the new notebook
server. 

To do this first locate the default profile:

    $ ipython profile locate

In this directory will be a file `ipython_notebook_config.py` to
which you add the line 

    c.NotebookApp.browser = u'/usr/bin/google-chrome %s --new-window'


