(lec06-review)=
# Formula and source checklist

Use this as a map, then work the [original questions and full solutions](quiz-workbook.md). This checklist adds no second version of the lecture.

## Find a formula and its procedure

| Formula | Where to learn and apply it |
| --- | --- |
| {eq}`eq-lec06-counts` — necessary measurement counts | [Ambiguity](ambiguity.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec06-gauge` — projective reconstruction ambiguity | [Ambiguity](ambiguity.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec06-affine` — affine measurements and centering | [Factorization](factorization.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec06-factorization` — rank-three affine factorization | [Factorization](factorization.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec06-metric` — orthographic metric upgrade | [Factorization](factorization.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec06-ba` — weighted reprojection least squares | [Optimization](optimization.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec06-jacobian` — projection and pose Jacobian blocks | [Optimization](optimization.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec06-updates` — gradient, Newton, Gauss–Newton, and damping | [Optimization](optimization.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec06-schur` — eliminate point updates with the Schur complement | [Optimization](optimization.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec06-canonical` — one canonical camera pair from a fundamental matrix | [Pipeline](pipeline.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec06-triangulation` — linear homogeneous triangulation | [Triangulation](triangulation.md); the adjacent application box gives the steps and assumptions |
| {eq}`eq-lec06-geometric` — geometric triangulation objectives | [Triangulation](triangulation.md); the adjacent application box gives the steps and assumptions |

## Trace the lecture slides

| PDF pages | Teaching location | Covered material |
| --- | --- | --- |
| 4–19 | [Ambiguity](ambiguity.md) | Unknowns, necessary counts, gauge, projective/affine/similarity ambiguity and house examples |
| 20–38 | [Factorization](factorization.md) | Affine/orthographic cameras, centering, SVD, rank at most three, metric upgrade and house sequence |
| 39–47 | [Pipeline](pipeline.md) | Perspective count, canonical cameras from F, sequential SfM, visibility, self-calibration |
| 48–52 | [Triangulation](triangulation.md) | Linear system/SVD, noisy rays, geometric objectives and sixth-degree candidate equation |
| 53–55 | [Pipeline](pipeline.md) | Calibrated five-point versus P3P, multiple solutions and verification |
| 56–72 | [Optimization](optimization.md) | Reprojection least squares, gradient/Newton/GN/LM, Jacobians, gauge and sparse elimination |

Pages 1–3 supply title/credits; repeated section titles and the duplicated BA definition on pages 57/59 are consolidated. Page 72's software examples are acknowledged in the optimization discussion rather than reproduced as installation instructions.

## Quiz route

- {ref}`Facade and floor reconstruction constraints <quiz-12-q1>`, {ref}`second scenario <quiz-12-q2>`, and {ref}`pipeline choice <quiz-12-q3>`.
- {ref}`Weak overlaps <quiz-16-q1>` and {ref}`contaminated matches <quiz-16-q2>`.
- {ref}`Linear triangulation with full matrices <quiz-a5-q1>`.
- {ref}`Numerical Gauss–Newton reprojection update <quiz-a6-q1>`.
- {ref}`Centered measurement matrix and factorization <quiz-a7-q1>`.

**Source qualifications:** rank is at most three, with equality requiring nondegeneracy. Parameter counts alone do not establish uniqueness. A projective camera block is not a rotation. Metric upgrade requires enough independent constraints and a valid positive metric. Linear triangulation optimizes algebraic error; the geometric objective is different.

Detailed page-level dispositions and editable formula/figure inventories are in the repository's `authoring/coverage.csv`, `lecture06-audit.md`, and `lecture06-formulas.csv`.
