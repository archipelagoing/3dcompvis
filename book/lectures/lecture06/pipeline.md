(lec06-pipeline)=
# Grow a reconstruction one view at a time

**Structure from motion (SfM)** estimates both the scene and the cameras. Lecture 5 supplies tracks; Lecture 4 supplies two-view geometry. This section joins those pieces into a reconstruction.

**Source:** PDF pages 39–47 and 53–55. Exam companion: {ref}`weak overlap and hierarchical reconstruction <quiz-16-q1>`.

```{figure} ../../images/lecture06/sfm-pipeline.*
:name: fig-lec06-pipeline
:width: 95%
:alt: Verified tracks initialize a pair, then camera registration, triangulation, and bundle adjustment repeat.

Original reconstruction loop based on PDF pages 43–46. New cameras need links to existing structure; bundle adjustment revisits earlier estimates.
```

## Start with a reliable pair

Use robust matches, a useful baseline, and enough shared nondegenerate structure. A nearly pure rotation can support image alignment while providing little or no depth information. A large baseline can improve triangulation but make matching harder.

For calibrated cameras, estimate an essential matrix and recover a relative rotation and translation direction, testing cheirality as in Lecture 4. Without calibration, a fundamental matrix initializes a **projective** reconstruction.

````{formula-box} Formula — one canonical camera pair from a fundamental matrix
```{math}
:label: eq-lec06-canonical
F^Te'=0,\quad P=[I\mid0],\quad
P'=[-[e']_\times F\mid e'].
```

$F$ has rank two, $e'\ne0$ is the second-image epipole, and $[e']_\times$ is its cross-product matrix. This produces cameras consistent with $F$ up to scale and projective gauge. The left $3\times3$ block of $P'$ is generally **not a physical rotation**. This is a projective construction, not calibrated pose extraction.
````

```{application} Initialize an uncalibrated pair
1. Robustly estimate a rank-two $F$ with a consistent image-order convention.
2. Find a nonzero vector in the nullspace of $F^T$.
3. Build the two camera matrices above and triangulate shared tracks.
4. Keep the result labeled projective until justified upgrade constraints are available.
```

**Why is this consistent?** The pair induces $[e']_\times(-[e']_\times F)$. Since $[e']_\times^2=e'e'^T-\|e'\|^2I$ and $e'^TF=0$, the product is $\|e'\|^2F$, the same fundamental matrix up to scale.

## Add cameras, then add points

1. **Register a new camera** using already reconstructed 3D points and their 2D observations (**PnP** in the calibrated case).
2. **Triangulate new tracks** seen in sufficiently separated registered cameras.
3. **Check** reprojection error, cheirality, and track consistency. Remove outliers; do not keep a point merely because a solver returned it.
4. **Bundle-adjust** the current cameras and points, then continue. Revisit drift rather than assuming each early estimate is final.

```{figure} ../../images/lecture06/visibility.*
:name: fig-lec06-visibility
:width: 65%
:alt: The source visibility matrix marks which images observe which reconstructed points.

Source PDF page 45. Each marked observation connects one camera and one point. Empty entries are missing data, not zero-valued pixel measurements.
```

## Do not confuse the minimal pose problems

| Problem | Known data | Unknown | Minimal sample and ambiguity |
| --- | --- | --- | --- |
| Calibrated relative pose | Matched pixels in two calibrated views | Relative rotation and translation direction | Five correspondences; up to ten algebraic candidates in the general five-point solver |
| P3P | Three known 3D points and their calibrated image rays | One camera pose | Three correspondences; up to four real pose candidates |
| Practical robust registration | Many noisy matches, possibly with outliers | Reliable pose | RANSAC plus extra observations, cheirality, and reprojection scoring |

A sample can generate several hypotheses. More observations select and refine a valid one. These are different problems: two unknown views versus one camera looking at an existing 3D map.

## What if calibration is unknown?

**Self-calibration** uses constraints such as constant intrinsics across views, zero skew, known principal-point assumptions, or geometric information such as vanishing points. Sufficient independent constraints can upgrade a projective reconstruction toward metric geometry. Constant intrinsics alone is not a universal guarantee: critical camera motions and degenerate scenes can leave ambiguities.

For long sequences, local reconstructions or keyframes can be joined through shared tracks and refined together. Weak overlap makes merging fragile; a global solver cannot invent missing connectivity. The workbook explains the quiz's hierarchical strategy, including when it helps and what still needs overlap.

```{index} Structure from motion
```
```{index} P3P
```
```{index} Self-calibration
```
