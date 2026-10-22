(lec05-quiz-workbook)=
# Original quiz questions and worked solutions

**Read the problem in black. Follow the numbered red steps. Work through the blue mathematics.** Every step explains why it is needed. Matrix calculations show the inputs and intermediate results; written-reasoning questions explain the decision instead of inventing numerical data.

**Source:** the supplied lecture-organized quiz booklet. Full problems follow its wording and givens, with typography normalized; the historical PDF filenames appear below. Source-key corrections and added numerical companions are marked.

**Retests have their own questions and full solutions.** Problems labeled **Original practice** are the booklet’s seven supplemental examples, separate from the 18 historical quizzes. Colored steps remain numbered and readable in grayscale.

## Jump to a quiz

- {ref}`Fall 2025 Quiz 4 — KLT with auto-exposure <quiz-source-9>`
- {ref}`Spring 2019 Quiz 6 — Feature trackability <quiz-source-13>`
- {ref}`A2. Harris response from gradients (L5, slides 11–30) <quiz-source-a2>`
- {ref}`A3. Lucas–Kanade least-squares displacement (L5, slides 39–50) <quiz-source-a3>`

---

(quiz-source-9)=
## Fall 2025 Quiz 4 — KLT with auto-exposure

**Historical source:** `3dcvMid/quizzesf25sol/cs532f25_quiz_4_solution.pdf`.

(quiz-9-q1)=
### Question 1

````{original-question}
You track features over a long monocular video with automatic exposure that changes brightness from frame to frame. Propose modifications to the KLT brightness-constancy formulation, explaining why they improve robustness without invalidating the local linearization.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — State brightness constancy
**Why:** Ordinary KLT explains image changes using motion alone.

State original KLT assumption: $I_2(x+\mathbf d)\approx I_1(x)$, with $\mathbf d=(u,v)^T$. Linearizing gives $I_xu+I_yv+I_t\approx0$.
````

````{solution-step} 2 — Model the exposure change
**Why:** Gain and offset can change intensities even at the correct match.

Model auto-exposure as a frame-dependent affine brightness change: $I_2(x+\mathbf d)\approx aI_1(x)+b$, where $a>0$ rescales contrast and $b$ changes brightness. This violates raw brightness constancy even if motion is correct.
````

````{solution-step} 3 — Normalize each patch
**Why:** Subtracting the mean removes offset and standardizing removes positive gain.

For each local patch $W$, calculate its mean $\mu=(1/|W|)\sum_W I$ and standard deviation $\sigma=\sqrt{(1/|W|)\sum_W(I-\mu)^2}$. Define normalized intensity $\boxed{\widetilde I(x)=(I(x)-\mu)/(\sigma+\varepsilon)}$, with a small $\varepsilon$ preventing division by zero.
````

````{solution-step} 4 — Prove the cancellation
**Why:** The affine exposure terms cancel under nonzero patch variance.

Show why the correction works when $\varepsilon\approx0$: if $I_2=aI_1+b$ and $a>0$, then $\mu_2=a\mu_1+b$ and $\sigma_2=a\sigma_1$. Therefore 

$$
\widetilde I_2=\frac{aI_1+b-(a\mu_1+b)}{a\sigma_1}=\frac{I_1-\mu_1}{\sigma_1}=\widetilde I_1.
$$
````

````{solution-step} 5 — Linearize the normalized images
**Why:** Tracking still needs derivatives of the residual that is actually optimized.

Now apply the usual local Taylor expansion to *normalized* patches: $\widetilde I_2(x+\mathbf d)\approx\widetilde I_2(x)+\nabla\widetilde I_2(x)^T\mathbf d$. The tracking equations retain the Lucas–Kanade/KLT least-squares form but use normalized derivatives.
````

````{solution-step} 6 — Consider joint exposure estimation
**Why:** Gain and offset can instead be treated as extra unknowns.

Optional alternative: estimate exposure nuisance parameters jointly by minimizing $\sum_W[I_2(x+\mathbf d)-aI_1(x)-b]^2$; linearize the residual with respect to small increments in $u,v,a,b$.
````

````{solution-step} 7 — Verify a numerical patch pair
**Why:** Matching normalized columns demonstrate the correction and its assumptions.

Original numerical companion: patches $I_1=(10,20,30)^T$ and $I_2=(30,50,70)^T=2I_1+10$ have means $20$ and $50$. Their centered columns are $(-10,0,10)^T$ and $(-20,0,20)^T$; population standard deviations are $\sqrt{200/3}$ and $2\sqrt{200/3}$. With $\varepsilon=0$ they normalize to the same column:

$$
\widetilde I_1=\widetilde I_2=\begin{pmatrix}-\sqrt{3/2}\\0\\\sqrt{3/2}\end{pmatrix}.
$$

With a small positive $\varepsilon$, invariance is approximate. Freeze the selected patch statistics while forming each local linear system, and recompute after updating the warp; if differentiating the full normalized residual instead, include derivatives of those statistics. Reject flat or saturated patches rather than trusting the denominator safeguard to create texture.
````

**Source check / assumptions:** The uploaded key specifically proposes patch mean/std normalization. This method assumes patches have nonzero texture and a roughly affine photometric change. Saturation, shadows and spatially nonuniform lighting can still break the model.


(quiz-source-13)=
## Spring 2019 Quiz 6 — Feature trackability

**Historical source:** `3dcvMid/olderquizzes/cs532s19_quiz6-2.pdf`.

(quiz-13-q1)=
### Problem 1(a–d)

````{original-question}
A binary image contains three black lines meeting at one vertex $v$: horizontal $\ell_h$, vertical $\ell_v$, and a $45^\circ$ line $\ell_s$. There is also one isolated black pixel $p=(x,y,1)$ surrounded by white pixels. (a) Express intersection vertex coordinates in terms of the horizontal/vertical lines. (b) Is the common vertex good to track? (c) What about an arbitrary point along the slanted edge with both $I_x$ and $I_y$ large? (d) Is the isolated black pixel better than a neighboring white pixel?
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Find the junction geometrically
**Why:** Intersecting the two known lines gives its position.

Represent a homogeneous line as $\ell=(a,b,c)^T$, with line equation $ax+by+cw=0$. Two noncoincident lines intersect at their cross product, giving 

$$
\boxed{v\sim \ell_h\times\ell_v}.
$$

 Verify that the diagonal line also passes through the vertex: $\ell_s^Tv=0$.
````

````{solution-step} 2 — Explain why the junction is trackable
**Why:** Multiple gradient directions constrain both motion components.

Use the Harris/KLT structure tensor $M=\sum_W w\nabla I\nabla I^T$. A corner-like intersection provides intensity gradients in multiple directions, making *both* eigenvalues sufficiently large. So $\boxed{\text{yes, the vertex is generally good to track}}$ if patch size/contrast resolve the junction.
````

````{solution-step} 3 — Test the diagonal-edge claim
**Why:** Two nonzero gradient components do not imply two independent directions.

For a straight diagonal edge, gradients may have *both coordinate components* $I_x\ne0$, $I_y\ne0$, but every local gradient is approximately parallel to the same edge normal $g$. Then $M\approx(\sum w\alpha_i^2)gg^T$, a rank-1 matrix with one near-zero eigenvalue. Thus $\boxed{\text{no, not reliably trackable along the edge}}$: the aperture problem remains.
````

````{solution-step} 4 — Compare the dot and neighboring pixel
**Why:** Tracking quality belongs to a window, not to a pixel's color.

For an isolated dot, local intensity changes in both x and y directions; the dot as a *patch* is distinctive. However a nearby white pixel whose tracking *window includes the same dot* sees essentially the same local gradients and is not necessarily worse. So $\boxed{\text{feature quality depends on the patch, not the center pixel color}}$.
````

````{solution-step} 5 — Check what the window contains
**Why:** A flat neighboring window has no useful motion information.

If the tracking window around the neighboring white pixel *misses* the dot completely, then it is flat and poor. The correct answer requires specifying the window and its gradients.
````

````{solution-step} 6 — Work out the line and rank calculations
**Why:** A full matrix shows precisely why the diagonal edge remains ambiguous.

Original algebraic companion to parts (a–c): a horizontal line at $v=v_0$ and vertical line at $u=u_0$ have

$$
\ell_h=\begin{pmatrix}0\\1\\-v_0\end{pmatrix},\quad\ell_v=\begin{pmatrix}1\\0\\-u_0\end{pmatrix},\quad
\ell_h\times\ell_v=\begin{pmatrix}-u_0\\-v_0\\-1\end{pmatrix}\sim\begin{pmatrix}u_0\\v_0\\1\end{pmatrix}.
$$

For $N$ identical diagonal-edge gradients $g=(1,1)^T$, the tracking matrix is

$$
M=N\begin{pmatrix}1\\1\end{pmatrix}\begin{pmatrix}1&1\end{pmatrix}
=N\begin{pmatrix}1&1\\1&1\end{pmatrix}.
$$

Its characteristic equation is $(N-\lambda)^2-N^2=\lambda(\lambda-2N)=0$. One eigenvalue is zero even though both gradient components are nonzero. Motion along the edge cannot be recovered from that patch alone.
````


(quiz-source-a2)=
## A2. Harris response from gradients (L5, slides 11–30)

**Original practice from the supplied booklet; not a historical quiz question.**

(quiz-a2-q1)=
### Illustrative problem

````{original-question}
A small patch contains two gradient vectors $(2,0)^T$ and $(0,3)^T$, equally weighted. Compute its second-moment matrix, eigenvalues, and Harris score for $k=0.04$. Classify it.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Set up the structure tensor
**Why:** Gradient outer products measure changes in every direction.

Construct the unweighted second-moment matrix as the sum of gradient outer products: $M=\sum_i g_ig_i^T$.
````

````{solution-step} 2 — Multiply and add the full matrices
**Why:** The off-diagonal and diagonal entries come from explicit products.

Multiply each $2\times1$ gradient by its $1\times2$ transpose, then add:

$$
\begin{aligned}
g_1g_1^T&=\begin{pmatrix}2\\0\end{pmatrix}\begin{pmatrix}2&0\end{pmatrix}
=\begin{pmatrix}4&0\\0&0\end{pmatrix},\\
g_2g_2^T&=\begin{pmatrix}0\\3\end{pmatrix}\begin{pmatrix}0&3\end{pmatrix}
=\begin{pmatrix}0&0\\0&9\end{pmatrix},\\
M&=\begin{pmatrix}4&0\\0&0\end{pmatrix}+\begin{pmatrix}0&0\\0&9\end{pmatrix}
=\begin{pmatrix}4&0\\0&9\end{pmatrix}.
\end{aligned}
$$

Here equal weights mean both weights are one; averaging instead would scale the eigenvalues and response.
````

````{solution-step} 3 — Read the eigenvalues
**Why:** A diagonal matrix makes the independent gradient strengths visible.

Because $M$ is diagonal, its eigenvalues are $\lambda_1=4$ and $\lambda_2=9$; intensity changes in two independent directions.
````

````{solution-step} 4 — Compute determinant and trace
**Why:** Harris combines these two scalar summaries.

Compute determinant and trace: $\det M=4(9)=36$, $\operatorname{tr}M=4+9=13$.
````

````{solution-step} 5 — Evaluate the Harris response
**Why:** Substitute the supplied k after computing the summaries.

Harris response: $R=\det M-k(\operatorname{tr}M)^2=36-0.04(13)^2=36-6.76=\boxed{29.24}$.
````

````{solution-step} 6 — Classify and select the feature
**Why:** A corner-like score still needs a threshold and nonmaximum suppression.

This positive score is *corner-like*; actual detector selection also requires an image-dependent threshold and spatial nonmaximum suppression. If instead $M=\operatorname{diag}(20,0)$, the response would be $-0.04(20)^2=-16$ (edge-like and singular).
````


(quiz-source-a3)=
## A3. Lucas–Kanade least-squares displacement (L5, slides 39–50)

**Original practice from the supplied booklet; not a historical quiz question.**

(quiz-a3-q1)=
### Illustrative problem

````{original-question}
Two pixels in one small tracked patch have spatial gradients $(I_x,I_y)=(2,0)$ and $(0,3)$, with temporal derivatives $I_t=-4$ and $-3$, respectively. Find the shared displacement $(u,v)$.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Write brightness constancy's linearization
**Why:** Small motion turns each pixel into one linear equation.

Start with linearized brightness constancy at each pixel: $I_xu+I_yv+I_t=0$.
````

````{solution-step} 2 — Substitute both pixels
**Why:** Different gradient directions constrain different displacement components.

Substitute pixel 1: $2u+0v-4=0\Rightarrow 2u=4$. Pixel 2: $0u+3v-3=0\Rightarrow3v=3$.
````

````{solution-step} 3 — Stack the linear system
**Why:** The patch shares one displacement vector.

Write matrix form: $Ad=b$, with 

$$
A=\begin{bmatrix}2&0\\0&3\end{bmatrix}
$$

, $d=(u,v)^T$, $b=(4,3)^T$.
````

````{solution-step} 4 — Multiply out the normal equations
**Why:** This exposes the structure tensor and right-hand side completely.

Multiply the full normal-equation matrices:

$$
A^TA=\begin{pmatrix}2&0\\0&3\end{pmatrix}\begin{pmatrix}2&0\\0&3\end{pmatrix}=\begin{pmatrix}4&0\\0&9\end{pmatrix},
$$

$$
A^Tb=\begin{pmatrix}2&0\\0&3\end{pmatrix}\begin{pmatrix}4\\3\end{pmatrix}=\begin{pmatrix}8\\9\end{pmatrix}.
$$

Thus the two least-squares equations are

$$
\begin{pmatrix}4&0\\0&9\end{pmatrix}\begin{pmatrix}u\\v\end{pmatrix}=\begin{pmatrix}8\\9\end{pmatrix}.
$$
````

````{solution-step} 5 — Solve and verify the displacement
**Why:** A zero residual checks the proposed motion in the stated linear model.

For this diagonal example, show the inverse explicitly:

$$
\begin{pmatrix}u\\v\end{pmatrix}
=\begin{pmatrix}1/4&0\\0&1/9\end{pmatrix}\begin{pmatrix}8\\9\end{pmatrix}
=\begin{pmatrix}8/4\\9/9\end{pmatrix}=\begin{pmatrix}2\\1\end{pmatrix}\,\mathrm{pixels}.
$$

Check $A(2,1)^T-b=(0,0)^T$. In implementations, solve the system rather than explicitly inverting it; use warping/pyramids when the local small-motion approximation is inadequate.
````

````{solution-step} 6 — Connect solvability to corner quality
**Why:** An edge makes the same normal matrix nearly singular.

Notice $A^TA=M$, the same second-moment matrix as in Harris. When both eigenvalues are positive and not too small, the optical-flow estimate is better determined; on an edge one eigenvalue tends toward zero and the aperture problem returns.
````
