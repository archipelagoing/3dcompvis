# Lecture 2 review status

**Reviewed with the user; progression to Lecture 3 authorized.**

## Delivered

- Chapter introduction plus seven ordered sections, ending with TLDR and eight-question quiz with explained answers.
- Spring 2020 Quiz 1: all five problem/subquestion units retained in three worked examples relocated to Lecture 1, alongside their foundation concepts; original L2 assignment preserved.
- Six numbered worked examples within Lecture 2; three short understanding checks; sixteen canonical formula/application pairs.
- Four original vector diagrams within Lecture 2, including the perspective explorer's static view, plus the quiz diagram relocated with its L1 practice; with editable TikZ and paired SVG/PDF assets; actual lecture court photograph with disclosed corner annotations and a computed inverse-sampled rectangular warp.
- Entire 129-page lecture audited. Repeated Lecture 1 geometry is cross-referenced; new rotation conversion, homography/warping, estimation and two-view material is taught here without filling the later chapters.
- Missing +1 in matrix-to-quaternion formula corrected; active/passive conventions, radial radius notation, and camera direction qualified.
- Updated coverage, formulas, quiz/figure registers, errata, glossary, keyword index and public references.

## Review locations

- Web: `http://127.0.0.1:8765/lectures/lecture02/index.html` while the existing preview server runs.
- Cumulative print: `print/CS532_Textbook.pdf`.
- Single manuscript/bundle: `print/CS532_Textbook.tex`, `print/CS532_Textbook_Source.zip`.
- Source audit: `lecture02-audit.md`, `lecture02-formulas.csv`, `coverage.csv`.

## Validation

- Numerical checks: `scripts/check_lecture02_math.py` passed, including independent rotation construction and held-out homography recovery.
- Figure sources and court warp generated; court comparison inspected.
- HTML and LaTeX export passed with Sphinx warnings treated as errors; XeLaTeX/latexmk compiled the cumulative PDF and index. Final checks cover unresolved references, missing mathematical glyphs, and overfull boxes.
- Before consolidation, Chromium checked all nine original chapter pages: equations rendered without MathJax error nodes; all article images loaded; the eight-question TLDR and answers were present. Mobile width and desktop screenshots were checked.
- Inspected all 24 original Lecture 2 PDF pages in rendered contact sheets and reviewed desktop court/quaternion and mobile screenshots. Tightened one cross-reference to remove an awkward one-line box continuation.
- Source bundle contains the continuous manuscript, PDF, support files, and selected local figures. Existing exporter/standalone compilation workflow is unchanged; no Overleaf access is claimed.

## Scope

At the original L2 handoff, Lectures 3–6 were planning outlines. The user has now authorized Lecture 3; its current state is tracked separately. No updates have been pushed or published. The portable source uses ordinary XeLaTeX plus bundled Sphinx support; Overleaf itself has not been accessed.

## Unique-content pass

Removed repeated foundations and hierarchy exposition, moved foundation quiz solutions to L1, replaced the repeated quaternion quarter-turn, and rewrote the TLDR/quiz around L2 additions. See `lecture01-02-overlap-audit.md`. Final consolidated builds and relocated references are checked after the revision.

Final consolidated checks passed: HTML and LaTeX warnings-as-errors builds, XeLaTeX PDF/index, updated numerical checker, Chromium on all eight remaining L2 pages plus relocated L1 practice, visible print solutions, and current manuscript in the portable ZIP. The chapter now has six worked examples and sixteen formula/application pairs.

## Interactive addition

Exactly one interactive explorer is placed at the relevant teaching point: perspective warp/cross-ratio in the homography section. The same MyST content supplies complete static explanation and results for print and no-JavaScript readers. See `INTERACTIVES.md` for the remaining lecture plan and validation.

**Quiz-format update:** the cross-lecture workbook revision supersedes earlier descriptions of shortened quiz examples and shared retest answers. See `QUIZ_WORKBOOK_STATUS.md` for current problem-level coverage and validation. Main lecture explanations retain their existing review status.
