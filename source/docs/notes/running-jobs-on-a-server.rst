Running jobs on a server
########################

:date: 2018-08-06

Running jobs on a cluster is quite different to your personal laptop. In this
post, I'll try to list a few tips which may help you get setup and running.
I'll use the OzStar cluster as an example, but the general advise equally
applies to other clusters.

Bookmark the documentation
--------------------------

If someone has taken the time to write documentation for the cluster. Make sure
you know where it is and have read at least the overview and any advise they
provide. For example, the OzStar documentation can be found `here
<https://supercomputing.swin.edu.au/docs/index.html>`_.

Logging in
----------

Usually, you'll be given an ssh address to log into by the documentation.
You'll be using this every time you log in so create an alias. First check that
you can login with the advise given. Once your happy with that, create an
`alias <http://tldp.org/LDP/abs/html/aliases.html>`_ to avoid having to
remember the ssh address. To do so, add something
like this to your :code:`.bashrc`

.. code-block:: console

    alias cluster='ssh -X username@ssh.address.com

Here the user name and address should be replaced, additionally you may prefer
to name the alias something like :code:`ozstar` instead of :code:`cluster`. The
flag :code:`-X` enables "X-forwarding", the means that you'll be able to
display graphical output on your local computer from the cluster.

Editing files
-------------

A cluster will typically not be located in the same building as you, nor even
the same continent. As such, it can often be slow to transfer data to/from
your local computer to the cluster. While it is technically possible to run
an integrated development environment (IDE) or other graphical text editor on
a cluster, there will likely be times when its too slow to be useable.

Instead, you should get familiar with at least one command-line text editor.
There is plenty of unsolicited advice around about why you should/shouldn't use
this one or that one. If you just want to get on with it, I suggest you use
`nano <https://wiki.gentoo.org/wiki/Nano/Basics_Guide>`_. Its on most
clusters and has a help bar at the bottom to show you how to use it. To get
started, simply run

.. code-block:: console

   $ nano text-file-you-want-to-edit.txt

and follow the instructions.


Persistent sessions and multiple screens
----------------------------------------

As you work more on a cluster, you may find it frustrating that it isn't easy
to get back to where you where after logging out and logging back in. Moreover,
you may wish to have multiple terminals. One for editing a file and the other
for running some script.

A solution to both of these problems is `tmux
<https://github.com/tmux/tmux/wiki>`_. There are many good articles on
everything that can be done with tmux, here I'll just give a quick guide to
using it on a cluster.

First, write following to a configuration file :code:`~/.tmux.conf`

.. code-block:: console

    unbind C-b
    set -g prefix C-a

    bind -n C-h select-pane -L
    bind -n C-j select-pane -D
    bind -n C-k select-pane -U
    bind -n C-l select-pane -R

    # Enable mouse mode (tmux 2.1 and above)
    set -g mouse on

    # Enable highlight of active window
    set -g window-style 'fg=colour247,bg=colour236'
    set -g window-active-style 'fg=colour250,bg=black'

Then, add the following alias to your :code:`.bashrc`

.. code-block:: console

    alias s='tmux new-session \; split-window -h \;'

(you can of course name the alias however you like).

Now, to start a session, at the command line run

.. code-block:: console

   $ s

This will open a new window with two panes. You can switch between them with
the commands :code:`CTRL+h` and :code:`CTRL+l` (note the plus here means press
both at the same time). these choices are not default tmux, but where set in
the configuration file above. You can now edit files in one pane and run
scripts with the other.

To log out of the pane, press :code:`CTRL+a` and then :code:`d`. This will drop
you back into the session (known as dettaching) you where at before. Now run

.. code-block:: console

   $ tmux ls

This will print a list of all the active sessions. You can log into one by running

.. code-block:: console

   $ tmux a -t 1

Where the number is the number (or name) of the session. The key point is that
you can now log out of the cluster, log back in and attached to a running
session which will be in exactly the state you left it before logging out.

A word of warning. It's possible with tmux to set jobs running on the head
node and leave them while you log out. This may be okay for some short-medium
length script, but in general should be avoided as it clogs up resources on the
head node. It's much kinder to other users to always submit jobs through the
proper queue.

Note, in the configuration file above. We set the tmux prefix to be
:code:`CTRL+a`. The default is :code:`CTRL+b`.

Updating :code:`DISPLAY`
------------------------

One downside to using tmux, is that it is possible for the X-forwarding to
get out of sync. Effectively, when you log in to the cluster with X-forwarding,
an environment variable :code:`$DISPLAY` is set. You can view what its set to
with

.. code-block:: console

    $ echo $DISPLAY
    localhost:11.0

for example. If, when running in tmux, you get warnings related to the DISPLAY
varibale. Try checking that it is set to the same value in the tmux session
as in the standard login shell. To set the variable, run

.. code-block:: console

    $ export DISPLAY='localhost:14.0'

for example.

Function for logging into pcdevX
--------------------------------

The CIT clusters are accessed via

.. code-block:: console

   $ gsissh ldas-pcdev1.ligo.caltech.edu
   $ gsissh ldas-pcdev2.ligo.caltech.edu
   $ ...

Rather than create an alias for each, one can add a bash function to your
bashrc

.. code-block:: console

   function pcdev(){
       gsissh ldas-pcdev$1.ligo.caltech.edu
   }

then

.. code-block:: console

   $ pcdev 1  # To access pcdev1


Browsing files on a cluster
---------------------------

For clusters which use ssh login, you can easily browse files using your local
computers file browser. On Ubuntu, open nautilus, navigate to
"File/Connect to Server" and enter the address as

.. code-block:: console

    sftp://USERNAME@SSH-LOGIN/file/path

For example, if your username on OzStar is "john", this would be

.. code-block:: console

    sftp://john@ozstar.swin.edu.au/home/john

From the file browser you can then natively open images and copy files.

