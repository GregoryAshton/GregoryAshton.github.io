Singularity container for pulsar tools
########################################

:date: 2019-01-25

I personally find installing typical tools for processing pulsar data difficult.
Previously, I did have success with `kern <https://kernsuite.info/>`_. But now
that the end of life of python 2 is less than a year away, I've moved all my
personal projects to python 3. Unfortunately, the pulsar interface for psrchive
is python 2 only.

To solve this, I've added a singularity container to `my personal collection
on singularity-hub <https://www.singularity-hub.org/collections/2045>`_. Tagged
as :code:`psrchive`, this can be used as follows

.. code-block:: console

   $ singularity pull --name psrchive.img shub://GregoryAshton/containers:psrchive
   $ singularity shell --bind $PWD psrchive.simg

The first step downloads the image. The second drops you into a shell which has
psrchive, tempo2, and the python interface along with a couple of other useful
python modules.

The recipe to build this image `can be found here
<https://github.com/GregoryAshton/containers/blob/master/Singularity.psrchive>`_.
This build on the Max Planck Institut for Radio Astronomy `docker image
<https://hub.docker.com/r/mpifrpsr/dspsr>`_.

Note, this obviously requires you to have singularity installed. For a personal
machine, see `these installation instructions
<https://singularity.lbl.gov/install-linux>`_. Singularity comes preinstalled
on most clusters, e.g., on OzStar:

.. code-block:: console

   $ module load singularity latest


