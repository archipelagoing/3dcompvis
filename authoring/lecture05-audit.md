# Lecture 5 slide audit

All 91 source PDF pages were extracted as text and visually inspected in complete contact sheets. The page-level ledger is `coverage.csv`; the reader-facing map is `book/lectures/lecture05/review.md`. PDF page numbers are one-based; printed labels agree where visible. Unnumbered early slides retain PDF positions.

| PDF pages | Destination | Disposition |
| --- | --- | --- |
| 1–2 | index.md | Title, outline, and credits recorded; no duplicate teaching. |
| 3–10 | features.md | All substantive concepts/formulas taught; progressive builds and repeated examples consolidated. |
| 11–33 | corners.md | All substantive concepts/formulas taught; progressive builds and repeated examples consolidated. |
| 34–60 | tracking.md | All substantive concepts/formulas taught; progressive builds and repeated examples consolidated. |
| 61–91 | descriptors.md | All substantive concepts/formulas taught; progressive builds and repeated examples consolidated. |

## Accuracy corrections

- Eigenvalue classification requires adequate response in both directions, not exactly equal eigenvalues. Two large derivative components can still give a rank-one tensor.
- Harris, weighted tensors and LK signs use explicit consistent conventions.
- ORB full pipelines have pyramid-based multiscale handling; a fixed steered descriptor alone does not. Primary ORB docs linked in text.
- BRISK long pairs estimate orientation; short pairs encode the descriptor. The slide 81 wording is qualified using the original paper/authors.
- A cross-image distance matrix is not generally symmetric or zero-diagonal.

## Selected examples

Mountain panorama (4–6), NASA Mars/SIFT (10), flat/edge/corner windows (11), complete Harris detection sequence (28–33), camera/object motion (36–37), aperture demonstrations (42–43,54–55), street-sign tracking (59), descriptor patterns (65,72,77), original confusion table (87) and matching-choice diagram (90). Other build slides contribute to the derivation rather than repeated screenshots.

## Scope and repetition

Earlier camera geometry, homogeneous algebra, epipolar constraints and generic RANSAC remain at their existing canonical teaching locations. The chapter links to those prerequisites. Original historical/booklet questions remain complete in the lecture workbook; main exposition links to them rather than reprinting their full solutions a second time. New TLDR questions are labeled original practice.
