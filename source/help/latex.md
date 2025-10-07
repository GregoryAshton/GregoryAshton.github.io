# Hints and tips on working with Latex

I work with a lot of people who use latex day to day to write documents. I see a lot of the same errors happening over and over again and this is my attempt to try and get those fixed. Therefore, this is not an article about how to do all the fun exciting things in Latex (like build diagrams with TikZ), but instead how to avoid common issues and get the most out the tool. Note that this is written predominantly as a guide to students submitting BSc/MSci projects.

## Overleaf

Obviously, [Overleaf](https://www.overleaf.com/) is great and a revolution. However, it has one feature that has lost many a student marks on their final report: by default it will [Try to compile despite errors](https://www.overleaf.com/learn/how-to/Using_the_Stop_on_First_Error_compilation_mode#:~:text=Compilation%20modes%20on%20Overleaf,-To%20manage%20LaTeX's&text=In%20the%20Try%20to%20compile,may%20also%20be%20%E2%80%9Cskipped%E2%80%9D.). As a result, new users often make mistakes which simply appear as a little red flag at the top. But, it still produces output. So no worries. However, that red flag is telling you your latex code is broken in a fundamental way. Overleaf is very clever and even tries to fix it. However, these fixes are usually mistaken and end up with your output containing nonsense. **Please make sure that you fix errors in your OverLeaf**.

## The grammar of equations

Equations are part of sentences (see, e.g. [this style guide](https://www.aanda.org/for-authors/language-editing/5-punctuation-and-style-concerns-regarding-equations-figures-tables-and-footnotes)). As such, they should be treated as part of the paragraph. For example, your latex source code may look like:

```
Newton's law of gravitation is
$$ F = G\frac{m_1 m_2}{r^2} \, , $$
where $m_1$ and $m_2$ are the mass of the two objects, $G$ is the gravitational constant, and $r$ is the separation between the masses.
```

A few notes on this:

1. After the equation, we add `\, ,`. The first part `\,` is adding [a space](https://www.overleaf.com/learn/latex/Spacing_in_math_mode), the second is adding a comma.
2. the `where` continues the sentence. Do not add a space between the equation and the next line otherwise latex will treat this as a new paragraph (usually ending up with an indentation).

Alternatively, the equation may be the end of the sentence, in which case it would finish as a full stop like this:
```
Given two masses $m_1$ and $m_2$ separated by $r$, Newton's law of gravitation can be expressed as
$$ F = G\frac{m_1 m_2}{r^2} \, . $$
```

## Text-mode subscripts

Often, we use subscripts to denote some property or other. For example, let's say you want to define the initial velocity as `$v_{init}$`. The `init` here will be in math mode (i.e. italics). Formally, it should be interpreted as `i` times `n` times `i` (etc), which is not what you mean. Therefore you should either:

1. Use text mode `$v_\text{init}$` (or equivalent)
2. Use the [subscript](https://ctan.org/pkg/subscript?lang=en) package

## Units and quantities
When you present a number in `latex`, it is important that it is appropriately formatted with its unit. The [siunitx](https://texdoc.org/serve/siunitx/0) package can help with this. Add to you pre-amble
```
\usepackage{siunitx}
```
Then, when you give a quantity, write it in the latex as
```
\qty{31.4}{\Hz}
```
where the second argument is the units to use [see the documentation](https://texdoc.org/serve/siunitx/0) for a list. This will properly format it using a smaller space and keeping the units and value next to each other without a line break.

There is also a `\num{}` command if you are giving just a number.

There are many other clever things you can do, like automating the rounding process etc. Again, see the docs.

## Use macros
If you have a complicated piece of latex that you are using in multiple places, create a macro. For example, if I wanted to keep referring to the software `sklearn` but I needed to use `texttt` to match the journal style, I would define:
    ```
    \newcommand{\sklearn}{\texttt{scikit-learn}}
    ```
Then at any point in the text I could write `\sklearn' to include the text. This way, should I need to change the style I only need to do so in one place.

You can also do the samething for mathematical symbols. This is especially useful if you keep changing your mind on which symbol to use: define it once and then you can change it everywhere all at once and avoid inconsistent usage. If you want to use it in the text as well, you can use `\ensuremath` like this:
```
\newcommand{\pastro}{\ensuremath{p_{\rm astro}}\xspace}
```
This way you can use `\pastro` in an equation or in the text directly.

It is typically a good idea to group together all your macro's and acro's at the top of the document in a single block of definitions (or in a separate file).

**Use macros for result quantities**: If your paper contains results from any sort of data analysis, it is likely you'll need to communicate some numbers (e.g. the mass of a star). Please, save yourself much heartache, do not hardcode those numbers into the paper. Instead, create a macro:
    ```
    \newcommand{\massofstar}{32.5}
    ```
    then anywhere you refer to the mass, you simply write `\massofstar`. Better yet, have your analysis script write the `newcommand` lines for you in a file `macros.tex`, then add `\include{macros}` in your latex document. Now, when you inevitably find a bug in your code the day before submission, you simply rerun and replace `macos.tex`. This also allows you to `diff` between the new and old `macros.tex` to see what changed! Finally, avoid editing the macros by hand. If you need to round the numbers, do this in the analysis script (this usually takes some thinking, but the [uncertainties](https://pythonhosted.org/uncertainties/) package can help here).


## Textual and parenthetic citations

There are two different types of citations, textual and parenthic. Please this, e.g. [this guide](https://apastyle.apa.org/style-grammar-guidelines/citations/basic-principles/parenthetical-versus-narrative). To understand the difference.
Then, if your bibliography style allows it, use the right one by using `\citep` for parenthetic and `\citet` for textual (assuming you are using `natbib`).



## Organise your bibtex files

Pick a convention for the keys (I like `AUTHOR_YEAR`, but oftentimes people like to use the ADS/Inspire key) and stick with it. This avoids repeated entries. You can use online tools [like this](https://flamingtempura.github.io/bibtex-tidy/) to tidy up a messy `bib` file. Both NASA ADS and InspireHEP have nice utilisies to generate bibtex files (see, e.g. [here](https://ui.adsabs.harvard.edu/abs/2020ApJ...892L...3A/exportcitation) and click cite [here](https://inspirehep.net/literature/1774379)). They also allow you to pick the format as well. Personally, I'm not a fan of maintaining a single huge `bib` file: I write a new one for each paper.

## Useful packages

There are a number of very useful packages that I highly recommend everyone use **by default** whenever they write a latex document. These are:

1. [acronym](https://ctan.org/pkg/acronym?lang=en). Use this to ensure that you correctly introduce acronyms on their first usage and only use them once. Never handle acronyms manually, instead include `\usepackage{acronym}`. Then define the acronym
    ```
    \newacro{GW}{Gravitational Wave}
    ```
    Then whenever you want to use the acronym, insert `\ac{GW}`. On the fist use this will resolve to `Gravitational Wave (GW)`.
2. [cleverref](https://ctan.org/pkg/cleveref?lang=en). Use this to avoid writing `In Fig.~\ref{fig:X} we see..` (which is hard to keep consistent). Instead simply write `In \cref{fig:X} we see`. You can set the choice of capitalization with an optioni on import: `\usepackage[capitalise]{cleveref}`
3. [hyperref](https://ctan.org/pkg/hyperref?lang=en). Use this to turn links on. Here is some setup to control the color:
    ```
    \usepackage{hyperref}% add hypertext capabilities
    \hypersetup{
        colorlinks,
        linkcolor={red!50!black},
        citecolor={blue!90!black},
        urlcolor={blue!80!black}
    }
    ```


