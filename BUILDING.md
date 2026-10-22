# Build and author the textbook

## Single source of truth

Write content in `book/` using MyST Markdown. `book/_toc.yml` controls reading
order for both editions. The native Sphinx/Jupyter Book LaTeX writer exports
one continuous manuscript; the exporter bundles the necessary typesetting
support and local figures. Do not maintain a separate hand-edited print text.

See `authoring/STYLE_GUIDE.md`, `authoring/templates/section.md`, and `todo.md`.
The original template exercise files remain on disk, outside the new navigation.

## Setup

Use Python 3.11 and a full TeX distribution (MacTeX or TeX Live). With `uv`:

```sh
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

Alternatively create a Python 3.11 virtual environment and use its pip.
The requirements retain the existing TeachBooks/Favourites stack and constrain
Jupyter Book to its compatible v1 series. The current Favourites requirement
tracks its upstream Git repository; its exact dependency versions may change.

## Commands from the repository root

| Command | Result |
| --- | --- |
| `make html` | Website at `book/_build/html/index.html` |
| `make latex` | Full manuscript at `print/CS532_Textbook.tex` plus support/assets |
| `make pdf` | Exports and compiles `print/CS532_Textbook.pdf` |
| `make bundle` | Compiles and packages `print/CS532_Textbook_Source.zip` |
| `make all` | Website, manuscript, PDF, and portable bundle |

Builds fail on Sphinx warnings. Index generation and repeated reference passes
are handled by latexmk. Upload the source ZIP to Overleaf, select the main `.tex`
and XeLaTeX, and follow `print/README.md`. Building locally does not publish the
website. The existing GitHub Actions workflow publishes only after changes are
pushed through the authorized repository workflow.

## Source and figure registers

`authoring/coverage.csv` starts with one row per PDF page, including image-only
pages. Expand it with verified topics/formulas and printed slide numbers during
each lecture audit. No extracted heading is automatically considered complete.
`authoring/quiz-index.csv` tracks primary lecture placement, duplicates, exclusions,
and verification status. Add subquestion-level entries during chapter authoring.

Add each selected image to `authoring/figure-credits.csv`. Use paired SVG/PDF
diagram assets where appropriate and check the actual builder selection. The
exporter places selected print assets under `print/images/` and packages support
files under `print/_support/`. Do not infer asset rights from the book's license.

When adding a chapter, update the public formula/glossary/quiz/errata references
as well as the registers. Compile both editions before marking it complete.

## Lecture 1 authoring checks

Run `.venv/bin/python scripts/check_lecture01_math.py` for the independently checked numerical examples. Rebuild the original vector diagrams with `.venv/bin/python scripts/build_lecture01_figures.py`; this requires XeLaTeX and Poppler's `pdftocairo`. The generated assets are already included, so ordinary book builds do not need to regenerate figures.

The local textbook extension deduplicates extension scripts in HTML builds. The optional Favourites MathJax loader patch is disabled to keep one standard MathJax loader and avoid duplicate startup. A forced full HTML rebuild is available with `teachbooks build book --builder html --all --warningiserror` after changing renderer configuration.

## Lecture 2 authoring checks

Install the optional numerical/image dependencies with `uv pip install --python .venv/bin/python -r requirements-authoring.txt` (these also support Lecture 1's numerical checker). Run `.venv/bin/python scripts/check_lecture02_math.py` to verify the quiz calculations, quaternion conversions, DLT, sampling, RANSAC and epipolar examples.

Regenerate Lecture 2's diagrams and computed court warp with `.venv/bin/python scripts/build_lecture02_figures.py`; this also requires XeLaTeX and Poppler. The source court photograph, approximate corner coordinates, and output dimensions are retained. No downloads are needed to regenerate these assets, and ordinary book builds use the bundled images without regeneration.
