(lec04-essential)=
# Recover camera pose with calibration

A fundamental matrix works with pixels. Calibration removes each camera's internal coordinate scaling, leaving a relation between **viewing directions**. That relation can reveal rotation and translation direction.

**Source:** lecture PDF pages 22–23. The explicit SVD construction below is a computational companion to the slides' essential-matrix and four-solution statements. OpenCV's [official decomposition and pose-recovery documentation](https://docs.opencv.org/4.12.0/d9/d0c/group__calib3d.html) provides an implementation cross-check: four pose candidates, a translation direction, and a positive-depth test.

```{index} Essential matrix; Cheirality; Translation scale
```

## Remove intrinsics before asking about motion

Use the first camera as the reference: $P=[I\mid0]$, $P'=[R\mid t]$ in calibrated coordinates. Here $X'=RX+t$; **$t$ is a coordinate-transform translation**, and the second camera center in the first frame is $-R^Tt$.

````{formula-box} Formula — essential matrix and calibrated constraint
```{math}
:label: eq-lec04-essential
\begin{aligned}
\widehat x&=K^{-1}x,\quad \widehat x'=K'^{-1}x',\\
E&=K'^TFK=[t]_\times R,\qquad \widehat x'^TE\widehat x=0,\\
[t]_\times&=\begin{pmatrix}0&-t_z&t_y\\t_z&0&-t_x\\-t_y&t_x&0\end{pmatrix}.
\end{aligned}
```

$K,K',F,E,R$ are $3\times3$; $t,\widehat x,\widehat x'$ are three-entry vectors. Use calibrated, undistorted coordinates and a nonzero baseline. $E$ has five DOF: three for rotation and two for translation **direction**. A nonzero essential matrix has singular values $(a,a,0)$ with $a>0$.
````

Why does the constraint work? A 3D correspondence satisfies $\lambda'\widehat x'=R\lambda\widehat x+t$. The vector $[t]_\times R\widehat x$ is perpendicular to both $t$ and $R\widehat x$, hence also to their combination $\widehat x'$. Dotting them gives zero. Conversely, substituting calibrated coordinates into $x'^TFx=0$ gives $E=K'^TFK$.

```{application} Separate calibration from coordinate normalization
1. **Input:** valid $F$ and both intrinsic matrices. Form $E=K'^TFK$.
2. Check two equal nonzero singular values and a third zero, allowing measurement noise.
3. With noisy $E=U\operatorname{diag}(s_1,s_2,s_3)V^T$, replace its singular values by $(a,a,0)$, where $a=(s_1+s_2)/2$; require $a>0$. This is the nearest essential-form correction in Frobenius norm.
4. Continue to pose decomposition and test positive depth.

$K^{-1}$ removes camera intrinsics. The earlier $T$ normalization only improves numerical conditioning. They serve different purposes. Unlike a general rank-two $F$, an $E$ also requires its first two singular values to agree.
```

## Four algebraic poses, usually one visible scene

````{formula-box} Formula — essential-matrix pose candidates
```{math}
:label: eq-lec04-poses
\begin{aligned}
E&\sim U\operatorname{diag}(1,1,0)V^T,\qquad
W=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix},\\
R_1&=UWV^T,\quad R_2=UW^TV^T,\qquad
(R,t)\in\{(R_1,\pm u_3),(R_2,\pm u_3)\}.
\end{aligned}
```

$u_3$ is the third column of $U$. Choose SVD signs so $\det U=\det V=+1$; flipping either third column leaves the zero-singular-value product unchanged. Then both $R_i$ are proper rotations. The unit translation fixes an arbitrary scale, not a known physical baseline.
````

```{application} Choose a pose by cheirality
1. Generate the four $(R,t)$ pairs and check $R^TR=I$, $\det R=1$.
2. For each pair, solve $\lambda'\widehat x'=R\lambda\widehat x+t$ for several reliable correspondences.
3. Keep the pose with positive depth in **both** cameras. This is **cheirality**: reconstructed points must lie in front of their observing cameras.
4. Check reprojection errors. With noise, use many matches and inspect an ambiguous result rather than trusting one marginal point.

Pure rotation, negligible parallax, or degenerate data can defeat this selection. General linear triangulation is developed in Lecture 6; the next example solves the two ray depths directly.
```

(ex-lec04-pose)=
````{worked-example} Worked example 4.5 — test all four poses
**Original numerical companion to:** PDF pages 22–23.

Take
$E=\begin{pmatrix}0&0&0\\0&0&1\\0&-1&0\end{pmatrix}$,
$\widehat x=(0.2,0.1,1)^T$, and $\widehat x'=(0,0.1,1)^T$.
The singular values are $(1,1,0)$. Its candidates can be written as $R=I$ or $R_x(180^\circ)=\operatorname{diag}(1,-1,-1)$, each with $t=\pm(1,0,0)^T$.

Solve $\lambda'\widehat x'=R\lambda\widehat x+t$. Its first coordinate fixes $0=0.2\lambda+t_x$; the other coordinates determine $\lambda'$.

| $R$ | $t_x$ | First depth $\lambda$ | Second depth $\lambda'$ | Visible in both? |
| --- | --- | --- | --- | --- |
| $I$ | $-1$ | $5$ | $5$ | Yes |
| $I$ | $+1$ | $-5$ | $-5$ | No |
| $R_x(180^\circ)$ | $-1$ | $5$ | $-5$ | No |
| $R_x(180^\circ)$ | $+1$ | $-5$ | $5$ | No |

The visible solution is $R=I$, $t=(-1,0,0)^T$. Its second camera center is $(1,0,0)^T$. The reconstructed point is $5\widehat x=(1,0.5,5)^T$; in camera two it is $(0,0.5,5)^T$, which reprojects correctly.

All lengths here use the chosen unit baseline. Doubling the baseline and all point coordinates leaves the two images unchanged. Metric scale needs extra information, such as a measured baseline.
````

```{understanding-check} Two different singular-value rules
A fitted matrix has singular values $(3,2,0.1)$. A rank-two $F$ correction keeps $(3,2,0)$. An essential-form correction uses $(2.5,2.5,0)$. The equal-pair condition is additional information supplied by calibration.
```
