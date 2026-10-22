# Compile the printable textbook

This folder is a generated print edition of the MyST pages in `book/`.
It currently contains the Lecture 1 draft, the shared foundation, and clearly labeled planning outlines for Lectures 2–6.

## Overleaf

Upload `CS532_Textbook_Source.zip` as a new project. Select `CS532_Textbook.tex`
as the main document and **XeLaTeX** as the compiler. Keep `_support/`, `images/`,
and `.latexmkrc` in the project. They supply the bundled typesetting support,
figures, and index/build settings. No Python, Sphinx installation, or remote
image download is needed to compile the bundle.

## Local LaTeX

Install a full TeX Live or MacTeX distribution with XeLaTeX, latexmk, tcolorbox,
and makeindex. In this directory run:

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error CS532_Textbook.tex
```

`latexmk` runs makeindex and the necessary repeated LaTeX passes to resolve page
numbers and references. The output is `CS532_Textbook.pdf`.

The `.tex` contains the entire running document; `_support/` contains Sphinx
styles and supporting files rather than separately assembled chapter manuscripts.
Generated markup is more verbose than hand-written LaTeX, but the complete bundle
compiles using an ordinary LaTeX installation. Edit the Markdown source for
lasting changes and regenerate with `make bundle`; direct edits to this export
will be overwritten.

Overleaf import must still be verified in Overleaf itself. Local compilation of
the portable bundle checks the underlying XeLaTeX workflow without that service.
