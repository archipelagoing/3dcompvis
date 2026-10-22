(lec05-review)=
# Formula and source checklist

Use this as a map, then work the [original questions and full solutions](quiz-workbook.md). This checklist adds no second version of the lecture.

## Find a formula and its procedure

| Formula | Where to learn and apply it |
| --- | --- |
| {eq}`eq-lec05-patch-energy` — patch change and its local approximation | [Corners](corners.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec05-eigen` — tensor eigenvalues and directional change | [Corners](corners.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec05-harris` — Harris and Shi–Tomasi responses | [Corners](corners.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec05-binary` — binary tests, smoothing and Hamming distance | [Descriptors](descriptors.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec05-orientation` — orientation from intensity moments | [Descriptors](descriptors.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec05-ratio` — nearest-neighbor distance ratio | [Descriptors](descriptors.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec05-quality` — matching evaluation | [Descriptors](descriptors.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec05-lk` — brightness constancy and patch least squares | [Tracking](tracking.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec05-iteration` — iterative tracking and coarse-to-fine transfer | [Tracking](tracking.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec05-photometric` — exposure-normalized patch | [Tracking](tracking.md); the adjacent application box gives the steps and assumptions |

## Trace the lecture slides

| PDF pages | Teaching location | Covered material |
| --- | --- | --- |
| 3–10 | [Features](features.md) | Panorama, repeatable/salient/local features, Mars Rover matches |
| 11–33 | [Corners](corners.md) | Shifted SSD, Taylor expansion, weighted tensor, eigenvalues/ellipses, Harris and NMS |
| 34–60 | [Tracking](tracking.md) | KLT assumptions, aperture problem, least squares, iterative/pyramid tracking, drift and exposure |
| 61–83 | [Descriptors](descriptors.md) | BRIEF, FAST/ORB, BRISK; orientation, scale and smoothing qualifications |
| 84–91 | [Descriptors](descriptors.md) | Distance matrices, thresholds, nearest neighbors/ratio, confusion table/ROC, search |

Pages 1–2 supply title/outline metadata. Repeated pictures and derivation builds are consolidated into the listed explanations. The final TLDR tests this lecture's additions; the original workbook remains the source for complete historical questions.

## Quiz route

- {ref}`Trackable patches and the slanted-edge trap <quiz-13-q1>`.
- {ref}`Exposure changes and normalization <quiz-9-q1>`.
- {ref}`Harris numerical tensor/eigenvalue calculation <quiz-a2-q1>`.
- {ref}`Lucas–Kanade full matrix solve <quiz-a3-q1>`.

**Source qualifications:** ORB's full pyramid pipeline handles multiple scales; fixed-scale steering alone does not. BRISK uses long pairs for orientation and short pairs for descriptor bits. A cross-image distance matrix need not be symmetric. See the cited primary references in [descriptors](descriptors.md).

Detailed page-level dispositions and editable formula/figure inventories are in the repository's `authoring/coverage.csv`, `lecture05-audit.md`, and `lecture05-formulas.csv`.
