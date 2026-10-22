# Lecture 6 slide audit

All 72 source PDF pages were extracted as text and visually inspected in complete contact sheets. The page-level ledger is `coverage.csv`; the reader-facing map is `book/lectures/lecture06/review.md`. PDF page numbers are one-based; printed labels agree where visible. Unnumbered early slides retain PDF positions.

| PDF pages | Destination | Disposition |
| --- | --- | --- |
| 1–3 | index.md | Title, outline, and credits recorded; no duplicate teaching. |
| 4–19 | ambiguity.md | All substantive concepts/formulas taught; progressive builds and repeated examples consolidated. |
| 20–38 | factorization.md | All substantive concepts/formulas taught; progressive builds and repeated examples consolidated. |
| 39–47 | pipeline.md | All substantive concepts/formulas taught; progressive builds and repeated examples consolidated. |
| 48–52 | triangulation.md | All substantive concepts/formulas taught; progressive builds and repeated examples consolidated. |
| 53–55 | pipeline.md | All substantive concepts/formulas taught; progressive builds and repeated examples consolidated. |
| 56–72 | optimization.md | All substantive concepts/formulas taught; progressive builds and repeated examples consolidated. |

## Accuracy corrections

- Parameter counts are necessary, not sufficient; calibrated gauge removes seven freedoms.
- Affine centered rank is at most three; generic rank three is not guaranteed. A missing measurement is not a zero.
- Metric-upgrade constraints use a symmetric positive definite L=CC^T with six independent entries, with stated unit-scale orthographic assumptions.
- Canonical projective camera blocks are not physical rotations.
- Algebraic triangulation is distinguished from geometric reprojection minimization and optimal corrected-image points. The sixth-degree equation is explained at the depth supplied by the slides, without inventing coefficients.
- Five-point relative pose and P3P have distinct inputs and multiple hypotheses.
- Residual/Jacobian signs, left pose increments, units, damping, gauge and sparse block assumptions are explicit.
- Slides 57/59 repeat the BA definition; slide 72 software links are optional examples.

## Selected examples

Facade tracks (5), projective/affine/similarity house reconstructions (15,17,19), Tomasi–Kanade house sequence (38), visibility matrix (45), complete booklet factorization/triangulation/GN questions, an original full 6×3 metric upgrade and 2-variable GN matrix solve. One local 3D point-refinement interactive shows the math geometrically, with a full static counterpart.

## Scope and repetition

Earlier camera geometry, homogeneous algebra, epipolar constraints and generic RANSAC remain at their existing canonical teaching locations. The chapter links to those prerequisites. Original historical/booklet questions remain complete in the lecture workbook; main exposition links to them rather than reprinting their full solutions a second time. New TLDR questions are labeled original practice.
