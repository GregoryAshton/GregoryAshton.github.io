Title: Tips for speeding up new system setup
Date: 2015-12-30
Category: 
Tags: 
Slug: Tips-for-speeding-up-new-system-setup
Authors: Greg Ashton

Installing a new OS can be fun and exciting, I often like to try out the new
features and switch a few times a year. However setting up the new system with
all the software and git projects that you were working on can be quite a pain.
In this post I will describe an easy way to *bootstrap* your git projects using
Max Hebditch's `batchgit` script.

To begin, we have an old system which has several git repositories, for example
perhaps it has something like

{% highlight bash %}
/home/greg/project1
/home/greg/Programs/project2
{% endhighlight %}

and these are backed up on `github` or `bitbucket`.

Then there is a new system, which we want to generate clones of these repo's.

## On the old system
Firstly we begin by heading to [the batchgit repo](https://github.com/maxhebditch/batchgit)
and cloning it. Once cloned, you need to add the directory to your bash `PATH`
variable, or alternatively always call it from wherever it is cloned. Either
way, you can then simply call `batchgit` which will walk you through the setup.
Once complete, you will find a file `~/,batchgitrc` which looks like

{% highlight bash %}
/home/greg/project1
/home/greg/Programs/project2
{% endhighlight %}

Alternatively, you could just write this yourself and then run `batchgit -s`, which,
if you have all the paths correct, will print a summary of the status of each repo.

Having setup batchgit, we can then use its *bootstrap* feature (also described
in the repo). Essentially we run

{% highlight bash %}
batchgit -b
{% endhighlight %}

which produces a directory `~/batchgit-takeaway`.

## On the new system

On the new system, copy the directory `~/batchgit-takeaway` from the old system,
for example using `scp`:

{% highlight bash %}
scp -r hostname@ipaddress:/path/to/batchgit-takeaway .
{% endhighlight %}

Now, before we attempt to clone repo's using `batchgit`, firstly check that
you have `git` installed, you have updated the ssh-keys on github/bitbucket,
and that the `batchgit` script is on your new systems bash `PATH`.
Once you have done these steps, you can proceed to run

{% highlight bash %}
batchgit -n
{% endhighlight %}

This will walk you through asking which repo's your wish to be cloned and makes
sure that things go in the correct directory.

Once complete, your new system should contain all your old repo's. Thanks very
much to Max for developing this, it has saved me a few minutes going around and
copying `url`'s from github.

