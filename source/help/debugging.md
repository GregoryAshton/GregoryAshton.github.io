# My script/job/test is not working, what should I do?

This is a very common problem. For anyone involved in scientific research
which relies on an element of programming, you will no doubt find that, at
some point you are faced with a situation where "it isn't doing what it
should be!" or "it won't run!". For those of us, like me, who did not receive
formal training on software development, this can be daunting. Your
supervisor or colleagues may expect you to solve it without help, what do you
do? It might be tempting to either give up or ask for someone else to fix it.
But, before you do either of things try to work through this list of steps:

1. **Breath**: it can be frustrating so first things first, try to take a step back. Grab a cup of tea/coffee/water and let your head clear.

2. **Read**: now, try reading both your script and the error message (in Python, this is called the `TraceBack`). The output messages might be quite long, but try scanning through it and find:

    - Which line of your script causes the error? What is it trying to do?
    - What is the error message (if any) from the output? Does it tell you which program caused the issue? You may find [this guide](https://realpython.com/python-traceback/) useful in understanding the `TraceBack`

3. **Check**: Now check out what else is going on:
    - How long does it take to fail, does it take a long time to fail or straight away?
    - What else is happening with your computer at the time? Does the memory/CPU usage of the program spike?
    - If your script relies on software, what version are you using? Is it up to date, did you update it recently?
    - Have you backed up your script, can you roll back to an earlier version to see if it works?

3. **Investigate:** hopefully by reading the scripts and logs, you might have an inkling about what is going on. Try to test it out, perhaps remove the line that is failing. What happens? Do you get a new error message? The goal here is to build some intuition about what the error is and the cause.

4. **Research:** Now that you have an idea about what is going on, it is time to research. A few places that are worth searching:
    - *Google/StackOverflow*: An easy first step is to simple search the error message on the internet. But, be warned: copy and pasting solutions is usually a recipe for disaster. Instead, read the solutions and comments to help you understand *how* they solve the problem.
    - *Documentation*: If the problem seems to be in a specific piece of software, try to find the documentation and scan it. Do they have a guide on troubleshooting, a place where they welcome questions?
    - *Source code*: If you have identified which line is failing in any underlying software, find the source code (if it is open source). Read it over. It may well be that you have found a bug: this is a great oppotunity to contribute. If you can see how to fix it, try editing the source code, this may require you to install the software from the source code to test your fix. If your fix is successful, consider opening a Merge Request/Pull Request to fix the code.

5. **Identify who you will ask for help**: If you have run through the steps above and things are still not working, you are now ready to ask for help. First, you need to identify who you will ask
    - If the problem is in a specific piece of software, does that software have a guide for getting help?
    - If you are working with a colleague/supervisor, they may be the right persont to contact now.
    - If your questions are more general, try StackOverflow or look for local programming support groups (e.g. at your University).

6. **Ask for help:** Now you know who to contact, you should write a message to them. Keep in mind the following:
    - Keep it concise. Avoid long paragraphs and lots of background, focus on what they need to know to help you.
    - Include a [Minimum Working Example](https://stackoverflow.com/help/minimal-reproducible-example). This will help them reproduce your problem. In making it you may even solve the problem yourself!
    - Include a description of your investigation and research: they will need to know all the details (i.e. versions of software, any oddities)
    - Tell them what you have tried already. This will make sure they don't repeat the same investigations you have undertaken and help them to help you.
    - If relevant, tell them why you are contacting them. If they have offered support, thank them for it! In some cases, what may appear to be a "missing feature" is in fact a large research project. If you need this feature, you may consider offering them an acknowledgement or even co-authorship on any subsequent publications.
After all of this, send your message. Have some patience, they may be overwhelmed by other tasks when you email. Feel free to email them again after a week or so if you haven't got an answer. They may have simply forgotten!

