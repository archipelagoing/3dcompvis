(lec02-tldr)=
# TLDR

**Lecture 2 in one sentence:** estimate planar image mappings from trustworthy matches, resample them correctly, and recognize when distortion or 3D depth requires another model.

## The important things

1. **Convert quaternions consistently.** This chapter adds quaternion-to-matrix and matrix-to-quaternion formulas. The scalar extraction is $w=\tfrac12\sqrt{1+\operatorname{tr}R}$; near a half-turn, use a largest-component branch. See {ref}`lec02-quaternions`.
2. **SLERP interpolates orientations.** Align endpoint quaternion signs, then interpolate along the unit sphere. For nearly identical orientations, normalized linear interpolation avoids an unstable denominator.
3. **A plane can be rectified with four nondegenerate matches.** A homography supplies the mapping; the destination rectangle's aspect ratio needs known geometry for metric accuracy. Raised objects and hidden floor cannot be reconstructed by a floor warp. See {ref}`lec02-homographies`.
4. **Cross-ratio survives perspective.** For four ordered collinear coordinates, $\operatorname{CR}(a,b;c,d)=(c-a)(d-b)/((c-b)(d-a))$. Ordinary spacings may change while this value stays fixed.
5. **Inverse warping fills the output grid.** For each destination pixel, use $H^{-1}$ to locate its source sample. Bilinear interpolation blends four neighbors with weights summing to one; strong shrinking also needs antialiasing. See {ref}`lec02-warping`.
6. **DLT estimates the mapping; normalization stabilizes it.** Each homography match contributes two rows to a $2n\times9$ system. The smallest right singular vector supplies the matrix entries. Normalize each image independently, then recover $H=(T')^{-1}\widetilde H T$. See {ref}`lec02-estimation`.
7. **RANSAC rejects inconsistent matches.** Sample → fit → score → repeat → refit. Under its sampling assumptions, use $N=\lceil\log(1-p)/\log(1-w^s)\rceil$, where $w$ is the inlier fraction, $s$ the sample size, and $p$ the desired sampling success probability. Consensus is not proof of a correct model.
8. **Distortion and depth variation require different tools.** Radial correction straightens lens-bent edges. The fundamental matrix constrains correspondence by $\ell'=Fx$ and $x'^TFx=0$; it has rank two and seven DOF. Rectification aligns corresponding epipolar lines with matching rows. See {ref}`lec02-two-view`.

## Short quiz

These original questions test the additions in this chapter. Foundation quiz solutions are in {ref}`lec01-quiz-practice`.

1. For a proper rotation with trace zero, what scalar quaternion component does the trace branch give?
2. Before SLERP, what should you do if the endpoint quaternions have a negative dot product?
3. What is $\operatorname{CR}(0,1;2,3)$? Should a projective warp of the line change it?
4. How many nondegenerate matches and how many DLT rows are needed for a minimal homography estimate?
5. A source-to-destination warp translates content by $(6,-2)$ pixels. Where does destination pixel $(10,10)$ sample?
6. Four neighboring intensities are $0,20,40,60$. What is their bilinear value at the center of the square?
7. For $p=0.99$, $w=0.8$, $s=4$, is the standard RANSAC budget 8 or 9 trials? Does it guarantee the correct model?
8. If $Fx=(0,-1,4)^T$, what must a matching ordinary point $(u',v')$ satisfy? Is $u'$ determined?

## Answers

```{admonition} Show answers and short explanations
:class: dropdown

1. **$w=1/2$.** Substitute the trace into $\tfrac12\sqrt{1+\operatorname{tr}R}$; the chosen branch takes the nonnegative sign.
2. **Negate one endpoint.** This aligns quaternion signs so interpolation follows a shortest rotation path.
3. **$4/3$, unchanged.** Substitute $(2-0)(3-1)/((2-1)(3-0))$. Preserve the ordering of the four points.
4. **Four matches, eight rows.** Each match gives two independent equations; the exact nondegenerate system is $8\times9$ with rank eight.
5. **Source $(4,12)$.** Undo the translation: subtract six from the column and add two to the row.
6. **30.** At the center all four weights are $1/4$.
7. **Nine.** Round the continuous estimate, about $8.74$, up. It gives a sampling probability under stated assumptions, not a correctness guarantee.
8. **$v'=4$; $u'$ remains free.** The line equation is $-v'+4=0$; image content must still identify a match along it.
```
