# Hints and tips on working with Latex

I work with a lot of people who use latex day to day to write documents. I see a lot of the same errors happening over and over again and this is my attempt to try and get those fixed. Therefore, this is not an article about how to do all the fun exciting things in Latex (like build diagrams with TikZ), but instead how to avoid common issues and get the most out the tool. Note that this is written predominantly as a guide to students submitting BSc/MSci projects.

## Overleaf

Obviously, [Overleaf](https://www.overleaf.com/) is great and a revolution. However, it has one feature that has lost many a student marks on their final report: by default it will [Try to compile despite errors](https://www.overleaf.com/learn/how-to/Using_the_Stop_on_First_Error_compilation_mode#:~:text=Compilation%20modes%20on%20Overleaf,-To%20manage%20LaTeX's&text=In%20the%20Try%20to%20compile,may%20also%20be%20%E2%80%9Cskipped%E2%80%9D.). As a result, new users often make mistakes which simply appear as a little red flag at the top. But, it still produces output. So no worries. However, that red flag is telling you your latex code is broken in a fundamental way. Overleaf is very clever and even tries to fix it. However, these fixes are usually mistaken and end up with your output containing nonsense. **Please make sure that you fix errors in your OverLeaf**.

## The grammar of equations

Equations are part of sentances (see, e.g. [this style guide](https://www.aanda.org/for-authors/language-editing/5-punctuation-and-style-concerns-regarding-equations-figures-tables-and-footnotes)). As such, they should be treated as part of the paragraph. For example, your latex source code may look like:

```
Newton's law of gravitation is
$$ F = G\frac{m_1 m_2}{r^2} \, , $$
where $m_1$ and $m_2$ are the mass of the two objects, $G$ is the gravitational constant, and $r$ is the separation between the masses.
```

A few notes on this:

1. After the equation, we add `\, ,`. The first part `\,` is adding [a space](https://www.overleaf.com/learn/latex/Spacing_in_math_mode), the second is adding a comma.
2. the `where` continues the sentance. Do not add a space between the equation and the next line otherwise latex will treat this as a new paragraph (usually ending up with an indentation).

Alternatively, the equation may be the end of the sentance, in which case it would finish as a full stop like this:
```
Given two masses $m_1$ and $m_2$ separated by $r$, Newton's law of gravitation can be expressed as
$$ F = G\frac{m_1 m_2}{r^2} \, . $$
```

## Text-mode subscripts

Often, we use subscripts to denote some property or other. For example, let's say you want to define the initial velocity as `$v_{init}$`. The `init` here will be in math mode (i.e. italics). Formally, it should be intepreted as `i` times `n` times `i` (etc), which is not what you mean. Therefore you should either:

1. Use text mode `$v_\text{init}$` (or equivalent)
2. Use the [subscript](https://ctan.org/pkg/subscript?lang=en) package

## Use packages

There are a number of very useful packages that I highly recommend everyone use **by default** whenever they write a latex document. These are:

1. [acronym](https://ctan.org/pkg/acronym?lang=en). Use this to ensure that you correctly introduce acronyms on their first usage and only use them once. Never handle acronyms manually, instead include `\usepackage{acronym}`. Then define the acronym
    ```
    \newacro{GW}{Gravitational Wave}
    ```
    Then whenever you want to use the acronym, inster `\ac{GW}`. On the fist use this will resolve to `Gravitational Wave (GW)`.
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

## Use macros
If you have a compicated peice of latex that you are using in multiple places, create a macro. For example, if I wanted to keep referring to the software `sklearn` but I needed to use `texttt` to match the journal style, I would define
    ```
    \newcommand{\sklearn}{\texttt{scikit-learn}}
    ```
Then at any point in the text I could write `\sklearn' to include the text. This way, should I need to change the style I only need to do so in one place.

You can also do the samething for mathematical symbols. This is expecially useful if you keep changing your mind on which symbol to use: define it once and then you can change it whenever you like. If you want to use it in the text as well, you can use `\ensuremath` like this:
```
\newcommand{\pastro}{\ensuremath{p_{\rm astro}}\xspace}
```
This way you can use `\pastro` in an equation or in the text directly.

It is typically a good idea to group together all your macro's and acro's at the top of the document in a single block of definitions.

## Textual and parenthetic citations

There are two different types of citations, textual and parenthic. Please this, e.g. [this guide](https://apastyle.apa.org/style-grammar-guidelines/citations/basic-principles/parenthetical-versus-narrative). To understand the difference.
Then, if your bibliography style allows it, use the write one by using `\citep` for parenthetic and `\citet` for textual (assuming you are using `natbib`).
