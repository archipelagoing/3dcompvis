(lec01-review)=
# Review: choose the right geometric operation

The most useful formula is the one whose inputs, coordinate conventions, and assumptions match the problem. Before calculating, say what geometric object you have and what you want to recover.

## Formula and source checklist

The PDF-page ranges refer to `wk1_2_cs532s26_IntroToGeometry.pdf`. Equation links lead to the canonical formula boxes and application procedures.

| Topic / operation | Formula or explanation | Source PDF pages |
| --- | --- | --- |
| Motivation, reconstruction pipeline, ambiguity, application examples | {ref}`lec01-motivation` | 2–61 |
| Homogeneous scale, finite/ideal points | {ref}`lec01-projective` and {eq}`eq-homogeneous-scale` | 65–71 |
| Point–line incidence | {eq}`eq-lec01-incidence` | 65 |
| Joins and intersections | {eq}`eq-lec01-cross` | 67 |
| Parallel lines and infinity | {eq}`eq-lec01-ideal` | 68–71 |
| 2D rotation and pivot transforms | {eq}`eq-lec01-rotation2`, {eq}`eq-lec01-rigid2` | 72–77 |
| Transformation families and invariants | {eq}`eq-lec01-hierarchy` | 78, 103 |
| Point, line, and plane transforms | {eq}`eq-lec01-dual` | 79, 81–82 |
| Planes, distance, three-point construction | {eq}`eq-lec01-plane`, {eq}`eq-lec01-plane-points` | 82–84 |
| Point/plane nullspaces and cofactors | {eq}`eq-lec01-plane-null`, {eq}`eq-lec01-cofactor` | 83–85 |
| Plücker representation and line distances | {eq}`eq-lec01-plucker`, {eq}`eq-lec01-line-distance` | 86–87 |
| Axis rotations and inverse | {eq}`eq-lec01-rotation3`, {eq}`eq-lec01-orthogonal` | 88–90 |
| Ordered angles and fixed/body axes | {eq}`eq-lec01-ordered-angles` | 93–100 |
| Axis–angle and computational supplement | {eq}`eq-lec01-axis-angle`, {eq}`eq-lec01-rodrigues` | 91 |
| Quaternion operations and conventions | {eq}`eq-lec01-quaternion` | 92 |
| Rigid transforms and frame composition | {eq}`eq-lec01-rigid3`, {eq}`eq-lec01-compose` | 101–102 |
| Virtual-plane projection | {eq}`eq-lec01-pinhole` | 105–110 |
| Extrinsics, intrinsics, projection matrix | {eq}`eq-lec01-camera` | 111–113 |
| Camera-motion hands-on task | {ref}`Example 1.15 <ex-lec01-camera-motion>` | 114 |
| Depth-map backprojection: quiz extension | {eq}`eq-lec01-backproject` | Quiz, not a slide formula |

The epipolar constraint and disparity formula embedded in the workflow previews on PDF pages 25–26 are explicitly deferred to Lecture 4, where their variables and assumptions will be developed.

The administrative title, policies, logistics, and reading-list slides are recorded in the coverage ledger but do not become mathematical exercises. The rank/SVD and Rodrigues explanations fill explanatory steps needed to understand the lecture; they are identified as supplements where they go beyond its printed formulas.

## Rework the assigned quizzes without the solutions

| Source | Location | What to check |
| --- | --- | --- |
| Fall 2025 Quiz 1, Q3 | {ref}`Example 1.10 <ex-lec01-relative-pose>` | Frame path, inversion, shared object frame/scale/time |
| Fall 2025 Quiz 1, Q4 | {ref}`Example 1.11 <ex-lec01-object-plane>` | Camera centers in one frame; noncollinearity |
| Fall 2017 Quiz 9, P2(a) | {ref}`Example 1.12 <ex-lec01-tetrahedron>` | Cross products, orientation, unit normalization |
| Fall 2017 Quiz 9, P2(b) | {ref}`Example 1.13 <ex-lec01-rotated-normals>` | Declared active rotation; normals remain perpendicular |
| Fall 2017 Quiz 9, P1 | {ref}`Example 1.16 <ex-lec01-depth>` | Supplement: calibration, axial depth/range, common frame |

Fall 2025 Quiz 1, Q1–Q2, remains assigned to Lecture 3's RANSAC/probability explanation. The Spring 2020 homogeneous-geometry quiz remains in Lecture 2; use its questions later as a transfer test rather than counting them as newly introduced Lecture 1 quiz material.

## Common mistakes to catch before you calculate

- Dividing a homogeneous coordinate by zero or treating the zero vector as a point.
- Calling an image vanishing point an ideal image point without checking its coordinates.
- Rotating about the origin when a different pivot was specified.
- Applying the point matrix directly to line/plane coefficients.
- Inferring a unique plane from collinear points.
- Treating every length-preserving matrix as a proper rotation.
- Using ordered-angle names without declaring axes and multiplication order.
- Mixing active/passive quaternion sandwiches.
- Negating a translation without rotating it when inverting a rigid transform.
- Treating camera pose and world-to-camera extrinsics as identical arrays.
- Assuming image-plane length, pixel coordinates, axial depth, and range use interchangeable units.

## A short transfer problem

(ex-lec01-transfer)=
```{understanding-check} Exercise 1.1 — combine frames, planes, and projection
A world point is $X=(2,1,6)^T$. A camera has center $C=(1,0,2)^T$, identity orientation, $f_x=f_y=400$ pixels, zero skew, and principal point $(200,150)$.

1. Write the world-to-camera translation and camera coordinates of $X$.
2. Project $X$ to pixels.
3. Find a plane through the camera center, the world origin, and $X$.
4. State when the plane-construction step would fail.
```

```{admonition} Solution
:class: dropdown
1. $t=-C=(-1,0,-2)^T$, so $X_c=(1,1,4)^T$.
2. $u=200+400(1/4)=300$ and $v=150+400(1/4)=250$ pixels.
3. Use the world origin as anchor: $C\times X=(-2,-2,1)^T$. Thus $-2x-2y+z=0$. Both $C$ and $X$ satisfy it; the origin does too.
4. It fails to determine a unique plane if the origin, camera center, and point are collinear, or if repeated points remove an independent direction.
```

You are ready to move on when you can explain the geometry before choosing a formula, solve these examples without copying their steps, and state each answer's assumptions and degeneracies. Lecture 2 will revisit the projective and rotation language and extend it toward image transformations and estimation.
