# CS 532 — Exam Study TODO (Lectures 1–6)

**Scope:** 18 relevant quiz PDFs (ranks 1–18 in the previous relevance rubric), **excluding** Fall 2025 Quiz 7 (ICP) and Quiz 8 (mesh topology). Includes duplicate PDFs intentionally. Scores below indicate slide relevance, **not actual test probabilities**. Use the companion `CS532_18_Quizzes_Step_by_Step.tex` (and compiled PDF) for concise, red, numbered solutions.

## 1. First: Lecture 3–4 mathematics — high priority

- [ ] **#1 — 100/100 · `cs532f15_quiz4.pdf`** — Fundamental matrix → epipolar line; expand epipolar constraint (PDF itself says *Spring 2019 Quiz 4*).
- [ ] **#2 — 100/100 · `cs532s19_quiz4.pdf`** — **Exact duplicate of #1**; use as an independent closed-notes retest.
- [ ] **#3 — 99/100 · `cs532f25_quiz_2_solution.pdf`** — Intersect two epipolar lines; use a given F and x′ to find a valid x. **Erratum:** `x′ᵀF` is line coefficients, not a point.
- [ ] **#4 — 98/100 · `cs532f25_quiz_3_solution.pdf`** — Stereo depth vs disparity; exact versus first-order depth error; depth-search bounds.
- [ ] **#5 — 98/100 · `cs532s19_quiz5-2.pdf`** — ±1-pixel disparity error, exact arithmetic, error dependence on disparity.
- [ ] **#6 — 98/100 · `cs532s20_quiz5.pdf`** — **Exact duplicate of #5**; retest later without notes.
- [ ] **#7 — 97/100 · `cs532s19-quiz3.pdf`** — Exhaustive polygon-corner matches; inlier ratio; homography RANSAC sample count; regular-polygon ambiguity.

## 2. Next: foundations, cameras, feature tracking — high priority

- [ ] **#8 — 96/100 · `cs532s20_quiz1.pdf`** — Homogeneous point/line cross products; projective intersections; 3×4 camera projection matrix.
- [ ] **#9 — 95/100 · `cs532f25_quiz_4_solution.pdf`** — Exposure changes, brightness constancy, robust KLT patch normalization.
- [ ] **#10 — 93/100 · `cs532s19_quiz2-2.pdf`** — Horizontal FOV to focal length, K matrix, matrix dimensions, homogeneous scaling, principal point.
- [ ] **#11 — 93/100 · `cs532s20_quiz3.pdf`** — **Near-exact duplicate of #10** (PDF header contains mixed 2019/2020 labeling); retest.
- [ ] **#13 — 91/100 · `cs532s19_quiz6-2.pdf`** — Corners vs edges vs isolated pixels, structure tensor and tracking solvability.
- [ ] **#14 — 90/100 · `cs532s20_quiz2.pdf`** — Pinhole-ray/plane intersection and a zero cross product.

## 3. Then: Structure from Motion, transfer questions

- [ ] **#12 — 92/100 · `cs532f25_quiz_5_solution-1.pdf`** — Projective→affine/metric upgrades; facade versus tiled floor; sequential vs global factorization. **Caution:** global metric upgrade from one known planar grid requires additional assumptions.
- [ ] **#15 — 88/100 · `cs532f15_quiz9.pdf`** — Ray–plane intersection and depth formula (PDF header says *Spring 2019 Quiz 9*).
- [ ] **#16 — 76/100 · `cs532f25_quiz_6_solution.pdf`** — SfM architecture for weak overlaps; RANSAC contamination checks; advanced application of L6.
- [ ] **#17 — 69/100 · `cs532f25_quiz_1_solution.pdf`** — Binomial complement probability; relative poses through a shared object; 3D plane normal.
- [ ] **#18 — 55/100 · `cs532_f17_quiz9.pdf`** — Backproject depthmaps into a common frame; tetrahedral face normals and rotations. Parts extend beyond the emphasis of L1–6.

## 4. Important gaps NOT adequately covered by the quiz set

- [ ] **L3 slides 34–45: homography DLT + SVD** — Derive two linear equations per correspondence; assemble 2n×9 matrix; recover H; normalized DLT.
- [ ] **L5 slides 11–30: Harris numerics** — Compute gradient sums, M, eigenvalues, determinant, trace, response R, non-max suppression.
- [ ] **L5 slides 39–50: Lucas–Kanade numerics** — Taylor linearization, A, b, AᵀA, least-squares displacement; aperture problem.
- [ ] **L4 slides 22–41: essential matrix** — E = K′ᵀ F K, singular values, 4 candidate poses, positive-depth cheirality.
- [ ] **L6 slides 48–52: triangulation** — Build AX = 0 from P, P′ and image matches; nullspace via SVD.
- [ ] **L6 slides 46, 62–70: bundle adjustment** — Reprojection residual, Jacobian, Gauss–Newton/LM objective and updates.
- [ ] **L6 slides 25–37: affine SfM factorization** — Center measurement matrix, rank 3 factorization, affine/metric ambiguity.

## 5. Exam readiness check

- [ ] Re-solve #1, #3, #4, #7, #8, #9, #12 without the red solutions.
- [ ] Be able to derive, not merely recall: `x′ᵀFx=0`, `Z=fb/d`, `N=ln(1-p)/ln(1-(1-e)^s)`, `x ~ PX`, `R=det(M)-k tr(M)²`.
- [ ] Write the assumptions next to each solution (calibration, rectification, nonzero disparity, independence, nondegenerate sample, nonzero gradient variance).
- [ ] Practice one **new** problem per gap topic above.
- [ ] On the exam, check coordinate units (px vs cm/m), homogeneous-scale ambiguity, valid transforms, and whether an approximation or exact value was requested.

**Source naming note:** The file names `cs532f15_quiz4.pdf` and `cs532f15_quiz9.pdf` imply 2015, but their displayed quiz headers say Spring 2019. The study guide retains both original filenames and the printed quiz wording.
