(lec02-estimation)=
# Estimate a reliable mapping

Four matches can determine a homography, but real matches are noisy and some are wrong. **DLT** solves for the matrix; **RANSAC** finds matches that agree with one matrix. They solve different problems.

**Source:** PDF pages 82–104, printed slides 83–105. These sections credit R. Hartley, A. Zisserman, and M. Pollefeys. [Lecture 3](../lecture03/index.md) adds the assigned homography/probability quizzes and a full projective numerical walkthrough.

## DLT: turn matches into linear equations

The **direct linear transformation (DLT)** starts from $x'\sim Hx$. Their cross product is zero because the vectors represent the same projective point: $x'\times Hx=0$.

For finite matches $(u,v)\leftrightarrow(u',v')$, multiply out the denominators in {eq}`eq-lec02-homography`. Each match supplies two independent equations in the nine entries of $H$.

````{formula-box} Formula — homography DLT system
```{math}
:label: eq-lec02-dlt
\begin{aligned}
A_i&=\begin{pmatrix}
u&v&1&0&0&0&-u'u&-u'v&-u'\\
0&0&0&u&v&1&-v'u&-v'v&-v'
\end{pmatrix},\\
h&=(h_{11},h_{12},h_{13},h_{21},h_{22},h_{23},h_{31},h_{32},h_{33})^T,\\
A&=\begin{pmatrix}A_1\\\vdots\\A_n\end{pmatrix},\qquad
\min_{\|h\|=1}\|Ah\|^2.
\end{aligned}
```

$A$ is $2n\times9$, $h$ is $9\times1$. The constraint excludes the useless zero solution. Four nondegenerate exact matches give rank eight and a one-dimensional nullspace; with noisy extra matches, minimize the residual instead of expecting exact zero.

The finite-coordinate rows assume each destination's last coordinate is nonzero. For ideal points, retain appropriate independent rows of the full cross-product system. Three cross-product equations have only two independent constraints; dropping the same row blindly can lose information.
````

```{application} Estimate a homography with SVD
1. Normalize coordinates as described below; reject a degenerate four-point sample.
2. Stack two rows per match to form $A$.
3. Compute $A=U\Sigma V^T$ using singular value decomposition. Choose the **right singular vector** with smallest singular value and reshape it row by row into $H$.
4. Undo coordinate normalization and check projected matches.

For an $8\times9$ system, request the full right-singular-vector basis: a reduced SVD can omit the ninth vector containing the nullspace. Do not confuse the last row of $V^T$ with the last column of $V^T$.
```

Fixing $h_{33}=1$ is a tempting shortcut, but valid homographies can have $h_{33}=0$. Unit-vector normalization avoids privileging that entry. DLT minimizes **algebraic error**, which depends on coordinate scaling. Pixel reprojection error is a more interpretable final accuracy measure.

(ex-lec02-dlt)=
````{worked-example} Worked example 2.4 — recover a simple planar map
**Source:** original numerical companion to PDF pages 83–94.

Match $(0,0),(1,0),(1,1),(0,1)$ to $(2,1),(4,1),(4,4),(2,4)$ in that order. The first correspondence produces rows

$$
(0,0,1,0,0,0,0,0,-2),\qquad
(0,0,0,0,0,1,0,0,-1).
$$

For $(1,0)\leftrightarrow(4,1)$ the rows are

$$
(1,0,1,0,0,0,-4,0,-4),\qquad
(0,0,0,1,0,1,-1,0,-1).
$$

The other two matches fill the remaining four rows. The resulting matrix has rank eight. Its null vector, reshaped and rescaled, gives
$H=\begin{pmatrix}2&0&2\\0&3&1\\0&0&1\end{pmatrix}$.

Check the unmeasured center: $H(1/2,1/2,1)^T=(3,5/2,1)^T$, the center of the destination rectangle. All four measured corners reproject exactly. Three collinear source points would invalidate this four-point recovery.
````

## Normalize: put the coordinates on a sensible scale

Raw pixel coordinates may be hundreds, while their products in $A$ reach tens of thousands. **Normalized DLT** recenters and rescales each image's points independently, reducing this imbalance.

````{formula-box} Formula — coordinate normalization and recovery
```{math}
:label: eq-lec02-normalize
\begin{aligned}
c&=\frac1n\sum_i p_i,\quad
\bar r=\frac1n\sum_i\|p_i-c\|,\quad s=\frac{\sqrt2}{\bar r},\\
T&=\begin{pmatrix}s&0&-sc_u\\0&s&-sc_v\\0&0&1\end{pmatrix},\qquad
\widetilde x=Tx,\quad \widetilde x'=T'x',\\
H&=(T')^{-1}\widetilde H T.
\end{aligned}
```

$p_i=(u_i,v_i)^T$ are finite 2D points; $T,T',H$ are $3\times3$. The mean distance from the normalized centroid becomes $\sqrt2$. Require $\bar r>0$; coincident points provide no spatial information. Normalization improves conditioning, not incorrect matches or degeneracy.
````

```{application} Use normalized DLT
1. Compute separate $T,T'$ from the source and destination matches.
2. Fit $\widetilde H$ to their normalized coordinates using {eq}`eq-lec02-dlt`.
3. Recover $H=(T')^{-1}\widetilde H T$ and evaluate error in original coordinates.

The source square in Example 2.4 has centroid $(1/2,1/2)$, mean radius $1/\sqrt2$, and scale $s=2$. Its normalized corners are $(\pm1,\pm1)$, at radius $\sqrt2$.
```

Why this recovery order? The normalized mapping is $T'x'\sim\widetilde H Tx$. Multiply by $(T')^{-1}$ to isolate the original destination coordinates. PDF page 92 also shows a simpler image-size scaling; it is an alternative heuristic, not the same transformation as centroid/mean-distance normalization.

## RANSAC: do not let wrong matches vote as measurements

An **{term}`inlier <Inlier>`** agrees with the model within a chosen error threshold. An **outlier** does not. **{term}`RANSAC <RANSAC>`** means random sample consensus: fit small random subsets, then count how many matches support each hypothesis.

```{figure} ../../images/lecture02/ransac.*
:name: fig-lec02-ransac
:width: 85%
:alt: A line supported by many clustered points despite scattered outliers, illustrating model consensus.

The idea behind the lecture's robust-line example: a large consistent group supports the correct model despite scattered bad measurements. Original schematic; homography hypotheses use four matches rather than two line points.
```

````{formula-box} Formula — RANSAC trial count and inlier score
```{math}
:label: eq-lec02-ransac
\begin{aligned}
N&=\left\lceil\frac{\log(1-p)}{\log(1-w^s)}\right\rceil,\\
r_i&=\|p_i'-\operatorname{dehom}(Hx_i)\|_2,\qquad
n_{\rm in}=\#\{i:r_i<\tau\}.
\end{aligned}
```

$p$ is the desired probability of at least one all-inlier sample, $w=1-e$ the inlier fraction, and $s$ the sample size (four for a homography). Here residuals and threshold $\tau$ are in destination pixels. $N$ is a dimensionless integer.

The usual $w^s$ model assumes independent draws, or a large pool approximating them, and nondegenerate all-inlier samples. Trials are independent. For sampling $s$ distinct matches from a small pool of $n$ containing $I$ true inliers, the exact all-inlier probability is $\binom I s/\binom n s$. Neither probability guarantees the selected model is correct.
````

The derivation is short: a trial is all-inlier with probability $w^s$. All $N$ trials fail with probability $(1-w^s)^N$. Set that failure probability at most $1-p$, take logarithms, and round up.

```{application} Fit a homography robustly
1. Sample four matches; reject collinear or otherwise degenerate configurations; estimate $H$.
2. Score every match against $H$ using a fixed error definition and threshold.
3. Keep the best consensus and repeat to the trial budget. Update the budget from a better observed inlier ratio, while recognizing that it is an estimate.
4. Refit to the best inliers, then refine pixel reprojection error if needed.

For $w=0$ no finite budget succeeds; for $w=1$ one nondegenerate trial suffices. A large consensus of repeated patterns can still support the wrong alignment. See Example 2.5.
```

(ex-lec02-ransac)=
```{worked-example} Worked example 2.5 — why a better inlier fraction saves work
**Source:** numerical expansion of PDF page 98's trial table; application figures from PDF page 104.

With $p=0.99$, $w=0.5$, and $s=4$, the continuous budget is $\log(0.01)/\log(15/16)\approx71.36$. Round **up** to 72 trials. At $w=0.8$, it falls to 9.

The lecture's building-image example starts with 268 putative matches. A 151-match consensus corresponds to roughly 56% inliers; using that rounded ratio gives about 45 trials. The slide reports 43 iterations: the simple probability model is a budget estimate, not a reproduction of the implementation's exact stopping history. Guided matching later finds 262 final inliers; this is a new matching stage, not simply the original consensus.
```

An expected consensus threshold is approximately $wn$ (rounded as needed), but it is not a statistical guarantee. **LMedS**, least median of squares, instead minimizes median squared residual; it is a different robust objective. Ordinary least squares can be dominated by gross outliers. Iterative refinement is useful **after** robust selection; iteration alone does not make an estimator robust.

## The complete slide pipeline

Detect interest points → propose matches → robustly estimate $H$ → refine using inliers → use $H$ to guide more matches. The slides name sum of absolute differences (SAD), sum of squared differences (SSD), and zero-mean normalized cross-correlation (ZNCC) as patch comparisons. SAD/SSD compare pixel intensities directly; ZNCC compares mean-centered, normalized patterns and needs nonzero patch variance. Lecture 5 develops matching and exposure changes.

When motion is known to be small, restrict candidate locations; do not impose that restriction on arbitrary viewpoint changes. Nonlinear refinement may use Levenberg–Marquardt to minimize an image-error objective, rather than the initial algebraic DLT objective.

```{understanding-check} Check 2.3 — can more points rescue a bad model?
Would fitting one homography to hundreds of matches on several depths always work better than using four floor corners?
```

```{admonition} Answer
:class: dropdown
No. Extra measurements cannot repair the wrong geometric model. With translation, a single homography generally fits one plane, not objects at many depths.
```

```{index} direct linear transformation
```

```{index} normalized DLT
```

```{index} RANSAC
```

```{index} inlier
```
