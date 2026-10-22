(lec05-tracking)=
# Track a feature by solving for its motion

**Which small shift makes the next patch resemble this one?** Instead of trying every pixel displacement, Lucas–Kanade uses local intensity derivatives to predict an improving shift.

**Source:** PDF pages 34–60. Full assigned problems: {ref}`exposure changes <quiz-9-q1>`, {ref}`trackability <quiz-13-q1>`, and {ref}`the numerical displacement calculation <quiz-a3-q1>`.

```{figure} ../../images/lecture05/motion-pairs.*
:name: fig-lec05-motion
:width: 90%
:alt: Source image pairs illustrate motion from a moving camera and a moving object.

Source PDF pages 36–37. Either camera motion or object motion changes image locations. The tracker estimates local image displacement; that displacement alone does not identify its 3D cause.
```

## One pixel gives one equation, not two

Let $I$ be the first frame and $J$ the next. **Brightness constancy** assumes the same visible surface has the same intensity after motion. **Spatial coherence** assumes a sufficiently small patch shares one translation. **Small motion** permits a local Taylor approximation.

````{formula-box} Formula — brightness constancy and patch least squares
```{math}
:label: eq-lec05-lk
\begin{aligned}
J(p+d)&\approx I(p),\qquad
J(p+d)\approx J(p)+J_xu+J_yv,\\
J_xu+J_yv&\approx-I_t,\qquad I_t=J(p)-I(p),\\
A&=\begin{pmatrix}J_x(p_1)&J_y(p_1)\\\vdots&\vdots\\J_x(p_n)&J_y(p_n)\end{pmatrix},\quad
b=-\begin{pmatrix}I_t(p_1)\\\vdots\\I_t(p_n)\end{pmatrix},\\
d^*&=\arg\min_d\|Ad-b\|^2,\qquad A^TAd=A^Tb.
\end{aligned}
```

$A$ is $n\times2$, $b$ is $n\times1$, $d$ is $2\times1$. Derivatives and displacement use consistent intensity/pixel units. This is the forward-additive local linearization using gradients of $J$ at the current warp. Reference-gradient/inverse-compositional variants change the update derivation; do not mix their signs or formulas. A single pixel supplies one scalar equation for two motion components.
````

**Why least squares?** Different patch pixels provide different gradient directions. Stack their equations and choose the displacement that minimizes their total squared residual. Differentiating $(Ad-b)^T(Ad-b)$ gives $2A^T(Ad-b)$; set this to zero to obtain the normal equations. In numerical code use QR/SVD or a stable solve, rather than explicitly forming an inverse.

The normal matrix is precisely the unweighted structure tensor:

$$A^TA=\begin{pmatrix}\sum J_x^2&\sum J_xJ_y\\\sum J_xJ_y&\sum J_y^2\end{pmatrix}=M.$$

That is the connection between **finding** a good feature and **tracking** it. Harris tests whether the same matrix will give a useful motion estimate. A weighted tracker uses $A^TWA$ and $A^TWb$, with $W=\operatorname{diag}(w_p)$.

```{application} Compute a Lucas–Kanade displacement
1. Select a textured patch; compute the current temporal differences and consistently chosen spatial derivatives.
2. Stack every row of $A$ and entry of $b$; keep the minus sign in $b=-I_t$.
3. Check the smallest eigenvalue and conditioning of $A^TA$. Reject ambiguous patches.
4. Solve the least-squares system. Interpret the result as the next-frame location minus the first-frame location under this convention.
5. Warp the next patch, recompute residuals, and verify that the match improved.

The {ref}`booklet numerical problem <quiz-a3-q1>` shows the full matrices, normal equations and displacement $(2,1)^T$.
```

## Why an edge can fool you

The **aperture problem** means a local edge reveals motion across the edge, but not motion along it. Adding more pixels with parallel gradients repeats the same directional information; it does not create a second independent equation.

```{figure} ../../images/lecture05/aperture.*
:name: fig-lec05-aperture
:width: 90%
:alt: Source diagrams compare actual and perceived motion for an edge seen through a circular aperture, then resolve it using multiple directions.

Source PDF pages 42–43 and 54–55. A second independent edge direction resolves the ambiguity. The barber-pole example in pages 44–45 illustrates the same effect perceptually; the moving stripes' local appearance need not reveal their full physical motion.
```

The original {ref}`junction/edge/isolated-dot quiz <quiz-13-q1>` makes an important distinction: two nonzero derivative components do not ensure two independent gradient directions. Feature quality depends on the **whole tracking patch**, not whether its center pixel is black or white. The source flat/edge/high-texture tree examples (pages 51–53) apply the same two-eigenvalue test.

## Iterate, then use a pyramid when necessary

````{formula-box} Formula — iterative tracking and coarse-to-fine transfer
```{math}
:label: eq-lec05-iteration
\begin{aligned}
r_p(d_k)&=J(p+d_k)-I(p),\\
A_k\Delta d&\approx-r(d_k),\qquad d_{k+1}=d_k+\Delta d,\\
d_{\ell-1}^{init}&=2d_\ell
\quad\text{for adjacent pyramid levels differing by factor two}.
\end{aligned}
```

$A_k$ contains the warped next-image gradients for this forward-additive version. Interpolate fractional coordinates. Displacements are measured in the pixels of their current pyramid level. Recompute gradients if the chosen formulation requires it; stop on a small update, small residual improvement, or an iteration limit. The local translation/appearance model can still fail.
````

```{application} Track beyond one small step
1. Smooth and downsample both frames to create compatible Gaussian pyramids.
2. Estimate motion at a coarse level, where large original motion occupies fewer pixels.
3. Double the displacement when moving to the next finer level; warp and refine there.
4. Reject failed tracks using residuals, conditioning, visibility, and forward/backward or reference-patch consistency.

For example, a displacement of 12 full-resolution pixels becomes 3 pixels after two factor-two reductions. A coarse estimate of $(3,1)$ initializes $(6,2)$ at the next level and $(12,4)$ at full resolution. A pyramid helps but does not guarantee convergence.
```

```{figure} ../../images/lecture05/tracking-sign.*
:name: fig-lec05-sign
:width: 75%
:alt: Source street-sign crops show tracked windows across frames and appearance after registration.

The lecture's “25” sign sequence, PDF page 59, attributed there to frames from Woody Allen's Manhattan and the tracking illustration. Compare the changing observed windows with the registered patches. Their agreement tests a track; incremental motion updates alone do not prevent drift. Source reuse terms unidentified.
```

Shi–Tomasi tracking (page 58) starts with features whose smallest tensor eigenvalue is large enough, tracks with a local translation model, then checks registration against the **first** observed patch. An affine consistency check can absorb moderate local shape change. Repeatedly replacing the template without checking the original can accumulate **drift**. Add newly visible points and remove occluded, out-of-image, weak or inconsistent ones.

## What if the camera changes exposure?

A correct match can violate raw brightness constancy when $J\approx aI+b$. The original {ref}`Fall 2025 exposure quiz <quiz-9-q1>` derives mean/standard-deviation patch normalization and checks an actual numerical pair.

````{formula-box} Formula — exposure-normalized patch
```{math}
:label: eq-lec05-photometric
\mu=\frac1n\sum_p I(p),\quad
\sigma^2=\frac1n\sum_p[I(p)-\mu]^2,\quad
\widetilde I(p)=\frac{I(p)-\mu}{\sigma+\varepsilon}.
```

For positive gain $a$ and nonzero variance, setting $\varepsilon=0$ exactly cancels an affine brightness change. Positive $\varepsilon$ makes that cancellation approximate. It prevents division by zero but does not make a flat patch informative. Clipping, cast shadows, specularities and spatially varying exposure can defeat this model.
````

```{application} Adapt the tracker to exposure changes
1. Reject nearly flat/saturated patches before normalizing.
2. Compute the normalization and track normalized appearance with consistent derivatives.
3. Specify whether patch statistics are frozen within a local solve or differentiated as part of the full residual; update them consistently after warping.
4. Alternatively estimate gain and offset alongside motion, then check residuals and conditioning.

Normalization is also the core of the NCC comparison already covered in Lecture 4; the new task here is using it consistently in the tracking linearization.
```

```{index} Lucas–Kanade tracking
```
```{index} Brightness constancy
```
```{index} Drift
```
