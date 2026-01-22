# Cleaning up directories

Using a computing cluster (or even your own machine), for many years, it is probable that things get messy and disorganised.
As you complete projects, the code and results often go stale, but you keep them `just in case'.
This is okay for a while, but eventually you'll be told you have TBs of storage and most of it is many years old. At this point, it is time to clean up.

## Finding the data
The first job is to figure out where the data is before you decide what to delete.

- **LIGO Data Grid visualisation tools**: If you are working on the LIGO clusters, you can find information about your home directories from regular scans at [this website](https://ldas-gridmon.ligo.caltech.edu/diskusage/). If you find your name and click the link it will give you a visualisation. If you are working on a different cluster, then contact the administrators who may be able to point you to a similar tool.
- **Summarise by directory**: If you don't have a visualisation tool to guide you, you can use standard UNIX tools. For example, if you use the `du` (disk usage tool) as follows:
    ```bash
    $ du -sh *
    4.3M directory_1/
    16M directory_2/
    50GB directory_3/
    5 file.txt
    ``` 
  you can start at the top level and drill down picking out which directories are large and okay to be removed.
  You can also count the number of files by using `find`:
    ```
    $ find <directory> -type f | wc -l
    23
    ```
  However, bear in mind that `find` will be doing a search: so if there are many files in subdirectories you may find this very slow.


## Removing the data
Once you know where the data is and you have decided to delete it, then of course you can just use `rm` to remove it. However, typically you will have directories which have a mix of lightweight configuration files and heavyweight result files and possibly also some log files. It is often wise to remove the result files and log files, but keep the configuration files for future reference (after all, they are usually only a few MB). 
You can use `find` to delete files with a certain type. First, search for them using a command like
```
find . -name "*.json" -type f
```
This will find all `json` file types and print them to the terminal. If you are happy you won't be deleting something that you want to keep, you can then delete them with
```
find . -name "*.json" -type f -delete
```
Typically, it is best to avoid delete many thousand files at once, but say focus on a specific project or folder.

