# Lecture 3 review status

**User approved this chapter and authorized progression to Lecture 4.** Lecture 2's review checkpoint was satisfied by the user's instruction to proceed.

## Delivered

- Chapter introduction plus six ordered sections, ending in a final TLDR with eight original questions and explained answers. Print puts the summary on one page and the quiz/answers on the next.
- All 80 source pages audited visually and textually. Pages 2–80 repeat L2 PDF 51–129; canonical theory stays in L1/L2, with explicit coverage destinations and source credits.
- Eight numbered worked examples: FOV/K; physical principal point; Euclidean ray cross product; known-plane depth; full normalized projective DLT; repeated-attempt probability; pentagon match counts and RANSAC budgets; regular-polygon symmetry.
- All parts of the five L3-assigned quiz sources accounted for, including the mixed-header near-duplicate retest; Fall 2025 Quiz 1 Q1–Q2 completed here as the secondary placement. Source assignment and subquestion rows retained in `quiz-index.csv`.
- Two new canonical numbered formula/application pairs, five original paired SVG/PDF diagrams with editable TikZ sources, short understanding checks, and complete source/formula/quiz/figure/errata/glossary/index updates.
- Exactly one seeded RANSAC sampling explorer, with native controls, reset/new-experiment actions, live substitutions, independent-status assumptions, prediction versus 200 simulated experiments, and a full static table/figure/explanation in print and without JavaScript.

## Validation completed

- `scripts/check_lecture03_math.py`: passed FOV/unit conversion, ray/plane checks and coefficient-scale invariance, full normalized projective DLT/nullspace/reprojection/held-out center, exact enumeration of 12,650 raw and 600 valid four-pair samples with five correct sets, minimal integer confidence budgets, coin probabilities, and ten polygon symmetries.
- `scripts/check_lecture03_browser.py`: Chromium passed all seven chapter pages for loaded images and rendered equations; six numerical widget states; new seed/reset/keyboard; mobile overflow; JavaScript-disabled, blocked-script, and browser-print fallbacks. Both earlier widget kinds still initialize. Exactly one widget occurs in each completed chapter.
- `make all`: HTML and LaTeX warnings-as-errors builds passed; exported continuous manuscript compiled with XeLaTeX/latexmk and the index; the cumulative PDF has 111 pages. No unresolved references, multiply defined labels, missing glyphs, or overfull boxes found. Existing upstream font-size/FontAwesome ToUnicode warnings remain benign.
- Visually inspected the five vector figures, desktop/mobile explorer screenshots, and all 15 L3 PDF pages. Corrected overlapping diagram labels, a one-line formula-box continuation, and quiz pagination; inspected final affected pages.
- Portable ZIP verified for current manuscript/PDF bytes, all 28 manuscript figure occurrences resolving to bundled assets, all five new vector PDFs, and required Sphinx support. The exported manuscript itself was compiled using those local support/assets; Overleaf was not accessed.
- `git diff --check`: passed. Existing unrelated workspace changes preserved.

## Review locations

- Local web preview: `http://127.0.0.1:8765/lectures/lecture03/index.html` while the preview server runs.
- Cumulative print: `print/CS532_Textbook.pdf` (L3 PDF pages 78–92; printed pages 74–88).
- Continuous manuscript: `print/CS532_Textbook.tex`.
- Portable XeLaTeX bundle: `print/CS532_Textbook_Source.zip`; instructions in its README and `BUILDING.md`.
- Authoring evidence: `lecture03-audit.md`, `lecture03-formulas.csv`, `coverage.csv`, quiz/figure/errata registers.

The user approved L3 and requested L4; its current status is tracked separately. Lectures 5–6 remain outlines. No changes were pushed or published.

**Quiz-format update:** the cross-lecture workbook revision supersedes earlier descriptions of shortened quiz examples and shared retest answers. See `QUIZ_WORKBOOK_STATUS.md` for current problem-level coverage and validation. Main lecture explanations retain their existing review status.
