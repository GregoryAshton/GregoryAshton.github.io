# Help

This page contains some helpful hints and tips that I've leared through my
career. I don't claim these to be perfect solutions, you have suggestions, please feel free to email me.

## Writing a paper/document

Writing scientific papers is a central part of life as a scientist. Like most things, investing a bit of time/money can make the process a little easier and allow you to focus on *writing* rather than the boring *admin* that inevitably goes with it. Here are a few ad-hoc things I've picked up which may help:

1. **Choose your medium**. There are many ways to write a paper. You can use `latex` directly on your computer (i.e. write a `.tex` file and compile it with `pdflatex`); you can use cloud-based latex solutions like Overleaf (see below); or you could use Word/Google Docs. All of these are great and have their place. Personally, I use `latex` directly when I'm working on a paper with more than 10 contributors and we need to use `git` to track changes and merges. I use Overleaf for most papers I write, and I use Word/Google Docs for pretty much anything which does not required images or equations.

2. **Use the tools**. There are a number of tools which can simplify your life. Taking the pain out of compilling latex, to automatically identifying and fixing spelling, gramatical, and typographic errors. As someone who has some mild dyslexia (and did not pay enough attention at school), I've found these invaluable. Given the availability of the checkers (most are free), it demonstrates real laziness to submit journal articles with typos (something I have definitely done). Here are my favourits:
    - [Overleaf](https://www.overleaf.com/): this is a cloud-based latex editor/compiler. For projects where you have a handful of collaborators, the free version works great! Make sure to use the built-in spelling correction. Overlead has an incredible ability to ignore Latex errors and still produce output. This is really useful during the the writing stage. But please, for the love of all that is good in this world, **fix those errors eventually**. They will result in broken arXiv compillations and usually many some aspect of your document is missing.
    - [Grammarly](https://app.grammarly.com/): there is a paid version which provides more in-depthanalysis. In my mind this is worth every penny if you are submitting grants/fellowships where a single typo could upset a reviewer (they are fickle beasts). But, the free version is also great. You can use this for Email, Word documents, and Overleaf (see [this S/O page](https://tex.stackexchange.com/questions/333947/integrating-grammarly-with-online-latex-editors-such-as-overleaf)).
    - [codespell](https://github.com/codespell-project/codespell): this is great for when you are forced to work on a latex document without overleaf.

3. **Use latex macros for results**: If your paper contains results from any sort of data analysis, it is likely you'll need to communicate some numbers (e.g. the mass of a star). Please, save yourself much heartache, do not hardcode those numbers into the paper. Instead, create a macro:
    ```
    \newcommand{\massofstar}{32.5}
    ```
    then anywhere you refer to the mass, you simply write `\massofstar`. Better yet, have your analysis script write the `newcommand` lines for you in a file `macros.tex`, then add `\include{macros}` in your latex document. Now, when you inevitably find a bug in your code the day before submission, you simply rerun and replace `macos.tex`. This also allows you to `diff` between the new and old `macros.tex` to see what changed! Finally, avoid editing the macros by hand. If you need to round the numbers, do this in the analysis script (this usually takes some thinking, but the [uncertainties](https://pythonhosted.org/uncertainties/) package can help here).

4. **Use latex macros for everything**: Another common headache the day before submission is that you realise you have used `\theta` to mean to different things. Doh! Or, perhaps your collaborator doesn't like you calling the dimensionaless spin of the black hole `\chi` and prefers `a_1`. To avoid the dangers of a last-minute Ctrl+F and replace, when you start writing **never use symboles directly** unless your are super super confident they will not change. Instead, define macros like
    ```
    \newcommand{\dimensionalspinmaginitude}{a_1}
    ```
    Being verbose is good here: it means you and your collaborators know that you mean the dimensionless spin magnitude, and not something else! You can also do this for things like software names where the formatting is usually journal specific. Add macros like
    ```
    \newcommand{\bilby}{\textsc{Bilby}}
    ```
    Then when you realise the journal prefers `texttt`, you change one thing.

5. **Organise your bibtex files**. Pick a convention for the keys (I like `AUTHOR_YEAR`, but oftentimes people like to use the ADS/Inspire key) and stick with it. This avoids repeated entries. You can use online tools [like this](https://flamingtempura.github.io/bibtex-tidy/) to tidy up a messy `bib` file. Both NASA ADS and InspireHEP have nice utilisies to generate bibtex files (see, e.g. [here](https://ui.adsabs.harvard.edu/abs/2020ApJ...892L...3A/exportcitation) and click cite [here](https://inspirehep.net/literature/1774379)). They also allow you to pick the format as well. Personally, I'm not a fan of maintaining a single huge `bib` file: I write a new one for each paper.


4. **Learn some grammar**: Honestly, I could not of cared less about grammar while at school. Only during my final year as an undergraduate, when we had to write a 10-page report, I realised that actually, communicating what I had learned was maybe a little bit important. While Grammarly and other tools can help, it is good to learn *why* they are making changes. Equally, if you have a collaborator who edits the text, ask them *why* and don't be ashamed. Better to learn later than never.

5. **Be consistent in your style**: English is a flexible language, but when reading a scientific article, a consistent style of writing avoids distracting the reader. For me, I found ["The Elements of Style"](https://en.wikipedia.org/wiki/The_Elements_of_Style) by Strunk and White to be hugely useful. I don't agree with all of it, but I find it useful to have a single point of reference to consult when I'm unsure. I don't always follow the advice (often you *need* the passive voice), but I try to maintain it on the whole. There is also an [automated checker in perl](https://github.com/devd/Academic-Writing-Check) which you can use to identify problem areas.

## My script/job/test is not working, what should I do?

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
