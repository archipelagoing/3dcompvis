(lec06-triangulation)=
# Triangulation: find the 3D point behind two pixels

**Each pixel gives a ray. Triangulation finds a point consistent with several rays.** Real rays usually miss because image measurements contain error.

**Source:** PDF pages 48–52. For full camera matrices, row construction, and substitution checks, work through {ref}`the booklet triangulation example <quiz-a5-q1>`.

## Turn projection into linear equations

Write the rows of camera $P_i$ as $p_{i1}^T,p_{i2}^T,p_{i3}^T$. For an observed homogeneous image point $(u_i,v_i,1)^T$,

$$u_i=\frac{p_{i1}^TX}{p_{i3}^TX},\qquad v_i=\frac{p_{i2}^TX}{p_{i3}^TX}.$$

Multiply by the denominator and move the numerator to the left. Each image supplies two independent rows.

````{formula-box} Formula — linear homogeneous triangulation
```{math}
:label: eq-lec06-triangulation
A_i=\begin{pmatrix}u_ip_{i3}^T-p_{i1}^T\\v_ip_{i3}^T-p_{i2}^T\end{pmatrix},\quad
A=\begin{pmatrix}A_1\\\vdots\\A_m\end{pmatrix},\quad
\widehat X=\underset{\|X\|=1}{\arg\min}\|AX\|^2.
```

$A$ is $2m\times4$. Its right singular vector with smallest singular value is $\widehat X$. If $\widehat X_4\ne0$, divide by that entry to obtain Euclidean coordinates. A zero last entry describes a point at infinity, not a finite coordinate you can obtain by dividing by zero.
````

```{application} Triangulate and check
1. Use image coordinates consistent with the cameras. If normalizing pixels by $T_i$, transform the camera to $T_iP_i$ too.
2. Build every row explicitly and take the last right singular vector.
3. Dehomogenize only if safe; reproject into every camera.
4. Check positive physical depth (**cheirality**) in the calibrated camera frames.
5. Reject large residuals and very small ray angles. Nearly parallel rays make depth unstable.
```

The linear method minimizes an **algebraic** residual. Rescaling rows or changing coordinates can change its noisy answer; it is not automatically invariant under arbitrary projective coordinate changes. Use it as a good initializer, then minimize the image error you care about.

## Refine the point in image coordinates

````{formula-box} Formula — geometric triangulation objectives
```{math}
:label: eq-lec06-geometric
\begin{aligned}
X^*&=\arg\min_X\sum_i\|\pi(P_iX)-x_i\|^2,\\
(\bar x,\bar x')^*&=\arg\min_{\bar x,\bar x'}
\bigl(\|\bar x-x\|^2+\|\bar x'-x'\|^2\bigr),\\
&\hspace{2em}\text{subject to }\bar x'^TF\bar x=0.
\end{aligned}
```

$\pi(a,b,c)^T=(a/c,b/c)^T$; norms in the second formulation compare the two finite image coordinates, with a homogeneous 1 appended only for the epipolar constraint. The first optimizes a 3D point with **fixed cameras**. The second finds the closest consistent pair of image points for a valid two-view $F$. Both assume the chosen unweighted pixel-error model; unequal uncertainty calls for suitable weights.
````

```{application} Choose the refinement
1. Obtain a linear estimate and inspect validity and residuals.
2. For fixed known cameras, refine the 3D point against reprojection error.
3. For the source's optimal two-view correction, parameterize corresponding epipolar lines and optimize the two corrected points before triangulating.
4. Compare all valid candidates and include boundary/infinite-parameter cases where required by that algorithm.
```

**What is the sixth-degree polynomial on slide 52?** Parameterizing the pair of epipolar lines by one scalar $t$ turns the correction cost into a rational function. Setting its derivative to zero yields a polynomial of degree up to six. Its real roots are candidate stationary solutions; evaluating the original cost chooses the best valid candidate. The degree does not mean six iterations or six cameras. The slide presents the reduction, not the full polynomial coefficients.

```{index} Triangulation
```
```{index} Cheirality
```
