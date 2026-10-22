```{raw} latex
\clearpage
```

(lec04-tldr)=
# TLDR

**Lecture 4 in one sentence:** estimate valid two-view geometry, choose a camera pose that sees the scene, and turn reliable stereo matches into depths with honest error estimates.

## The important things

1. **Keep points, lines, and scalars distinct.** The assigned quizzes apply the existing epipolar rules to symbolic expansion and third-view prediction. Two lines in a third image can locate a point, unless their intersection is degenerate. See [quiz practice](epipolar-practice.md).
2. **Check rank before trusting “F.”** Fall 2025 Quiz 2 supplies a rank-three matrix. Its bilinear equation can be solved, but it is not valid pinhole-camera geometry. A noisy estimate requires a rank-two correction and pixel-space residual checks. See [estimation](estimation.md).
3. **Calibration supplies an essential matrix.** $E=K'^TFK=[t]_\times R$ has equal nonzero singular values and one zero. It recovers translation direction, not metric scale. Numerical conditioning transforms and camera calibration are different operations. See [essential geometry](essential.md).
4. **Test all four poses.** Two rotations and two translation signs produce four candidates. Positive reconstructed depths in both cameras select the visible configuration for suitable nondegenerate data. Translation $t$ is not the second camera center.
5. **Disparity is inverse depth.** In the specified rectified convention, $Z=fb/d$. Use focal length and disparity in pixels, baseline and depth in one length unit. Account for unequal principal-point columns. See [stereo](stereo.md).
6. **A one-pixel depth error is not symmetric.** Underestimating disparity pushes the point farther by more than an equal overestimate pulls it nearer. Use the exact error when the disparity error is a substantial fraction of disparity. Small disparities are especially fragile.
7. **Appearance chooses among geometric candidates.** Dense stereo generates hypotheses, evaluates costs, aggregates support, and selects or rejects. Minimize SAD/SSD; maximize NCC. Flat patches, repetitions, and occlusions can defeat a low-cost match. See [matching](matching.md).
8. **Support has assumptions.** A constant-disparity window favors fronto-parallel surfaces; large windows can mix depths. Shifted, elongated, weighted, or oriented-plane support can help. Rank retains a count; Census retains the ordered relative-intensity pattern. None removes ambiguity automatically.

```{raw} latex
\newpage
```

## Short quiz

These original questions test this chapter's additions.

1. For $x_A=(0,1,1)^T$, $x_B=(1,0,1)^T$, expand $x_B^TFx_A$ in matrix entries.
2. Two predicted lines in image C are proportional. Does their cross product give a unique finite correspondence?
3. A noisy matrix has singular values $(4,2,0.2)$. What singular values do rank-two F correction and essential-form correction use?
4. A candidate pose reconstructs a point with depths $+5$ and $-5$ in the two cameras. Is that point a valid visible correspondence under that pose?
5. Rectified cameras have $b=0.2\,\mathrm m$, $f=600$ pixels, $d=30$ pixels. What is the depth? If measured disparity becomes 31, is the point reconstructed nearer or farther?
6. For that setup, which disparity interval corresponds to depths from 2 to 6 meters?
7. Which direction do you optimize SAD and NCC? Can a constant-intensity patch supply a defined zero-mean NCC score?
8. With center intensity 10 and ordered neighbors $(8,12,7,11)$, what are the Census string and rank under the strict darker-than-center convention?

## Answers

```{admonition} Show answers and short explanations
:class: dropdown

1. **$f_{12}+f_{13}+f_{32}+f_{33}=0$.** The right vector selects columns 2 and 3; the left vector selects rows 1 and 3.
2. **No.** Proportional line vectors describe the same line. Their cross product is zero, so a unique point is undetermined.
3. **F: $(4,2,0)$; E: $(3,3,0)$.** E additionally requires its first two singular values to agree.
4. **No.** The point is behind the second camera. Positive depth is required in both observing cameras.
5. **4 meters; nearer.** The perturbed estimate is $120/31\approx3.871\,\mathrm m$, giving signed error $-4/31\approx-0.129\,\mathrm m$.
6. **$[20,60]$ pixels.** The far endpoint gives $120/6$; the near endpoint gives $120/2$.
7. **Minimize SAD, maximize NCC; no.** A flat patch has zero centered norm, making NCC's denominator zero.
8. **1010; rank 2.** Neighbors 1 and 3 are darker. Census keeps their positions, while rank keeps only their count.
```
