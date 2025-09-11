# Writing a paper/document

Writing scientific papers is a central part of life as a scientist. Like most things, investing a bit of time/money can make the process a little easier and allow you to focus on *writing* rather than the boring *admin* that inevitably goes with it. Here are a few ad-hoc things I've picked up which may help:

1. **Choose your medium**. There are many ways to write a paper. You can use `latex` directly on your computer (i.e. write a `.tex` file and compile it with `pdflatex`); you can use cloud-based latex solutions like Overleaf (see below); or you could use Word/Google Docs. All of these are great and have their place. Personally, I use `latex` directly when I'm working on a paper with more than 10 contributors and we need to use `git` to track changes and merges. I use Overleaf for most papers I write, and I use Word/Google Docs for pretty much anything which does not required images or equations.

2. **Use the tools**. There are a number of tools which can simplify your life. Taking the pain out of compiling latex, to automatically identifying and fixing spelling, gramatical, and typographic errors. As someone who has some mild dyslexia (and did not pay enough attention at school), I've found these invaluable. Given the availability of the checkers (most are free), it demonstrates real laziness to submit journal articles with typos (something I have definitely done). Here are my favourits:
    - [Overleaf](https://www.overleaf.com/): this is a cloud-based latex editor/compiler. For projects where you have a handful of collaborators, the free version works great! Make sure to use the built-in spelling correction. Overlead has an incredible ability to ignore Latex errors and still produce output. This is really useful during the the writing stage. But please, for the love of all that is good in this world, **fix those errors eventually**. They will result in broken arXiv compilations and usually many some aspect of your document is missing.
    - [Grammarly](https://app.grammarly.com/): there is a paid version which provides more in-depthanalysis. In my mind this is worth every penny if you are submitting grants/fellowships where a single typo could upset a reviewer (they are fickle beasts). But, the free version is also great. You can use this for Email, Word documents, and Overleaf (see [this S/O page](https://tex.stackexchange.com/questions/333947/integrating-grammarly-with-online-latex-editors-such-as-overleaf)).
    - [codespell](https://github.com/codespell-project/codespell): this is great for when you are forced to work on a latex document without overleaf.

3. **Use latex macros for results**: If your paper contains results from any sort of data analysis, it is likely you'll need to communicate some numbers (e.g. the mass of a star). Please, save yourself much heartache, do not hardcode those numbers into the paper. Instead, create a macro:
    ```
    \newcommand{\massofstar}{32.5}
    ```
    then anywhere you refer to the mass, you simply write `\massofstar`. Better yet, have your analysis script write the `newcommand` lines for you in a file `macros.tex`, then add `\include{macros}` in your latex document. Now, when you inevitably find a bug in your code the day before submission, you simply rerun and replace `macos.tex`. This also allows you to `diff` between the new and old `macros.tex` to see what changed! Finally, avoid editing the macros by hand. If you need to round the numbers, do this in the analysis script (this usually takes some thinking, but the [uncertainties](https://pythonhosted.org/uncertainties/) package can help here).

4. **Use latex macros for everything**: Another common headache the day before submission is that you realise you have used `\theta` to mean to different things. Doh! Or, perhaps your collaborator doesn't like you calling the dimensionaless spin of the black hole `\chi` and prefers `a_1`. To avoid the dangers of a last-minute Ctrl+F and replace, when you start writing **never use symbols directly** unless your are super super confident they will not change. Instead, define macros like
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


