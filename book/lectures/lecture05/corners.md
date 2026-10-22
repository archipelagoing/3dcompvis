(lec05-corners)=
# Why corners are easier to locate

**Slide a small image window. Does its appearance change?** If it barely changes, you cannot tell where it belongs. Harris corner detection measures that change in every direction.

**Source:** PDF pages 11–33. Numerical booklet companion: {ref}`Harris gradients and response <quiz-a2-q1>`. Tracking interpretation: {ref}`Spring 2019 Quiz 6 <quiz-13-q1>`.

```{figure} ../../images/lecture05/patch-types.*
:name: fig-lec05-patches
:width: 90%
:alt: Sliding windows on flat, edge, and corner regions produce different directional appearance changes.

Source PDF page 11. Flat: little change in any direction. Edge: little change along the edge. Corner: appreciable change in every direction. “Corner” describes a locally well-constrained patch, not just a sharp-looking center pixel.
```

## From a shifted patch to a 2×2 matrix

Let $I(x,y)$ be intensity and $d=(u,v)^T$ a small shift in pixels. Let $w_p\ge0$ weight sample $p$ in the patch; a Gaussian emphasizes samples near its center. The source starts with unit weights and later introduces Gaussian weights.

````{formula-box} Formula — patch change and its local approximation
```{math}
:label: eq-lec05-patch-energy
\begin{aligned}
E(d)&=\sum_{p\in W}w_p[I(p+d)-I(p)]^2,\\
I(p+d)&\approx I(p)+I_x(p)u+I_y(p)v,\\
E(d)&\approx d^TMd,\qquad
M=\sum_{p\in W}w_p
\begin{pmatrix}I_x^2&I_xI_y\\I_xI_y&I_y^2\end{pmatrix}.
\end{aligned}
```

$M$ is the **structure tensor**, also called the second-moment matrix. $I_x,I_y$ are intensity change per pixel. $M$ is $2\times2$, $d$ is $2\times1$, and $E$ is a scalar squared-intensity cost. The first line is the chosen exact patch objective; the quadratic form is a first-order small-shift approximation. Assume a differentiable/interpolated image and consistent sample weights.
````

**Why does the matrix appear?** Substitute the Taylor approximation into the intensity difference. The unchanged $I(p)$ cancels, leaving $I_xu+I_yv$. Squaring gives

$$I_x^2u^2+2I_xI_yuv+I_y^2v^2.$$

Summing those three coefficients gives the diagonal and off-diagonal entries of $M$. Multiplying $[u\ v]M(u,v)^T$ expands back to the same expression. A gradient column $g_p=(I_x,I_y)^T$ contributes the outer product $w_pg_pg_p^T$, not the scalar dot product $g_p^Tg_p$.

```{application} Build and use the structure tensor
1. Compute both spatial derivatives at each patch sample.
2. Form its full outer product; multiply by the sample weight.
3. Add the matrices entry by entry.
4. Evaluate a trial shift with $d^TMd$, or inspect eigenvalues to find weak directions.

Weights and intensity scaling affect response magnitudes, so thresholds must match that convention. See the full products in {ref}`the numerical Harris problem <quiz-a2-q1>`.
```

## Eigenvalues tell you the weak direction

An **eigenvector** is a direction the matrix scales without turning. Its **eigenvalue** is the scale. For this symmetric nonnegative tensor, choose perpendicular unit eigenvectors. Writing a shift in those directions makes the cost especially simple.

````{formula-box} Formula — tensor eigenvalues and directional change
```{math}
:label: eq-lec05-eigen
\begin{aligned}
M&=Q\operatorname{diag}(\lambda_1,\lambda_2)Q^T,
\quad Q^TQ=I,\quad \lambda_i\ge0,\\
d&=Qz\quad\Longrightarrow\quad E(d)\approx\lambda_1z_1^2+\lambda_2z_2^2,\\
M&=\begin{pmatrix}a&c\\c&b\end{pmatrix}
\quad\Longrightarrow\quad
\lambda_{\pm}=\frac{a+b\pm\sqrt{(a-b)^2+4c^2}}2.
\end{aligned}
```

The eigenvalue formula comes from $\det(M-\lambda I)=(a-\lambda)(b-\lambda)-c^2=0$. For a positive cost level $k$, the ellipse semiaxes are $\sqrt{k/\lambda_i}$ when both eigenvalues are positive. A small eigenvalue makes a long, weakly constrained direction. Eigenvalues need not be equal for a useful corner.
````

```{application} Classify the patch
1. Compute both eigenvalues and sort them as $\lambda_{max}\ge\lambda_{min}$.
2. Both small: flat patch. One small: edge-like patch. Both sufficiently large: useful two-directional structure.
3. Also check conditioning $\lambda_{max}/\lambda_{min}$ when $\lambda_{min}>0$; a very large ratio means much weaker information in one direction.
4. Interpret “large” relative to noise, intensity scale, weights, and patch size.
```

For $M=\operatorname{diag}(4,9)$, unit horizontal motion costs $4$, unit vertical motion costs $9$. The constant-cost contour $4u^2+9v^2=1$ has semiaxes $1/2$ and $1/3$. Both directions are constrained, although the vertical one changes faster.

For a diagonal edge with two gradients $(2,2)^T$, summation gives

$$M=\begin{pmatrix}8&8\\8&8\end{pmatrix},\qquad
M\begin{pmatrix}1\\-1\end{pmatrix}=\begin{pmatrix}0\\0\end{pmatrix}.$$

Both $I_x$ and $I_y$ can be large while motion along $(1,-1)^T$ remains invisible. This answers the slanted-edge part of {ref}`the original trackability quiz <quiz-13-q1>`.

## Turn the score into selected corners

````{formula-box} Formula — Harris and Shi–Tomasi responses
```{math}
:label: eq-lec05-harris
R_H=\det M-k(\operatorname{tr}M)^2
=\lambda_1\lambda_2-k(\lambda_1+\lambda_2)^2,
\qquad R_{ST}=\lambda_{min}(M).
```

$k$ is a dimensionless parameter, typically 0.04–0.06 in these slides. A large positive Harris response suggests a corner; an edge usually gives a negative response, and a weak flat patch gives a small response. A positive response alone does not set a practical detection threshold. Shi–Tomasi directly measures the least-constrained direction.
````

```{application} Run Harris detection
1. Differentiate the image; smooth the derivative products with the chosen Gaussian window.
2. Compute $M$ and $R_H$ at every candidate pixel.
3. Keep responses above a chosen threshold.
4. Apply **non-maximum suppression (NMS)**: retain a local peak rather than every nearby high response. Define a tie-breaking rule and minimum separation.
5. Reject image-border candidates without sufficient valid support.
```

```{figure} ../../images/lecture05/harris-stages.*
:name: fig-lec05-harris-stages
:width: 95%
:alt: Five stages of Harris detection on the lecture toy-animal image: input, response, thresholded mask, local maxima, and selected points.

The source toy-animal sequence, PDF pages 28–33. Thresholding produces clusters; NMS selects representative peaks. The source local-maxima marks are tiny: compare that sparse panel with the threshold mask and final overlay. Source image creator/reuse terms unidentified.
```

(ex-lec05-nms)=
`````{worked-example} Worked example 5.1 — a threshold is not NMS
```{original-question} Original practice question
**Original companion to:** PDF pages 30–32. Suppose the local response grid is

$$R=\begin{pmatrix}1&2&1&0&0\\2&9&8&0&1\\1&7&3&1&2\\0&0&1&6&1\\0&0&0&1&0\end{pmatrix}.$$
```

````{solution-step} 1 — Apply the threshold
**Why:** Weak responses should not become candidates.

With the strict threshold $R>5$, the surviving values are $9,8,7,6$. Use one-based row/column locations: $(2,2),(2,3),(3,2),(4,4)$.
````

````{solution-step} 2 — Compare each candidate with its neighbors
**Why:** Adjacent high responses can describe the same local feature.

In a $3\times3$ neighborhood, the $9$ suppresses the neighboring $8$ and $7$. The $6$ at $(4,4)$ is larger than its own neighbors, so it survives. The two retained centers are $(2,2)$ and $(4,4)$.
````

````{solution-step} 3 — Check what the procedure guarantees
**Why:** A local maximum is a selection rule, not proof of a correct correspondence.

Both surviving responses exceed the threshold and are local peaks. A later matching step must still identify the corresponding physical points.
````
`````

## Explore the surface in 3D

`````{interactive-demo} corner
Switch among a flat patch, an edge, and a corner. The image panel is schematic; the **two listed gradient samples** define the exact model. Change the trial shift and rotate the error surface to inspect the weak directions. Orbiting only changes the inspection view.

**Static experiment:** use unit weights and these two-sample models:

| Patch | Gradient samples | Tensor $M$ | Eigenvalues | Trial cost at $(u,v)=(1,0)$ |
| --- | --- | --- | --- | --- |
| Flat | $(0,0),(0,0)$ | zero matrix | $0,0$ | $0$ |
| Edge | $(2,2),(2,2)$ | $\left(\begin{smallmatrix}8&8\\8&8\end{smallmatrix}\right)$ | $16,0$ | $8$ |
| Corner | $(2,0),(0,3)$ | $\operatorname{diag}(4,9)$ | $9,4$ | $4$ |

The exact displayed quadratic model is $E_{lin}=d^TMd$. Its relationship to the nonlinear image-shift cost is approximate. For the edge, shifts $(1,-1)$ cost zero; for the corner that shift costs $4+9=13$. This is the difference between an ambiguous valley and a bowl with a unique minimum.

```{figure} ../../images/lecture05/error-surfaces.*
:name: fig-lec05-surfaces
:width: 95%
:alt: A flat plane, a trough, and a bowl represent flat, edge and corner patch error surfaces.

Original surfaces for the three stated tensors. Every printed result uses the same matrices as the interactive.
```
`````

```{index} Structure tensor
```
```{index} Harris corner detector
```
```{index} Non-maximum suppression
```
```{index} Aperture problem
```
