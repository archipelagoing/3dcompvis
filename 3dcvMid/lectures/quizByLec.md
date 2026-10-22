
# CS 532 — Quizzes Organized by Lecture

All **20 quizzes** are organized by their **primary lecture match**, rather than overall relevance ranking. Secondary overlaps are noted where applicable.

**Relevance scale:** A = highest relevance; B = strong relevance; C = partial relevance; D = outside the six-lecture scope. Scores are from the original rubric.

## Lecture 1 — Foundations and 3D Geometry

| Quiz | Score | What it tests | Also relevant |
|---|---:|---|---|
| Fall 2025 Quiz 1 | 69 C | Camera-relative poses, 3D plane construction, coordinate transformations, probability | L3, L4 |
| Fall 2017 Quiz 9 | 55 C | Depth maps to 3D points, surface normals, rotation of 3D vectors | L4 |

**Study note:** These are supplementary rather than high-priority practice quizzes.

## Lecture 2 — Projective Geometry and Linear Algebra

| Quiz | Score | What it tests | Also relevant |
|---|---:|---|---|
| Spring 2020 Quiz 1 | 96 A | Homogeneous coordinates, point collinearity, cross products, 2D lines and intersections, projection matrices | L1 |

**Coverage gap:** No quiz directly tests the more advanced rotation representations, quaternions, and transformation hierarchies emphasized in Lecture 2.

## Lecture 3 — Camera Projection, Homographies, and RANSAC

| Quiz | Score | What it tests | Also relevant |
|---|---:|---|---|
| Spring 2019 Quiz 3 | 97 A | Homography, feature correspondences, inlier rates, RANSAC iterations | L2 |
| Spring 2019 Quiz 2 | 93 A | Camera intrinsics, focal length, calibration matrix, homogeneous projections | L1, L2 |
| Spring 2020 Quiz 3 | 93 A | Camera calibration, focal length, projection matrices | L1, L2 |
| Spring 2020 Quiz 2 | 90 A | Pinhole camera model, perspective projection, cross products | L1, L2 |
| 2015 Quiz 9 | 88 B | Viewing-ray and plane intersection, camera projection | L1 |

**Near-duplicates:** Spring 2019 Quiz 2 and Spring 2020 Quiz 3.

**Coverage gap:** Numerical DLT construction, SVD, normalized homography estimation, and image warping.

## Lecture 4 — Two-View Geometry and Stereo

**Most quiz coverage**

| Quiz | Score | What it tests |
|---|---:|---|
| 2015 Quiz 4 | 100 A | Fundamental matrix, epipolar line and constraint |
| Spring 2019 Quiz 4 | 100 A | Fundamental matrix, epipolar line and constraint |
| Fall 2025 Quiz 2 | 99 A | Three-view epipolar geometry, intersections of epipolar lines |
| Fall 2025 Quiz 3 | 98 A | Stereo disparity, depth estimation error, disparity search limits |
| Spring 2019 Quiz 5 | 98 A | Depth error from underestimating or overestimating disparity |
| Spring 2020 Quiz 5 | 98 A | Same disparity/depth questions |

**Duplicate pairs:** 2015 Quiz 4 ≈ Spring 2019 Quiz 4; Spring 2019 Quiz 5 ≈ Spring 2020 Quiz 5.

**Coverage gap:** Essential matrix decomposition, normalized eight-point algorithm, triangulation, and stereo matching cost functions.

## Lecture 5 — Corners and Feature Tracking

| Quiz | Score | What it tests |
|---|---:|---|
| Fall 2025 Quiz 4 | 95 A | Brightness constancy, KLT tracking, robustness to exposure changes |
| Spring 2019 Quiz 6 | 91 A | Trackable points, corners versus edges, image gradients and aperture ambiguity |

**Coverage gap:** Numerical Harris calculations, second-moment eigenvalues, Lucas–Kanade normal equations, feature descriptors, and matching metrics.

## Lecture 6 — Structure from Motion

| Quiz | Score | What it tests |
|---|---:|---|
| Fall 2025 Quiz 5 | 92 A | Projective/affine/metric reconstruction ambiguity, geometric constraints, sequential versus factorization SfM |
| Fall 2025 Quiz 6 | 76 B | Large-scale SfM pipelines, incremental versus hierarchical approaches, robust geometric verification |

**Coverage gap:** Factorization via SVD, triangulation, reprojection error, bundle adjustment, Gauss–Newton, and Levenberg–Marquardt.

## Outside Lectures 1–6

| Quiz | Score | What it tests |
|---|---:|---|
| Fall 2025 Quiz 7 | 22 D | ICP and point-cloud registration |
| Fall 2025 Quiz 8 | 5 D | Mesh topology, half-edge structures |
