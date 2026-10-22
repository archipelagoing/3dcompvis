(lec04-estimation)=
# Estimate F from noisy matches

The [eight-point route](../lecture02/two-view.md) already supplies the linear rows and normalization order. Here we add what makes that route usable: a numerical noisy fit, an explicit rank constraint, and an error measured in pixels.

**Source:** lecture PDF pages 24–37; printed slides 24–34, then 39–41. The section develops the earlier Hartley–Zisserman–Pollefeys material.

## Make the fitted matrix physically admissible

Noise usually gives a full-rank linear estimate. A true fundamental matrix must have rank two.

````{formula-box} Formula — nearest rank-two correction
```{math}
:label: eq-lec04-ranktwo
\widehat F=U\operatorname{diag}(\sigma_1,\sigma_2,\sigma_3)V^T,
\qquad
F_2=U\operatorname{diag}(\sigma_1,\sigma_2,0)V^T.
```

The $3\times3$ SVD has $\sigma_1\ge\sigma_2\ge\sigma_3\ge0$. This minimizes the Frobenius distance (the square root of the sum of squared entry differences) among matrices of rank at most two. Require $\sigma_2>0$ for rank **exactly** two. It does not minimize image reprojection error.
````

```{application} Correct the normalized estimate
1. **Input:** the matrix reshaped from the normalized linear system's smallest right singular vector.
2. Compute its SVD and set only the smallest singular value to zero.
3. Undo point normalization using the existing rule $F=T'^TF_2T$.
4. **Check:** rank two, valid epipoles, and pixel-space errors on matches you did not fit.

Normalization improves numerical conditioning; it cannot repair outliers or degenerate geometry. The source's image-size mapping to $[-1,1]^2$ is a scaling heuristic. The worked example uses independent centroid/mean-distance normalization from Lecture 2.
```

```{raw} latex
\Needspace{15\baselineskip}
```

## Measure how far a point misses its predicted line

An algebraic residual $x'^TFx$ changes if you rescale $F$. Pixel distance to the line does not.

````{formula-box} Formula — point-to-line and symmetric epipolar error
```{math}
:label: eq-lec04-epipolar-error
\begin{aligned}
\operatorname{dist}(x',\ell')&=\frac{|au'+bv'+c|}{\sqrt{a^2+b^2}},\quad
x'=(u',v',1)^T,\ \ell'=(a,b,c)^T,\\
r&=x'^TFx,\quad \ell'=Fx,\quad \ell=F^Tx',\\
e_{\rm sym}^2&=r^2\left[\frac1{\ell_1'^2+\ell_2'^2}
+\frac1{\ell_1^2+\ell_2^2}\right].
\end{aligned}
```

Use undistorted pixel coordinates and finite lines with nonzero first-two-component norm. The symmetric error sums squared distances in both images; it is not the same as minimizing jointly corrected image positions. Near an epipole, a vanishing line makes this calculation undefined.
````

```{application} Score a hypothesis in image units
1. Predict a line in each image and compute its perpendicular point distance.
2. Combine the two squared distances if using the symmetric criterion.
3. Set a threshold in units matching that criterion: pixels for distance, pixels squared for squared error.
4. Inspect held-out errors and spatial coverage, not just the number of fitted points.

For line $(0,-2,6)^T$ and point $(5,4,1)^T$, the distance is $|-8+6|/2=1$ pixel. Scaling the line by ten leaves the answer unchanged.
```

(ex-lec04-eightpoint)=
````{worked-example} Worked example 4.4 — a complete noisy eight-point-route fit
**Original numerical companion to:** PDF pages 25–33. Twelve matches make this an overdetermined fit using the eight-point algorithm, not a different “twelve-point” camera model. Coordinates are pixels, rounded to two decimals **before fitting**.

| $u$ | $v$ | $u'$ | $v'$ |
| --- | --- | --- | --- |
| 160.14 | 174.24 | 192.03 | 195.37 |
| 506.19 | 306.72 | 505.53 | 337.77 |
| 115.57 | 325.55 | 134.85 | 346.85 |
| 344.14 | 93.47 | 305.48 | 122.09 |
| 186.44 | 258.74 | 208.55 | 281.31 |
| 211.28 | 59.43 | 209.20 | 86.37 |
| 555.25 | 368.93 | 556.98 | 406.35 |
| 168.42 | 96.09 | 116.58 | 131.45 |
| 445.56 | 357.02 | 477.41 | 384.87 |
| 17.61 | 68.56 | 10.62 | 103.15 |
| 108.56 | 279.43 | 127.33 | 300.86 |
| 499.77 | 272.68 | 543.72 | 295.87 |

**1. Normalize both sets.** Centroid/mean-distance normalization gives

$$
T\approx\begin{pmatrix}.0071174&0&-1.968505\\0&.0071174&-1.578194\\0&0&1\end{pmatrix},\quad
T'\approx\begin{pmatrix}.0070558&0&-1.992253\\0&.0070558&-1.759429\\0&0&1\end{pmatrix}.
$$

**2. Stack one row per match.** The first normalized row of {eq}`eq-lec02-eightpoint` is approximately

$$
(0.528172,0.215457,-0.637327,0.315694,0.128781,-0.380937,
-0.828729,-0.338063,1).
$$

The matrix is $12\times9$. Use its smallest right singular vector, reshaped row by row into $\widehat{\widetilde F}$.

**3. Enforce rank two.** This normalized matrix has singular values approximately
$(0.718385,0.695646,0.000568)$. Set the last to zero using {eq}`eq-lec04-ranktwo`.

**4. Undo normalization.** With full-precision intermediate values, $F=T'^TF_2T$. Rescaling only for display so $F_{33}=1$ gives

$$
F\approx\begin{pmatrix}
6.85735\!\times\!10^{-7}&2.31624\!\times\!10^{-6}&-0.00429928\\
2.63343\!\times\!10^{-6}&8.60518\!\times\!10^{-7}&-0.02609573\\
0.00274885&0.02456939&1
\end{pmatrix}.
$$

**5. Check what the fit predicts.** The training root-mean-square symmetric epipolar error is about **0.49 pixels**. Four unmeasured projections from the generating cameras give about **0.33 pixels**. Those points were not used for fitting. Rounded matrix entries can alter residuals; the check uses full precision.

For reproducibility, the original synthetic scene uses 16 noncoplanar points, a 9° camera rotation, translation $(-0.8,0.12,0.05)^T$, and independent approximately 0.25-pixel coordinate noise on the twelve training matches. This is a controlled example, not a guarantee that real correspondences will fit this well.
````

## Robust fitting: change the model and sample size

Use the existing [RANSAC explanation](../lecture02/estimation.md) and [sampling qualifications](../lecture03/probability-ransac.md). The new detail is that a fundamental-matrix **seven-point solver** can generate multiple candidate matrices from one sample. Its two-dimensional linear nullspace becomes $F(\lambda)=F_0+\lambda F_1$; imposing $\det F(\lambda)=0$ gives a cubic, generically with one or three real candidate roots. Score each candidate.

An eight-point solver needs eight matches instead. At 80% inliers and 99% clean-sample confidence, the independent-status budgets are **20** trials for seven-point samples and **26** for eight-point samples. The slide's table on PDF page 35 corresponds to about **95%**, not 99%; choose the confidence explicitly.

After scoring, refit on the inliers, search near predicted epipolar lines for additional matches, and refine geometric error. Under Gaussian image-coordinate noise, the slide's maximum-likelihood recommendation minimizes squared displacements to jointly corrected corresponding image points; this is stronger than finding the nearest matrix in entry space. PDF page 36's ±1.5-pixel band is an example tolerance, not a universal constant. Planar scenes and pure rotation remain [degenerate cases](../lecture02/two-view.md); a plausible low residual alone does not prove a recoverable camera baseline.
