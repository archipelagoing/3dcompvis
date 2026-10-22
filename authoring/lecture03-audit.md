# Lecture 3 source audit and ownership

All 80 PDF pages of `wk3_cs532s26_ImageFormation+Homographies-1.pdf` were extracted and inspected visually in rendered contact sheets, including image-heavy material and mathematical displays. The title is unnumbered; visible printed labels match PDF pages 2–80. Page-level dispositions are in `coverage.csv`.

## Boundary decision

PDF pages 2–80 repeat Lecture 2 PDF pages 51–129 in order. Existing L1/L2 canonical explanations retain ownership: projection and camera motion (L1); transformation families (L1), homographies/court rectification, warping/bilinear sampling, DLT/normalization, RANSAC/LMedS/adaptive scoring, radial distortion, epipolar/F/rectification introductions (L2). The public review table records navigation. Credits preserved: John Oliensis (2), Steve Seitz (23), R. Hartley/A. Zisserman/M. Pollefeys (33/46/56/62).

The camera-motion slide (12) and photographed court task (22) are already developed examples. Link to those existing treatments rather than duplicate pictures or tasks. The new numerical projective DLT application extends the earlier affine example. It documents independent centroid/mean-radius normalization, sample rows, full right null vector, reshape/denormalization, corner and held-out center checks. No existing general derivation was copied.

## New chapter work

- Calibration/FOV: all Spring 2019 Quiz 2 P1–P4 parts; Spring 2020 Quiz 3 retained as near-duplicate retest. Full K needs square-pixel/zero-skew/center assumptions. P3 answers compactly reference L1. P4 requires separating pixel principal point from physical virtual-plane 3D coordinates.
- Spring 2020 Quiz 2 P1–P2: scene/image Euclidean 3D vectors share a ray, so cross product is zero. Distinguished from homogeneous 2D joining-line notation.
- Filename 2015 Quiz 9, printed Spring 2019: symbolic ray–plane depth, original numeric companion, parallel/contained/center/behind-camera cases, axial depth versus range and unit assumptions.
- Fall 2025 Quiz 1 Q1–Q2: three independent wins and seven independent attempts. Geometry parts remain L1.
- Spring 2019 Quiz 3 P1 all four bullets: 25 pairs, five correct, 20% inlier fraction, explicit 99% choice, independent approximation and exact finite-pool/valid-sample alternatives. Regular versus equilateral wording qualified. Ten dihedral alignments; five if orientation evidence rules out reflections. Extra trials cannot resolve missing identities.

## Presentation

Eight numbered worked examples, two new canonical formula/application pairs, five original paired SVG/PDF diagrams with editable TikZ sources, short understanding checks, final TLDR/eight original questions with explained answers. One local accessible RANSAC explorer uses independent match statuses and seeded repeats; it compares prediction, one experiment, and 200 experiments. The finite-pool distinctions are explicitly outside the widget model. This probability concept is clearer in a sampling display than an unrelated 3D scene. Static table/curve/explanation carry the full point into PDF and no-JavaScript reading.

Numerical verification is reproducible in `scripts/check_lecture03_math.py`; it includes exhaustive enumeration of all 12,650 raw four-pair sets, 600 valid sets and five clean sets, minimal integer budgets, and DLT nullspace/held-out checks. Browser verification is in `scripts/check_lecture03_browser.py`. Build and final inspection results are recorded in `LECTURE03_STATUS.md` after execution. User review remains pending. Later lectures remain outlines; nothing published.
