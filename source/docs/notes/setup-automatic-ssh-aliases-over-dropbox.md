Title: setup automatic ssh aliases over dropbox
Date: 2015-01-23
Category: 
Tags: 
Slug: setup-automatic-ssh-aliases-over-dropbox
Authors: Greg Ashton

Like many people I frequently work on the same project on several computers. 
This usually results in frequent use of `ssh` when I forget to commit changes
on git, or don't have all the correct software on one computer. Since I don't 
have a static ip I have been using [Dropbox](http://lifehacker.com/5737187/
use-dropbox-to-find-the-ip-address-of-your-remote-computers) to keep track of 
the address and then update aliases manually. Today I decided to automate the
process and as I know I will forget how I did it, I will record the process
here for myself in the future.

### Python script

Firstly we need a script which saves an the address as a useful alias:

#!/usr/bin/python

import subprocess
import os

# Read in the ipaddress, hostname and username
command_line = "/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2| awk '{print $1}'"
ipaddress = subprocess.check_output(command_line, shell=True).rstrip("\n")
hostname = subprocess.check_output("hostname", shell=True).rstrip("\n")
user = subprocess.check_output("/usr/bin/whoami", shell=True).rstrip("\n")

# Save results in a dictionary
data = {}

# Save aliases in a file
dir_of_script = os.path.dirname(os.path.realpath(__file__))
alias_file = "ssh-aliases"
alias_file = dir_of_script+"/"+alias_file

# If file exists read in data
try:   
    with open(alias_file, "r") as file:
        for line in file:
            [alias, syscall] = line.split("=")
            data[alias.lstrip("alias ")] = syscall.lstrip("'ssh -X ").rstrip("'\n").split("@")
    data[hostname] = [user, ipaddress]
except IOError:
    data = {hostname : [user, ipaddress]}

# Write to the file
with open(alias_file, "w+") as file:
    for key, val in data.iteritems():
        file.write("alias {}='ssh -X {}@{}'\n".format(key, val[0], val[1]))
{% endhighlight %}

When run, this will save a file in the current directory `ssh-aliases` containing
an aliases to access the current machine. If a previous entry existed and the ip
address has changed then the alias file will be updated. 

### Dropbox
A simple way to share these aliases between several computers is to use 
Dropbox. Save the script above as `saveIP.py` in a directory `eyeP` of your
Dropbox folder. 

### Crontab 
Now we need to ask each computer to automatically run this python script at 
startup. This can be achieved by adding a crontab job. First run 

    crontab -e

If this is the first time you have run crontab it will ask you which editor to
use. When in doubt, choose the default. Then add the line 

    @reboot sleep 60 && python ~/Dropbox/eyeP/saveIP.py

editing the path as appropriate. Note that the cronjob sleeps for a minute first,
this avoids issues where the ipaddress and username come up blank. I don't
know what causes them, but this seems a sensible work around.

### Edit profile
Finally we just need to edit `~./bashrc` on any computer that we want to use
these aliases on. Simply add the line 

    source ~/Dropbox/eyeP/ssh-aliases

and after reloading the profile (`$ bash`), you should be able to use the
aliases. For now this script simply sets these aliases by the computers
host-name which can be checked by running `$ hostname`.  Obviously this may
cause conflicts if you have the same host-name on two computers.
 
