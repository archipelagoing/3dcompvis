# Lecture 4 review status

**Ready for user review.** The user approved Lecture 3 and authorized Lecture 4. Lectures 5–6 remain outlines.

## Delivered

- Introduction plus seven ordered sections: epipolar quiz applications; noisy F estimation; essential matrices/poses; stereo depth and error; dense matching; review; final TLDR and eight-question answered quiz.
- All 77 source pages audited textually and visually. Printed-number discontinuity and unnumbered page 54 recorded. Canonical distortion, fundamental-matrix and rectification references retain their L2 location; the requested L4 guided recap makes this chapter usable without jumping away for each explanation.
- All six assigned quiz sources and their subparts completed, including both duplicate retests and the mixed-year header. Fall 2025 Quiz 2's supplied matrix has determinant four/rank three; the line/point equality is corrected explicitly. Stereo answers distinguish exact signed errors from the supplied first-order magnitude.
- Eleven numbered worked examples, three additional guided epipolar calculations, and eleven canonical formula/application pairs. Includes a reproducible noisy 12-match normalized F fit with held-out checks and an explicit four-pose/positive-depth calculation.
- Seven figures: five original paired SVG/PDF diagrams; an editable paired panel of actual source toy/plant photographs; the unmodified source window-size comparison. Extracted originals, editable vector sources, captions and source/rights uncertainty retained.
- One genuine local 3D stereo explorer: modeled camera/image-plane geometry, epipolar plane, true and perturbed ray intersections, linked image coordinates, numerical substitutions, depth/baseline/focal/error controls, point dragging, inspection orbit/zoom, keyboard controls/reset, and static print/no-JavaScript counterparts.
- Updated navigation, coverage, formulas, quiz/figure/errata registers, glossary and independent keyword index entries, prior-chapter cross-references, TODO, build instructions and portable-bundle README.

## Original delivery validation (before clarity revision)

- `scripts/check_lecture04_math.py`: all quiz parts, determinant/rank/source correction, regenerated rounded training dataset, noisy F singular values, 0.49-pixel training and 0.33-pixel held-out symmetric RMS errors, essential constraints and four proper poses, signed exact stereo errors and disparity limits, seven/eight-point RANSAC budgets, SAD/SSD/NCC, rank/Census and adaptive costs passed.
- `scripts/check_lecture04_browser.py`: all eight L4 pages rendered equations/images without MathJax errors; ten independently computed stereo states passed, including actual 3D virtual-plane intersections and ray reprojection, zero/negative measured disparity and off-image observations. Point dragging changed modeled depth; orbit/zoom preserved modeled numbers. Reset, keyboard, phone width/both camera labels, print/no-JS/blocked-module/no-WebGL fallbacks, and initialization of all three earlier widget kinds passed.
- Exactly one intended widget occurs in each completed lecture. Independent keyword entries link to teaching locations as well as glossary entries.
- `make all`: strict HTML and LaTeX warnings-as-errors builds passed; the exported continuous manuscript and index compiled with XeLaTeX/latexmk. Final TeX log has no overfull boxes, unresolved references, missing glyphs, or multiply defined labels. Existing upstream font-size/FontAwesome ToUnicode warnings remain benign.
- Inspected all 22 L4 print pages in contact sheets and affected pages individually, plus vector figures and desktop/mobile screenshots. Fixed a wide normalization-matrix display, a detached formula heading, one-line box tails and phone framing. Final TLDR and complete quiz/answers occupy separate pages.
- Cumulative PDF: 133 letter-size pages. L4 occupies PDF pages 93–114 (printed 89–110).
- Portable ZIP integrity and exact current manuscript/PDF/README bytes verified. All 34 manuscript figure occurrences resolve to bundled assets, including all six new figures and required Sphinx support. The exported manuscript compiled with those local assets/support and ordinary XeLaTeX. Overleaf itself was not accessed.
- `git diff --check`: passed. Existing unrelated workspace changes preserved.

## Review locations

- Local preview: `http://127.0.0.1:8765/lectures/lecture04/index.html` while the preview server runs.
- PDF: `print/CS532_Textbook.pdf`.
- Running manuscript: `print/CS532_Textbook.tex`.
- Portable import/print bundle: `print/CS532_Textbook_Source.zip`; select XeLaTeX and follow its README.
- Source evidence: `lecture04-audit.md`, `lecture04-formulas.csv`, `lecture04-matches.csv`, `coverage.csv` and quiz/figure/errata registers.

L4 user review remains pending before starting L5. No publishing or pushes performed.

## User-requested clarity revision

- Renamed chapter/epipolar/stereo titles for TOC and search visibility. Added direct homepage routes to the three guided calculations, each assigned epipolar quiz example, stereo sensitivity and 3D explorer.
- Explained ray → plane → line; added a notation/shape table and an original paired SVG/PDF sloping-line illustration. Guided calculations show row-by-row multiplication, several match tests, normalized point-line distance, reverse mapping with the transpose, and both epipole nullspaces.
- Expanded all epipolar quiz arithmetic: symbolic row/column selection, both third-view matrix products, every cross-product component, homogeneous division and substitution checks, and the supplied row-product/line solution. Preserved existing quiz/example labels and source errata.
- Expanded stereo derivation, signed exact-error fraction algebra, derivative and non-calculus interpretation, relative error, distance-squared local sensitivity, near/far comparisons, a bounded-error interval, and both quizzes' exact signed calculations. Retained the single genuine 3D widget and static fallback.
- Added independent camera-derived F/rank/nullspace/projection checks, scale-invariant line distance, finite-difference sensitivity and interval checks. Browser checker also verifies direct example/sensitivity targets and phone layout of the revised pages.
- Final revision verification: independent math checker passed; strict `make all` HTML/LaTeX/PDF/bundle build passed; full browser checker passed all eight pages, new direct calculation/sensitivity links, mobile page width, ten independent ray states and existing interactive/fallback checks.
- Inspected the revised web screenshots, all initial revision L4 print pages, then affected final pages after print layout adjustments. Final TeX log has no overfull boxes, unresolved references, duplicate labels or missing glyphs. The existing font substitution/FontAwesome warnings remain.
- Current cumulative PDF: **140 pages**. Revised L4 occupies PDF pages **93–121** (printed **89–117**); these counts supersede the original delivery counts above.
- Current portable ZIP passed integrity checks; PDF, manuscript and README match the working exports exactly. All **35** manuscript figure occurrences resolve to bundled assets. `git diff --check` passed. No publishing or pushes performed.

**Quiz-format update:** the cross-lecture workbook revision supersedes earlier descriptions of shortened quiz examples and shared retest answers. See `QUIZ_WORKBOOK_STATUS.md` for current problem-level coverage and validation. Main lecture explanations retain their existing review status.
