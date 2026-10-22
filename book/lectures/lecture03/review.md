(lec03-review)=
# Review and source checklist

This chapter adds applications to the theory already taught. Use this checklist to find the right calculation without reading repeated explanations.

## New formula boxes

| Task | Canonical formula and application |
| --- | --- |
| Turn centered horizontal FOV into pixel focal length | {eq}`eq-lec03-fov`, [calibration](calibration.md) |
| Intersect a calibrated ray with a known plane | {eq}`eq-lec03-ray-plane`, [ray–plane depth](ray-plane.md) |

For DLT rows, coordinate normalization, and RANSAC's trial budget, use the original [Lecture 2 boxes](../lecture02/estimation.md). This chapter's projective numerical example and sampling cases apply those formulas to new data.

## Worked examples and quiz coverage

| Example | Skill | Source |
| --- | --- | --- |
| {ref}`3.1 <ex-lec03-calibration>` | FOV and calibration matrix | Spring 2019 Quiz 2 P1–P2; Spring 2020 Quiz 3 retest |
| {ref}`3.2 <ex-lec03-principal>` | Dimensions, homogeneous scale, physical principal point | Same quizzes P3–P4; foundation dimensions linked to L1 |
| {ref}`3.3 <ex-lec03-ray>` | Image-plane intersection and Euclidean cross product | Spring 2020 Quiz 2 P1–P2 |
| {ref}`3.4 <ex-lec03-plane>` | Ray–plane depth and visibility | Printed Spring 2019 Quiz 9 P1; original numerical companion |
| {ref}`3.5 <ex-lec03-dlt>` | Full normalized projective DLT and held-out check | Original companion to slides 34–45 |
| {ref}`3.6 <ex-lec03-probability>` | Independent events and repeated attempts | Fall 2025 Quiz 1 Q1–Q2 |
| {ref}`3.7 <ex-lec03-pentagon>` | Candidate counts, inliers, trial budget | Spring 2019 Quiz 3 P1 bullets 1–3 |
| {ref}`3.8 <ex-lec03-symmetry>` | Indistinguishable regular-polygon alignments | Same quiz P1 bullet 4 |

## Repeated slide material: where it lives

The entire 80-page deck was checked, including diagrams and formulas. Page 1 is the title; pages 2–80 repeat Lecture 2's PDF pages 51–129.

| Lecture 3 PDF pages | Teaching location |
| --- | --- |
| 2–12: image formation and camera motion | [Lecture 1 cameras](../lecture01/cameras.md), including the camera-motion slide exercise |
| 13–22: homographies and transformation hierarchy | [Lecture 1 transformations](../lecture01/transformations.md), [Lecture 2 homographies and court task](../lecture02/homographies.md) |
| 23–32: forward/inverse warping and interpolation | [Lecture 2 warping](../lecture02/warping.md) |
| 33–45: estimation, DLT, normalization | [Lecture 2 estimation](../lecture02/estimation.md), plus the [new numerical walkthrough](homography-practice.md) |
| 46–55: RANSAC, consensus, matching pipeline | [Lecture 2 estimation](../lecture02/estimation.md), plus the [new quiz applications](probability-ransac.md) |
| 56–80: radial distortion, epipolar geometry, fundamental matrix, rectification | [Lecture 2 distortion and two-view introduction](../lecture02/two-view.md); later two-view problems belong to Lecture 4 |

## Check before handing in a solution

- **Coordinates:** are these pixels, physical image-plane coordinates, normalized rays, or homogeneous points?
- **Assumptions:** did you supply square pixels and a centered principal point before writing the full $K$?
- **Depth:** does the intersection satisfy both the plane and the image ray, with $Z>0$?
- **DLT:** did you use the full right-vector basis and undo both normalizations?
- **Probability:** what does one counted trial sample, and what event does the confidence describe?

Continue to the final [TLDR and short quiz](tldr.md).
