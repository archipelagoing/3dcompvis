# Step 0 foundation status

Completed locally on October 22, 2026. Lecture writing has not begun; next is the Lecture 1 audit and slide-example selection.

## Delivered

- Six lecture-aligned navigation chapters with clearly labeled planning outlines, introductory notation/prerequisite pages, and public formula/quiz/glossary/credit/errata references.
- Shared MyST source, HTML stylesheet, authoring template, stable-label and numbering conventions, and custom web/print teaching boxes.
- Six lecture image folders in both editions. An original pixel-axis diagram validates the paired SVG/PDF workflow, with editable TikZ source and credits.
- A 563-page initial coverage inventory, 20-source quiz register (18 in scope), figure-credit register, and errata register. Source paths exist. These are initial registers, not completed topic/formula/subquestion audits.
- Inspected Lecture 1/2 heading overlap and provisional teaching ownership in `lecture-boundaries.md`. Full mathematical and visual audits remain lecture-by-lecture work.
- A continuous `print/CS532_Textbook.tex`, compiled PDF, bundled Sphinx support, and portable source ZIP. `make all` builds both editions; `make bundle` refreshes the downloadable print source.

## Verification

- Installed the existing TeachBooks stack in an isolated Python 3.11 environment; used TeachBooks 0.2.4, Jupyter Book 1.0.4.post1, and Sphinx 7.4.7.
- HTML and LaTeX export succeeded with Sphinx warnings treated as errors.
- Checked six generated lecture pages, formula/application markup, equation anchor, SVG selection, and quiz/register source paths.
- XeLaTeX/latexmk compiled the continuous letter-size PDF, with makeindex and resolved references. Checked lecture numbering starts at 1, the index exists, and print solutions remain visible.
- Inspected rendered notation/formula and figure pages. Checked the final LaTeX log for unresolved references, undefined commands, overfull boxes, and missing characters.
- Extracted the portable ZIP into a separate temporary directory and successfully compiled it using latexmk/XeLaTeX without the project Python environment. The last layout refinements were also rebuilt successfully in the project.

## Limits and remaining work

- Overleaf itself has not been accessed; the portable bundle's underlying local LaTeX compilation was verified.
- HTML structure was checked, but no browser screenshot review was performed in this step. Review both editions with the Lecture 1 pilot.
- TeX emits benign font/icon mapping and size-substitution notices from the upstream class; inspect future content for actual missing mathematical characters.
- Detailed explanations, slide-example choices, formula inventories, prerequisite refreshers, and quiz subquestion solutions are still to be written and verified per lecture.
- Nothing was committed, pushed, or published. The existing live book is unchanged.
