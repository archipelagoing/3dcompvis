# Lecture 2 source audit and example selections

All 129 PDF pages of `cs532_f25_Week2.pdf` were read using extracted text and rendered contact sheets. Mathematical image slides on PDF pages 48, 49, and 109 were additionally inspected as individual larger images. The court photograph embedded on page 71 was extracted and inspected before use. The assigned Spring 2020 Quiz 1 was read in full.

## Labels and scope

Printed slide labels match PDF pages 1–43. Pages 44–49 have no visible printed label. From PDF page 50 onward the printed label equals PDF page plus one. Page references in the chapter are explicitly PDF pages; the coverage ledger retains the distinct printed labels.

| PDF pages | Disposition |
| --- | --- |
| 1–2 | Lecture identity and contributor credits; no student-facing repetition of logistics |
| 3–11 | Homogeneous geometry review, with canonical Lecture 1 references and Quiz P1/P3 applications |
| 12–19 | 2D rotation, pivot, hierarchy and dual transform review; linked to Lecture 1 |
| 20–27 | 3D points/planes, cofactors, incidence nullspaces and Plücker line/distance review; linked to full Lecture 1 formulas |
| 28–41, 50 | Elementary/ordered rotations, rigid transforms and hierarchy; repeated canonical formulas linked |
| 42–49 | Axis-angle/quaternion review and new conversions; corrected active convention and scalar extraction; compact SLERP companion explains slide interpolation claim |
| 51–61 | Camera introduction and motion exercise already solved in Lecture 1; linked and applied to Quiz P2 |
| 62–71 | Projectivity, planar mapping, transform hierarchy/invariants; court assignment developed as computed real-image example |
| 72–81 | Filtering versus warping, global coordinates, forward/inverse sampling and bilinear interpolation |
| 82–94 | Homography measurement count, cross-product DLT, rank/nullspace, noisy algebraic fit, homogeneous versus fixed-entry solve, normalization/denormalization |
| 95–104 | Outlier problem, RANSAC algorithm/probability/consensus/adaptation, LMedS contrast, matching and refinement pipeline, actual building-example counts |
| 105–110 | Lens images described, explicit radial correction model with consistent radius/direction, calibration ideas |
| 111–126 | Epipolar planes/lines/epipoles, three motion examples, F constraint/properties, camera-derived F, linear estimation and rank correction |
| 127–129 | Rectification goal, epipole transformation, practical limitations, paired-object result |

Repeated builds/section-title slides are consolidated. The page ledger records a destination for each page. No later lecture is marked authored because it shares material with this deck. Circular points/absolute conic remain the short Lecture 1 vocabulary preview; full reconstruction use remains Lecture 6. Full assigned homography/probability problems and noisy estimation extensions remain Lecture 3; assigned epipolar/stereo problems remain Lecture 4.

## Selected actual slide examples

- **Parallel lines/railway, PDF 7–11:** avoid reusing Lecture 1's duplicate railway image; use the assigned two-vertical-lines quiz and a new precise diagram.
- **Axis-angle and conversion, PDF 42–49:** cyclic-axis and half-turn original numerical companions expose sign conventions and a missing +1; compare against Rodrigues and recover the original matrix.
- **Court rectification assignment, PDF 71:** embed the actual supplied photograph, annotate four disclosed approximate corners, and compute a rectangular warp using normalized DLT and inverse bilinear resampling. Aspect ratio is illustrative, not claimed metric calibration. Raised objects and missing floor are explicitly discussed.
- **Pixel sampling, PDF 76–80:** redraw forward/inverse grids and solve a four-intensity interpolation example.
- **Robust line, PDF 96:** original consensus schematic; clearly distinguish its line model from four-match homography hypotheses.
- **Building robust match example, PDF 104:** interpret 268 putative matches, 151 consensus and 262 guided final matches. Distinguish reported iterations from the rounded theoretical budget.
- **Converging/parallel/forward cameras, PDF 118–120:** explain epipole location and draw a rectified special case with a numerical F example.

## Formula and quiz verification

`lecture02-formulas.csv` lists 16 canonical equations/boxes, each paired with an application procedure. All assigned Quiz 1 subquestions have individual register rows. Explanations qualify repeated-point degeneracy, projection denominators and the camera center, and the distinct-line requirement d>0.

`scripts/check_lecture02_math.py` verifies intersections/collinearity, quaternion conversions against independent Rodrigues matrices for random axes/angles, half-turn handling, interpolation, projective cross-ratio, bilinear weights, normalized DLT and held-out points, court corner reprojection, RANSAC counts, camera-derived F and constraints, and F coordinate-change formulas. Newly authored examples are labeled rather than attributed to the quiz.

`scripts/build_lecture02_figures.py` regenerates four original paired SVG/PDF diagrams and the court comparison from the retained source image. Source permissions/unknown individual image authorship are recorded without invention.


## Unique-content revision

The user requested unique teaching across chapters after reviewing the first draft. `lecture01-02-overlap-audit.md` records the comparison and final ownership. The foundation review table and entire geometry-quiz page were removed from Lecture 2. The distinct Spring 2020 Quiz 1 solutions were moved to Lecture 1, retaining original assignment metadata. The collinearity formula is now in Lecture 1's formula register; its legacy equation/example targets remain valid. Lecture 2's sixteen formula pairs now include the new directional-scale factorization instead of the relocated collinearity test.

The repeated 2D/3D hierarchy table/explanation, quaternion definition/sign-equivalence explanation, basic quarter-turn example, and foundational TLDR/quiz questions were removed or replaced. New quaternion conversion practice uses a 120-degree cyclic-axis rotation. The new affine factorization on PDF page 68 is retained, because Lecture 1 does not teach it. No substantive source topic is lost by consolidating repeated slides.
