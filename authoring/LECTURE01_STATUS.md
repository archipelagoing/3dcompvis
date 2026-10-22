# Lecture 1 review status

**Reviewed with the user.** The requested final TLDR/quiz was added, and the user authorized Lecture 2.

## Delivered

- A chapter introduction and ten ordered topic/review sections, covering the actual Lecture 1 deck rather than the earlier provisional outline.
- Nineteen numbered worked examples, eight short understanding checks, and one end-of-chapter transfer exercise, with explained solutions in both editions.
- Twenty-five canonical formula boxes with application procedures and 26 labeled equations including the relative-pose worked specialization.
- A final TLDR with eight key rules and eight original quiz questions, with concise answers collapsible online and included in print.
- Seventeen chapter figures: fourteen original vector diagrams and three source-supplied image assets, including the foundation quiz diagram relocated from Lecture 2. Editable diagram sources and credits are retained.
- Integrated Fall 2025 Quiz 1 Q3–Q4 and Fall 2017 Quiz 9 P2(a–b), plus a supplementary solution of the latter's depth-map problem P1. Fall 2025 probability Q1–Q2 remains assigned to Lecture 3.
- Updated source-page coverage, formula/quiz registers, keyword glossary/index, formula reference, source credits, and verified errata/convention notes.

## Review locations

- Web: `book/_build/html/lectures/lecture01/index.html` (local preview at `http://127.0.0.1:8765/lectures/lecture01/index.html` while the preview server runs).
- Print: `print/CS532_Textbook.pdf` — cumulative edition, with Lecture 1 and clearly labeled later outlines.
- Source: `print/CS532_Textbook.tex` and `print/CS532_Textbook_Source.zip`.
- Audit: `lecture01-audit.md`, `lecture01-formulas.csv`, and `coverage.csv`.

## Checks performed

- Independently checked intersections, dual transforms, plane nullspaces/cofactors, skew-line distance, rotation order, the expanded Euler matrix, quaternion conventions, frame composition, tetrahedron normals, projection, camera-motion branches, and common-frame backprojection. The numerical checker passed.
- HTML and LaTeX export passed with Sphinx warnings treated as errors. XeLaTeX/latexmk generated the cumulative PDF and index; final logs contain no unresolved references, undefined commands, missing mathematical characters, or overfull boxes.
- Inspected all twelve original diagrams as rendered figures and selected typeset PDF pages, including dense quaternion formulas and quiz geometry.
- Headless Chromium checked all nine chapter pages: equations render without MathJax error nodes and every article image loads. Verified mobile page width and reviewed desktop/mobile screenshots.
- Fixed an inherited optional MathJax loader patch that loaded the engine repeatedly. The local extension also deduplicates repeated inline extension declarations. Confirmed a single engine loader and one copy of the checked global declaration.
- The source bundle includes the referenced local assets and LaTeX support. A standalone compile in a separate temporary directory is recorded in the final task result.

## Deliberate limits

Source preview equations for epipolar geometry/stereo remain assigned to Lecture 4. Circular points and the absolute conic are defined as vocabulary previews, with their reconstruction role reserved for Lecture 6. Full calibration and depth-fusion algorithms remain later material. The source-image creators not identified by the deck are not invented in the credits.

The PDF is generated from MyST through Sphinx and contains its typesetting macros; the bundle includes the support files needed for ordinary XeLaTeX compilation. Overleaf itself was not accessed. No changes were pushed or published; the live site remains unchanged.

Please review pacing, explanatory depth, formula/application formatting, figure size, and the source-caption detail before expanding the remaining lectures.

Spring 2020 Quiz 1 foundation solutions were relocated here under the user's later unique-content requirement. The original Lecture 2 quiz assignment and stable legacy labels are preserved. See `lecture01-02-overlap-audit.md`.

## Interactive addition

Exactly one interactive explorer is placed at the relevant teaching point: camera motion/projection after Example 1.15. The same MyST content supplies complete static explanation and results for print and no-JavaScript readers. See `INTERACTIVES.md` for the remaining lecture plan and validation.

The projection explorer now uses an actual WebGL 3D scene with orbit/zoom, draggable point, point/camera/focal/yaw controls, linked pixel view and world→camera→pixel calculation cards. Its static 3D scene diagram and physical-plane-to-pixel calculation are retained in print. One widget remains.

**Quiz-format update:** the cross-lecture workbook revision supersedes earlier descriptions of shortened quiz examples and shared retest answers. See `QUIZ_WORKBOOK_STATUS.md` for current problem-level coverage and validation. Main lecture explanations retain their existing review status.
