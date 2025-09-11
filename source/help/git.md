# Using git to track initial project progress

`git` is a super powerful tool. Most people have heard of `github` or `gitlab`, these are websites that store `git` repositories and allow people to collaborate in building software, to provide easy access, and to track developments in a meaningful way. However, `git` itself is simply a [version control software](https://git-scm.com/) and can be used without pushing the repository to `github` or `gitlab`. Here I describe a simple way I use `git` to track progress of projects during the initial conception.

1. Okay, so you have a cool idea for a project and you spent a day writing a hacky script which is the proof of concept. Great, now you want to expand it out, maybe add some bells and whistles.

2. Before you do anything else. Put the script + anything else into a directory with a half sensible name, then run `git init`, `git add *`, and `git commit -m "Initial commit adding everything"`. Now you have a snapshot of the code.

3. Now continue as you would anyway, perhaps adding a first bell then a whistle. But oh no! You broke the proof of concept... but how? Let's figure it out.. run `git diff` and you'll see the changes against your last working version. You spot the type fix it and then again add and commit everything.

4. Continue this process. The more often you stop and commit things the better.

5. At some point either you will figure out the project is a donut, in which case put it in the failed projects directory and move on. Or, you think it has legs. At this point you may choose to start a "fresh" git repo and try to make your commits more serious (no more curse words when you break it!). Or, you could just push your current repo to github. Who knows, when you win the Nobel prize for your ieda people may look back at those early commits to spot your genious!
I think too often we wait far to long to start using proper project management tools. By allowing yourself to just use `git` locally (i.e. you don't need to push to a repo, set up a CI, and add testing), we gain a lot of benefits without the overhead. 
