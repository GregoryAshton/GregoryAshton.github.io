# Getting a usable python environment (in WSL or in Linux)
I strongly recommend people use anaconda (AKA conda) to manage their python installation. The full instructions can be found [here](https://docs.anaconda.com/anaconda/install/index.html). If you are working in Ubuntu through WSL, follow the instructions for [Linux/Debian](https://docs.anaconda.com/anaconda/install/linux/). I'll provide a quick TLDR here:

1. Install the [prerequisites](https://docs.anaconda.com/anaconda/install/linux/#prerequisites)

2. Scroll to the bottom of [this page](https://www.anaconda.com/products/individual#linux) and copy the link address for the Linux install, something like "64-Bit (x86) Installer (581 MB)" i.e. right click "Download" and hit Copy link address)

3. Run `wget <THE LINK ADDRESS` to download the file (Note: you can just download it from the browser, but if you are working in a virtual machine/on a cluster/in WSL you'll then need to move the file from your local machine to the target. Using `wget` directly skips this step).

4. Install `anaconda` by running `bash ~/PATH/TO/FILE` where the `FILE` will be something like `Anaconda3-2020.02-Linux-x86_64.sh`

5. Finally, once you have installed `conda` and restarted, your command prompt will have start with `(base)`. This tells you that you are in the `base` conda environment. DO NOT INSTALL THINGS IN THE BASE ENVIRONMENT.

6. Instead, follow [this guide](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands) to create a new environment. For example, to create an environment called `testing` with `python 3.9`, run `conda create -n testing python=3.9`. Once complete, you'll need to activate the environment `conda activate testing`.

7. While `conda` may seem like a headache (you will no doubt forget to activate the environment occasionally and wonder why nothing works!). This headache is minor compared to the headache which occurs when you need to install two different versions of `numpy` for two different projects. As such, use a new environment for each project you work on.



