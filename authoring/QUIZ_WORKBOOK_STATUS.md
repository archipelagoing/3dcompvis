# Complete quiz-workbook revision

The previous quiz treatments were uneven: some were shortened prompts with compact answers, and duplicate retests shared solutions. This revision implements the user's requested complete-problem/red-step/blue-math format across all six lectures. It supersedes earlier quiz-presentation completion claims.

## Delivered

- Six `quiz-workbook.md` pages, prominent chapter-entry links, original quiz/subquestion navigation, a rebuilt public practice index, and direct links from the previous teaching examples.
- All **18 historical quizzes** from the provided booklet: **39 original problem groups**, retaining every grouped subpart and every duplicate retest independently. The booklet's **seven original supplements** are clearly separate, giving **46 full booklet statements and 225 worked steps**.
- All **32 original end-of-chapter quiz questions** in completed Lectures 1–4 retain their statements and now have **65 worked steps**, with separate expandable web answers and openly printed solutions. Total: **78 complete problem statements and 290 styled solution steps**.
- Original problems in normal text, red numbered action headings, a short plain-English reason for every step, and blue native mathematical typesetting. Full matrix/vector inputs, row/column products, intermediate outputs, substitutions, exact fraction arithmetic and sanity checks are shown where applicable. Conceptual questions retain complete arguments rather than fabricated numerical inputs.
- Source questions follow the supplied booklet's wording and givens, with typography normalized; no claim of verbatim historical-PDF transcription. Original PDF filenames, duplicate/header notes, source errors, and added numerical companions remain identified.
- Expanded pose/block-matrix and numerical 4×4 products, tetrahedron cross products/rotated normals, full projection/DLT systems, epipolar matrices/intersections/rank checks, stereo signed errors, Harris/LK/exposure normalization, triangulation/nullspaces, a numerical Gauss–Newton update and affine factorization/ambiguity.
- Booklet camera-plane and epipolar-plane sketches preserved as editable local SVG/PDF pairs. Existing credited figures support the corresponding original questions, including the viewing-ray sketch.
- Updated prompts, authoring guide/template, TODO, registers, build instructions and portable-bundle README. Future quiz content is maintained in `quiz-worked-content.json` and rendered using `scripts/render_quiz_workbooks.py`; other chapters remain authored in MyST.

## Verification

- `scripts/check_quiz_workbooks.py`: all 46 complete question statements match the provided booklet; all 18 historical/seven supplement entries, separate retests and 225 steps accounted for. Independent calculations verify DLT/full right nullspace, Harris/eigenvalues, LK/displacement, exposure normalization, edge rank, essential constraints, triangulation/reprojection, finite-difference optimization, factorization/gauge and insufficient infinity-plane constraints.
- Existing Lecture 1–4 independent mathematical checks passed. These cover the retained source quiz answers, coordinate conventions, oriented normals, calibration, probabilities/sampling/symmetry, epipolar constraints/rank, stereo exact errors and related examples.
- `scripts/check_quiz_workbooks_browser.py`: six workbooks have the expected original-question/step counts and targets; MathJax and images render; step headings and both inline/display math have the requested colors; dark-theme contrast colors, phone-width layout, migrated example links, all four TLDR quizzes and print visibility passed. Fixed a discovered theme rule that hid closed web answers in browser print.
- **1,134 internal article links** resolved in a static HTML audit, including the moved quiz anchors.
- Strict `make all` completed: HTML/LaTeX warnings-as-errors, continuous XeLaTeX PDF compilation, index/reference resolution and source ZIP packaging. Final print log contains no overfull boxes, unresolved references, duplicate labels or missing glyphs. Existing upstream font substitutions/FontAwesome ToUnicode warnings remain.
- Final PDF: **214 pages**. Extracted text contains all **46 booklet question headings**, **32 original practice headings** and the complete worked solutions; the manuscript has exactly **290 styled step headings**. Two earlier guided-calculation headings also use the word “Step.”
- Inspected representative web questions/workings, phone rendering and final print pages for poses, epipolar matrices/intersections, exact stereo errors, normalization, Harris, triangulation/factorization and original TLDR answers. Color, native equations, matrix legibility and reading order checked.
- Portable ZIP passed integrity checks. Current PDF, manuscript and README bytes match their bundled counterparts; all **47 figure occurrences** resolve to bundled local assets. The exact exported manuscript compiled with those assets/support using XeLaTeX. Overleaf itself was not accessed.
- `git diff --check` passed; original PDFs and unrelated preexisting changes preserved.

## Review

- Local practice index: `http://127.0.0.1:8765/reference/quiz-index.html`.
- Full epipolar question: `http://127.0.0.1:8765/lectures/lecture04/quiz-workbook.html#quiz-3-q2`.
- Print artifacts: `print/CS532_Textbook.pdf`, `print/CS532_Textbook.tex`, `print/CS532_Textbook_Source.zip`.
- Question inventory: `quiz-question-coverage.csv`; reviewed workings: `quiz-worked-content.json`.

The Lecture 5–6 **quiz workbooks** are now populated; their main slide-based chapters, complete lecture figures/interactives and remaining teaching material are still unfinished. This revision does not mark the whole textbook complete. No publication, pushes or external messages performed.
