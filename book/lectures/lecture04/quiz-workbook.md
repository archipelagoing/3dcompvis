(lec04-quiz-workbook)=
# Original quiz questions and worked solutions

**Read the problem in black. Follow the numbered red steps. Work through the blue mathematics.** Every step explains why it is needed. Matrix calculations show the inputs and intermediate results; written-reasoning questions explain the decision instead of inventing numerical data.

**Source:** the supplied lecture-organized quiz booklet. Full problems follow its wording and givens, with typography normalized; the historical PDF filenames appear below. Source-key corrections and added numerical companions are marked.

**Retests have their own questions and full solutions.** Problems labeled **Original practice** are the booklet’s seven supplemental examples, separate from the 18 historical quizzes. Colored steps remain numbered and readable in grayscale.

## Jump to a quiz

- {ref}`Older Quiz 4 — Epipolar line and constraint <quiz-source-1>`
- {ref}`Spring 2019 Quiz 4 — Duplicate epipolar retest <quiz-source-2>`
- {ref}`Fall 2025 Quiz 2 — Three-view epipolar geometry <quiz-source-3>`
- {ref}`Fall 2025 Quiz 3 — Stereo depth sensitivity <quiz-source-4>`
- {ref}`Spring 2019 Quiz 5 — Exact stereo errors <quiz-source-5>`
- {ref}`Spring 2020 Quiz 5 — Repeat disparity test <quiz-source-6>`
- {ref}`A4. Essential matrix and cheirality (L4, slides 22–41) <quiz-source-a4>`

---

(quiz-source-1)=
## Older Quiz 4 — Epipolar line and constraint

**Historical source:** `3dcvMid/olderquizzes/cs532f15_quiz4.pdf`.

**Header note:** this filename contains “2015”; the PDF is printed Spring 2019.

(ex-lec04-symbolic)=
(quiz-1-q1)=
### Problem 1

````{original-question}
Let $x_A=(x,y,w)^T$ be a point in image A and $F_{AB}=[f_{ij}]$ be the fundamental matrix from image A to B. Write the epipolar-line equation in B, using both matrix entries and the row vectors $\mathbf f_1^T,\mathbf f_2^T,\mathbf f_3^T$. Make an illustrative sketch.
````

**Given / relevant facts:**

$$
F_{AB}=\begin{bmatrix}f_{11}&f_{12}&f_{13}\\f_{21}&f_{22}&f_{23}\\f_{31}&f_{32}&f_{33}\end{bmatrix}
$$

A homogeneous line is $\ell_B=(a,b,c)^T$.

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Choose the point-to-line rule
**Why:** F maps the known point to possible matches in the other image.

Start from the fundamental-matrix point-to-line relation: $\ell_B=F_{AB}x_A$. This is a line, not the matched pixel itself.
````

````{solution-step} 2 — Multiply all three rows
**Why:** The resulting column contains line coefficients.

Multiply each row of the full matrix by the input column:

$$
\begin{aligned}
\ell_B&=\begin{pmatrix}f_{11}&f_{12}&f_{13}\\f_{21}&f_{22}&f_{23}\\f_{31}&f_{32}&f_{33}\end{pmatrix}
\begin{pmatrix}x\\y\\w\end{pmatrix}\\
&=\begin{pmatrix}f_{11}x+f_{12}y+f_{13}w\\f_{21}x+f_{22}y+f_{23}w\\f_{31}x+f_{32}y+f_{33}w\end{pmatrix}
=\begin{pmatrix}\mathbf f_1^Tx_A\\\mathbf f_2^Tx_A\\\mathbf f_3^Tx_A\end{pmatrix}.
\end{aligned}
$$

The output entries are line coefficients $(a,b,c)^T$, not point coordinates.
````

````{solution-step} 3 — Enforce point-line incidence
**Why:** A true candidate must give a zero scalar dot product.

A candidate $x_B=(u_B,v_B,w_B)^T$ lies on that line when its dot product is zero:

$$
\begin{aligned}
0=x_B^T\ell_B
&=(f_{11}x+f_{12}y+f_{13}w)u_B\\
&\quad +(f_{21}x+f_{22}y+f_{23}w)v_B\\
&\quad +(f_{31}x+f_{32}y+f_{33}w)w_B.
\end{aligned}
$$

For a finite point set $w_B=1$, giving $au_B+bv_B+c=0$. If $b\ne0$, rewrite it as $v_B=-(a/b)u_B-c/b$ for plotting; $b=0$ instead gives a vertical line when $a\ne0$.
````

````{solution-step} 4 — Draw the predicted line
**Why:** One point generally predicts a line rather than a unique match.

If the point is finite, set $w_B=1$; plot $au_B+bv_B+c=0$. For $b\neq0$, $v_B=-(a/b)u_B-c/b$. Draw a line in image B through the unknown match; its exact location depends on the supplied $F_{AB}$ and $x_A$.
````

```{figure} ../../images/quizzes/epipolar-plane.*
:width: 70%
:alt: The supplied booklet’s schematic shows the two cameras, corresponding rays and epipolar plane. The line’s slant is illustrative; in 3D it is the intersection of that plane with image plane B.

The supplied booklet’s schematic shows the two cameras, corresponding rays and epipolar plane. The line’s slant is illustrative; in 3D it is the intersection of that plane with image plane B.
```


(quiz-1-q2)=
### Problem 2

````{original-question}
Write the explicit epipolar constraint $x_B^TF_{AB}x_A=0$ for $x_A=(1,0,1)^T$ and $x_B=(0,1,1)^T$. Rewrite it using row-vector dot products.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Multiply F by the assigned point
**Why:** The zero middle coordinate removes the second column's contribution.

Multiply the actual point into the full symbolic matrix:

$$
\begin{aligned}
F_{AB}x_A&=\begin{pmatrix}f_{11}&f_{12}&f_{13}\\f_{21}&f_{22}&f_{23}\\f_{31}&f_{32}&f_{33}\end{pmatrix}\begin{pmatrix}1\\0\\1\end{pmatrix}\\
&=\begin{pmatrix}f_{11}(1)+f_{12}(0)+f_{13}(1)\\f_{21}(1)+f_{22}(0)+f_{23}(1)\\f_{31}(1)+f_{32}(0)+f_{33}(1)\end{pmatrix}
=\begin{pmatrix}f_{11}+f_{13}\\f_{21}+f_{23}\\f_{31}+f_{33}\end{pmatrix}.
\end{aligned}
$$
````

````{solution-step} 2 — Dot with the second point
**Why:** Its row selects the second and third line coefficients.

Transpose the other point and multiply the row by that column:

$$
\begin{aligned}
x_B^TF_{AB}x_A
&=\begin{pmatrix}0&1&1\end{pmatrix}\begin{pmatrix}f_{11}+f_{13}\\f_{21}+f_{23}\\f_{31}+f_{33}\end{pmatrix}\\
&=0(f_{11}+f_{13})+1(f_{21}+f_{23})+1(f_{31}+f_{33}).
\end{aligned}
$$

The result is a scalar: $(1\times3)(3\times1)=1\times1$.
````

````{solution-step} 3 — Set the scalar to zero
**Why:** This is the required epipolar constraint on the unknown entries.

Enforce incidence: 

$$
\boxed{f_{21}+f_{23}+f_{31}+f_{33}=0}.
$$
````

````{solution-step} 4 — Rewrite with row-vector products
**Why:** The compact row notation must express the same scalar equation.

Rewrite using the supplied row vectors: $x_B^TFx_A=(\mathbf f_2^T+\mathbf f_3^T)x_A=\mathbf f_2\cdot x_A+\mathbf f_3\cdot x_A=0$.
````

**Source check / assumptions:** The quiz provides symbolic $F$, so no individual numeric $f_{ij}$ values can be solved; the requested result is a constraint on the entries.


(quiz-source-2)=
## Spring 2019 Quiz 4 — Duplicate epipolar retest

**Historical source:** `3dcvMid/olderquizzes/cs532s19_quiz4.pdf`.

(quiz-2-q1)=
### Problem 1

````{original-question}
Given $x_A=(x,y,w)^T$ and the rows $\mathbf f_1^T,\mathbf f_2^T,\mathbf f_3^T$ of $F_{AB}$, express its epipolar line in image B and make a sketch.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Check mapping direction
**Why:** A point in A must generate a line in B.

Choose the correct direction: $F_{AB}$ maps a *point in A* to a *line in B*; compute $\ell_B=F_{AB}x_A$.
````

````{solution-step} 2 — Expand the matrix multiplication
**Why:** Each row supplies one coefficient of that line.

Multiply each row of the full matrix by the input column:

$$
\begin{aligned}
\ell_B&=\begin{pmatrix}f_{11}&f_{12}&f_{13}\\f_{21}&f_{22}&f_{23}\\f_{31}&f_{32}&f_{33}\end{pmatrix}
\begin{pmatrix}x\\y\\w\end{pmatrix}\\
&=\begin{pmatrix}f_{11}x+f_{12}y+f_{13}w\\f_{21}x+f_{22}y+f_{23}w\\f_{31}x+f_{32}y+f_{33}w\end{pmatrix}
=\begin{pmatrix}\mathbf f_1^Tx_A\\\mathbf f_2^Tx_A\\\mathbf f_3^Tx_A\end{pmatrix}.
\end{aligned}
$$

The output entries are line coefficients $(a,b,c)^T$, not point coordinates.
````

````{solution-step} 3 — Write the complete line equation
**Why:** Incidence converts the coefficient vector into a condition on a candidate point.

A candidate $x_B=(u_B,v_B,w_B)^T$ lies on that line when its dot product is zero:

$$
\begin{aligned}
0=x_B^T\ell_B
&=(f_{11}x+f_{12}y+f_{13}w)u_B\\
&\quad +(f_{21}x+f_{22}y+f_{23}w)v_B\\
&\quad +(f_{31}x+f_{32}y+f_{33}w)w_B.
\end{aligned}
$$

For a finite point set $w_B=1$, giving $au_B+bv_B+c=0$. If $b\ne0$, rewrite it as $v_B=-(a/b)u_B-c/b$ for plotting; $b=0$ instead gives a vertical line when $a\ne0$.
````

````{solution-step} 4 — Make the requested sketch
**Why:** The camera rays and image line explain the algebra geometrically.

Sketch two camera centers joined by a baseline, their image planes, a common 3D point and both rays; label the line in image B that contains the possible match. The same diagram as on the preceding page applies.
````

```{figure} ../../images/quizzes/epipolar-plane.*
:width: 70%
:alt: The same schematic is reproduced beside this separate retest. The camera rays and baseline lie in one epipolar plane.

The same schematic is reproduced beside this separate retest. The camera rays and baseline lie in one epipolar plane.
```


(quiz-2-q2)=
### Problem 2

````{original-question}
For $x_A=(1,0,1)^T$ and $x_B=(0,1,1)^T$, expand $x_B^TF_{AB}x_A=0$ and express it in terms of row vectors.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Multiply the known point into F
**Why:** This selects and adds columns one and three.

Multiply the actual point into the full symbolic matrix:

$$
\begin{aligned}
F_{AB}x_A&=\begin{pmatrix}f_{11}&f_{12}&f_{13}\\f_{21}&f_{22}&f_{23}\\f_{31}&f_{32}&f_{33}\end{pmatrix}\begin{pmatrix}1\\0\\1\end{pmatrix}\\
&=\begin{pmatrix}f_{11}(1)+f_{12}(0)+f_{13}(1)\\f_{21}(1)+f_{22}(0)+f_{23}(1)\\f_{31}(1)+f_{32}(0)+f_{33}(1)\end{pmatrix}
=\begin{pmatrix}f_{11}+f_{13}\\f_{21}+f_{23}\\f_{31}+f_{33}\end{pmatrix}.
\end{aligned}
$$
````

````{solution-step} 2 — Perform the final row-column product
**Why:** Only two output coefficients contribute.

Transpose the other point and multiply the row by that column:

$$
\begin{aligned}
x_B^TF_{AB}x_A
&=\begin{pmatrix}0&1&1\end{pmatrix}\begin{pmatrix}f_{11}+f_{13}\\f_{21}+f_{23}\\f_{31}+f_{33}\end{pmatrix}\\
&=0(f_{11}+f_{13})+1(f_{21}+f_{23})+1(f_{31}+f_{33}).
\end{aligned}
$$

The result is a scalar: $(1\times3)(3\times1)=1\times1$.
````

````{solution-step} 3 — Enforce the zero constraint
**Why:** Correspondence requires incidence, not equality between a point and a line.

Set the scalar to zero: $\boxed{f_{21}+f_{23}+f_{31}+f_{33}=0}$.
````

````{solution-step} 4 — Express the row-vector form
**Why:** This checks the equivalent notation requested by the quiz.

In row notation, $\boxed{(\mathbf f_2^T+\mathbf f_3^T)x_A=0}$; this is one scalar epipolar incidence constraint.
````


(quiz-source-3)=
## Fall 2025 Quiz 2 — Three-view epipolar geometry

**Historical source:** `3dcvMid/quizzesf25sol/cs532f25_quiz_2_solution.pdf`.

(ex-lec04-third-view)=
(quiz-3-q1)=
### Question 1

````{original-question}
Three images A, B, C observe a point. The pair $x_A\leftrightarrow x_B$ is known, but its image location $x_C$ is unknown. Given fundamental matrices $F_{AC}$ and $F_{BC}$ (which map A/B points to lines in C), determine $x_C$.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Predict the line from image A
**Why:** The unknown point in C must satisfy the A-to-C geometry.

Map $x_A$ to a line in C: $\boxed{\ell_C^{(A)}=F_{AC}x_A}$. Any correct $x_C$ must satisfy $x_C^T\ell_C^{(A)}=0$.
````

````{solution-step} 2 — Predict the line from image B
**Why:** A second independent view supplies another constraint in the same image C.

Map $x_B$ independently to a second line in C: $\boxed{\ell_C^{(B)}=F_{BC}x_B}$. The same $x_C$ must satisfy $x_C^T\ell_C^{(B)}=0$.
````

````{solution-step} 3 — Intersect the two lines
**Why:** Their cross product gives the homogeneous intersection.

In the projective plane, the intersection of two lines is their cross product: 

$$
\boxed{x_C\sim \ell_C^{(A)}\times\ell_C^{(B)}}.
$$
````

````{solution-step} 4 — Normalize and check the intersection
**Why:** Homogeneous coordinates must be converted before reading a finite pixel.

Normalize $x_C=(q_1,q_2,q_3)^T$ to $(q_1/q_3,q_2/q_3)$ if $q_3\ne0$. Check both incidence products equal zero. If the two lines coincide, they do not determine a unique point; with noisy lines use an appropriate least-squares estimate.
````

````{solution-step} 5 — Define a numerical companion
**Why:** The original symbolic question has no numerical matrices to multiply.

Original numerical companion: let $x_A=(1/2,3/4,1)^T$, $x_B=(1/4,3/4,1)^T$, and

$$
F_{AC}=\begin{pmatrix}0&0&-1\\0&0&0\\1&0&0\end{pmatrix},\quad
F_{BC}=\begin{pmatrix}0&0&-1\\0&0&-1\\1&1&0\end{pmatrix}.
$$

These are compatible with identity-oriented normalized cameras centered at $(0,0,0)$, $(1,0,0)$, $(0,1,0)$ observing world point $(2,3,4)$.
````

````{solution-step} 6 — Multiply both numerical matrices
**Why:** Full row products show exactly where both predicted lines come from.

Multiply both matrices, retaining every row operation:

$$
\begin{aligned}
\ell_C^{(A)}&=\begin{pmatrix}0&0&-1\\0&0&0\\1&0&0\end{pmatrix}\begin{pmatrix}1/2\\3/4\\1\end{pmatrix}
=\begin{pmatrix}0(1/2)+0(3/4)-1\\0\\1(1/2)+0+0\end{pmatrix}
=\begin{pmatrix}-1\\0\\1/2\end{pmatrix},\\
\ell_C^{(B)}&=\begin{pmatrix}0&0&-1\\0&0&-1\\1&1&0\end{pmatrix}\begin{pmatrix}1/4\\3/4\\1\end{pmatrix}
=\begin{pmatrix}-1\\-1\\1/4+3/4\end{pmatrix}
=\begin{pmatrix}-1\\-1\\1\end{pmatrix}.
\end{aligned}
$$
````

````{solution-step} 7 — Expand the cross product
**Why:** Its three components determine the common image point.

Intersect the two lines by expanding the cross product:

$$
x_C\sim\begin{pmatrix}-1\\0\\1/2\end{pmatrix}\times\begin{pmatrix}-1\\-1\\1\end{pmatrix}
=\begin{pmatrix}0(1)-(1/2)(-1)\\(1/2)(-1)-(-1)(1)\\(-1)(-1)-0(-1)\end{pmatrix}
=\begin{pmatrix}1/2\\1/2\\1\end{pmatrix}.
$$

Divide by the last coordinate to get $(u_C,v_C)=(1/2,1/2)$. A scaled result $(4,4,8)^T$ gives the same ratios.
````

````{solution-step} 8 — Substitute into both lines
**Why:** Both independent constraints must pass at the answer.

Check both original line equations at the answer:

$$
\begin{aligned}
(\ell_C^{(A)})^Tx_C&=(-1)(1/2)+0(1/2)+(1/2)(1)=0,\\
(\ell_C^{(B)})^Tx_C&=(-1)(1/2)+(-1)(1/2)+(1)(1)=0.
\end{aligned}
$$

Coincident lines give a zero cross product and no unique point. Distinct parallel lines meet at infinity; nearly parallel lines make a finite intersection sensitive to noise. Image appearance must still confirm visibility and identity.
````

```{figure} ../../images/lecture04/third-view.*
:width: 70%
:alt: The two numerical companion lines intersect at the predicted third-image point.

The two numerical companion lines intersect at the predicted third-image point.
```


(ex-lec04-invalid-f)=
(quiz-3-q2)=
### Question 2

````{original-question}
Given $x'=(1,2,1)^T$ and 

$$
F=\begin{bmatrix}1&2&1\\0&1&2\\1&0&1\end{bmatrix}
$$

, propose an epipolar-consistent point $x$.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Choose the unprimed-image line
**Why:** The transpose maps the primed point back to a line in the unprimed image.

Start from $\boxed{x'^TFx=0}$. To obtain the possible locations of $x$, form the line $\ell=F^Tx'$ in the *unprimed* image.
````

````{solution-step} 2 — Transpose and multiply explicitly
**Why:** The line coefficients come from row-column products.

Transpose explicitly, then multiply row by row:

$$
F^T=\begin{pmatrix}1&0&1\\2&1&0\\1&2&1\end{pmatrix},\qquad
F^Tx'=\begin{pmatrix}1(1)+0(2)+1(1)\\2(1)+1(2)+0(1)\\1(1)+2(2)+1(1)\end{pmatrix}
=\begin{pmatrix}2\\4\\6\end{pmatrix}.
$$
````

````{solution-step} 3 — Write the incidence equation
**Why:** A candidate must make the dot product zero.

Write line incidence for $x=(u,v,1)^T$: $2u+4v+6=0$, or $\boxed{u+2v+3=0}$.
````

````{solution-step} 4 — Choose a convenient finite point
**Why:** One free coordinate remains because the answer is a whole line.

Choose a convenient solution, e.g. $v=0\Rightarrow u=-3$. Thus $\boxed{x=(-3,0,1)^T}$. Alternatively $u=-1\Rightarrow v=-1$.
````

````{solution-step} 5 — Check the answer and the matrix rank
**Why:** Solving the given equation does not make an invalid matrix physically valid.

Verify the point by multiplying it into the original supplied matrix:

$$
Fx=\begin{pmatrix}1&2&1\\0&1&2\\1&0&1\end{pmatrix}\begin{pmatrix}-3\\0\\1\end{pmatrix}
=\begin{pmatrix}-3+0+1\\0+0+2\\-3+0+1\end{pmatrix}
=\begin{pmatrix}-2\\2\\-2\end{pmatrix},
$$

$$
x'^TFx=\begin{pmatrix}1&2&1\end{pmatrix}\begin{pmatrix}-2\\2\\-2\end{pmatrix}=-2+4-2=0.
$$

But $\det F=1(1)-2(-2)+1(-1)=4$, so its rank is three. The point solves the supplied equation; this matrix is not a valid fundamental matrix for pinhole cameras.
````

**Source check / assumptions:** The uploaded solution writes $x'^TF=x$; that is dimensionally/conceptually inaccurate. $x'^TF$ is a *line row-vector*, not a specific corresponding image point. There are infinitely many epipolar-consistent points on this line. Note that a true fundamental matrix must have rank 2; the numerical matrix given in the quiz is nonsingular, but its scalar incidence equation remains solvable as requested.


(quiz-source-4)=
## Fall 2025 Quiz 3 — Stereo depth sensitivity

**Historical source:** `3dcvMid/quizzesf25sol/cs532f25_quiz_3_solution.pdf`.

(ex-lec04-stereo-fall)=
(quiz-4-q1)=
### Question 1

````{original-question}
Rectified stereo cameras have baseline $b=10$ cm, common focal length $f=50$ pixels, and true disparity $d^*=25$ pixels. Determine the depth error caused by a 1-pixel disparity mistake.
````

**Given / relevant facts:**

Use $Z=bf/d$. The problem does not say whether disparity is over- or underestimated, so compute both; the supplied key uses a first-order approximate magnitude.

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Compute the true depth
**Why:** We need a reference before defining an error.

Keep physical units consistent: $bf=(10\,\mathrm{cm})(50\,\mathrm{px})=500\,\mathrm{cm\,px}$. True depth: 

$$
Z^*=500/25=\boxed{20\,\mathrm{cm}}.
$$
````

````{solution-step} 2 — Calculate the underestimated-disparity case
**Why:** A smaller positive disparity should reconstruct a farther point.

For $\delta=-1$, measured disparity is $24$ pixels:

$$
\widehat Z_- =\frac{500}{24}=\frac{125}{6}\,\mathrm{cm},\qquad
\Delta Z_- =\frac{125}{6}-20=\frac{125-120}{6}=\frac56\,\mathrm{cm}\approx+0.83333\,\mathrm{cm}.
$$
````

````{solution-step} 3 — Calculate the overestimated-disparity case
**Why:** A larger disparity should reconstruct a nearer point.

For $\delta=+1$, measured disparity is $26$ pixels:

$$
\widehat Z_+ =\frac{500}{26}=\frac{250}{13}\,\mathrm{cm},\qquad
\Delta Z_+ =\frac{250}{13}-20=\frac{250-260}{13}=-\frac{10}{13}\,\mathrm{cm}\approx-0.76923\,\mathrm{cm}.
$$
````

````{solution-step} 4 — Compare the first-order approximation
**Why:** The derivative estimates a small change rather than both exact nonlinear errors.

To obtain the first-order approximation, differentiate $Z(d)=bf/d$: 

$$
\frac{dZ}{dd}=-\frac{bf}{d^2},\quad \Delta Z\approx-\frac{500}{25^2}\Delta d=-0.8\Delta d\ \mathrm{cm}.
$$

 Thus the *approximate magnitude* is $\boxed{0.8\,\mathrm{cm}}$ for $|\Delta d|=1$.
````

**Source check / assumptions:** The exact errors are asymmetric ($+0.8333$ and $-0.7692$ cm), whereas the linearized approximation gives $\pm0.8$ cm. The source key reports the approximation, not both exact cases.

```{figure} ../../images/lecture04/depth-sensitivity.*
:width: 70%
:alt: The same pixel error produces much larger depth errors at smaller disparity.

The same pixel error produces much larger depth errors at smaller disparity.
```


(ex-lec04-search)=
(quiz-4-q2)=
### Question 2

````{original-question}
For the same setup, restrict the searched 3D depth range to between 1 m and 5 m. What disparity interval corresponds to this?
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Convert the baseline to meters
**Why:** Depth and baseline must use the same physical unit.

Convert baseline: $b=10\,\mathrm{cm}=0.1\,\mathrm m$. Then $bf=0.1(50)=5\,\mathrm{m\,px}$.
````

````{solution-step} 2 — Invert the depth formula
**Why:** Search limits are requested in disparity rather than depth.

Invert the depth equation: $d=bf/Z$. Larger depth implies smaller disparity.
````

````{solution-step} 3 — Evaluate the far endpoint
**Why:** The farthest permitted point gives the smallest positive disparity.

At farthest depth $Z_{\max}=5$ m: $d_{\min}=5/5=\boxed{1\,\mathrm{px}}$.
````

````{solution-step} 4 — Evaluate the near endpoint
**Why:** The nearest permitted point gives the largest disparity.

At nearest depth $Z_{\min}=1$ m: $d_{\max}=5/1=\boxed{5\,\mathrm{px}}$. Search $\boxed{d\in[1,5]\,\mathrm{px}}$.
````


(quiz-source-5)=
## Spring 2019 Quiz 5 — Exact stereo errors

**Historical source:** `3dcvMid/olderquizzes/cs532s19_quiz5-2.pdf`.

(ex-lec04-stereo-spring)=
(quiz-5-q1)=
### Problem 1(a–c)

````{original-question}
Rectified cameras have baseline $b=10$ cm and focal length $f=5$ pixels. True disparity is $d^*=3$ pixels. (a) Find the depth error when disparity is underestimated by one pixel; (b) when overestimated by one pixel; (c) explain whether these errors remain constant at larger disparity.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Insert focal length and baseline
**Why:** Their product determines the depth scale.

Write the depth-disparity law and insert the givens: $Z(d)=bf/d=(10)(5)/d=50/d\ \mathrm{cm}$.
````

````{solution-step} 2 — Compute the true depth
**Why:** Signed errors are measured relative to this value.

True depth is $Z^*=50/3=\boxed{16\tfrac23\,\mathrm{cm}}\approx16.6667$ cm.
````

````{solution-step} 3 — Underestimate disparity by one
**Why:** Subtract exact fractions before rounding the error.

Underestimate disparity by one: $\widehat d=3-1=2$. Then

$$
\widehat Z=\frac{50}{2}=25\,\mathrm{cm},\qquad
\Delta Z=25-\frac{50}{3}=\frac{75-50}{3}=\frac{25}{3}\,\mathrm{cm}\approx+8.3333\,\mathrm{cm}.
$$

A positive signed error means the estimated point is too far away.
````

````{solution-step} 4 — Overestimate disparity by one
**Why:** The nonlinear inverse relation produces a different error magnitude.

Overestimate disparity by one: $\widehat d=3+1=4$. Then

$$
\widehat Z=\frac{50}{4}=\frac{25}{2}\,\mathrm{cm},\qquad
\Delta Z=\frac{25}{2}-\frac{50}{3}=\frac{75-100}{6}=-\frac{25}{6}\,\mathrm{cm}\approx-4.1667\,\mathrm{cm}.
$$

A negative signed error means the estimate is too near. The two magnitudes are unequal.
````

````{solution-step} 5 — Generalize the two exact errors
**Why:** Their denominators show how the magnitudes change with disparity.

No: $Z(d)=bf/d$ is nonlinear. The exact error for +1 px is $Z(d+1)-Z(d)=-bf/[d(d+1)]$; for -1 px it is $Z(d-1)-Z(d)=+bf/[d(d-1)]$ for $d>1$. Both magnitudes diminish at larger $d$.
````

````{solution-step} 6 — Interpret the local derivative
**Why:** It explains the trend for small perturbations.

The derivative $dZ/dd=-bf/d^2$ gives the local approximation $|\Delta Z|\approx bf|\Delta d|/d^2$. Because $1/d^2$ decreases as $d$ grows, disparity errors cause smaller depth errors for nearer points.
````


(quiz-source-6)=
## Spring 2020 Quiz 5 — Repeat disparity test

**Historical source:** `3dcvMid/olderquizzes/cs532s20_quiz5.pdf`.

**Header note:** the supplied PDF contains mixed/overprinted year labels. The filename and separate retest entry are retained.

(quiz-6-q1)=
### Problem 1(a–c)

````{original-question}
Rectified stereo cameras: $b=10$ cm, $f=5$ pixels, true $d^*=3$ pixels. Determine (a) error for $\hat d=2$, (b) error for $\hat d=4$, and (c) how errors behave as disparity increases.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Set up the stereo depth law
**Why:** The same physical and pixel units must be used consistently.

Write $Z(d)=bf/d$, using $bf=(10\,\mathrm{cm})(5\,\mathrm{px})=50\,\mathrm{cm\,px}$.
````

````{solution-step} 2 — Find the true depth
**Why:** This is the reference for both signed errors.

True depth: $Z^*=50/3=16.6667$ cm.
````

````{solution-step} 3 — Solve the smaller-disparity case
**Why:** A common denominator makes the positive error explicit.

Underestimate disparity by one: $\widehat d=3-1=2$. Then

$$
\widehat Z=\frac{50}{2}=25\,\mathrm{cm},\qquad
\Delta Z=25-\frac{50}{3}=\frac{75-50}{3}=\frac{25}{3}\,\mathrm{cm}\approx+8.3333\,\mathrm{cm}.
$$

A positive signed error means the estimated point is too far away.
````

````{solution-step} 4 — Solve the larger-disparity case
**Why:** The exact subtraction exposes the unequal negative error.

Overestimate disparity by one: $\widehat d=3+1=4$. Then

$$
\widehat Z=\frac{50}{4}=\frac{25}{2}\,\mathrm{cm},\qquad
\Delta Z=\frac{25}{2}-\frac{50}{3}=\frac{75-100}{6}=-\frac{25}{6}\,\mathrm{cm}\approx-4.1667\,\mathrm{cm}.
$$

A negative signed error means the estimate is too near. The two magnitudes are unequal.
````

````{solution-step} 5 — Explain the asymmetry
**Why:** Equal disparity changes do not give equal changes in inverse disparity.

Explain why the two numbers differ: $Z$ is proportional to $1/d$, not linear in $d$; changes of +1 and -1 around the same $d$ need not have equal effects.
````

````{solution-step} 6 — State the large-disparity trend
**Why:** The derivative and exact formula both predict decreasing sensitivity.

Generalize: $\frac{dZ}{dd}=-bf/d^2$, so a fixed disparity error typically matters less at larger disparities. For exact +1 px, $\Delta Z=-bf/[d(d+1)]$.
````


(quiz-source-a4)=
## A4. Essential matrix and cheirality (L4, slides 22–41)

**Original practice from the supplied booklet; not a historical quiz question.**

(quiz-a4-q1)=
### Illustrative problem

````{original-question}
Two calibrated cameras have relative rotation $R=I$ and translation $t=(1,0,0)^T$ in compatible normalized units. Form $E$, identify its rank and singular values, and explain why pose decomposition is not unique without a positive-depth test.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Write the essential-matrix construction
**Why:** Translation and rotation determine the calibrated two-view relation.

The essential matrix is $\boxed{E=[t]_\times R}$, with cross-product matrix 

$$
[t]_\times=\begin{bmatrix}0&-t_z&t_y\\t_z&0&-t_x\\-t_y&t_x&0\end{bmatrix}
$$

.
````

````{solution-step} 2 — Insert the translation and rotation
**Why:** The cross-product matrix fixes every entry.

Insert $t=(1,0,0)^T$ and $R=I$: 

$$
\boxed{E=\begin{bmatrix}0&0&0\\0&0&-1\\0&1&0\end{bmatrix}}.
$$
````

````{solution-step} 3 — Multiply E transpose by E
**Why:** Its eigenvalues determine E's singular values.

Compute the singular-value check from the complete product:

$$
\begin{aligned}
E^TE&=\begin{pmatrix}0&0&0\\0&0&1\\0&-1&0\end{pmatrix}
\begin{pmatrix}0&0&0\\0&0&-1\\0&1&0\end{pmatrix}\\
&=\begin{pmatrix}0&0&0\\0&1&0\\0&0&1\end{pmatrix}.
\end{aligned}
$$

Its eigenvalues are $1,1,0$, so the singular values of $E$ are their nonnegative square roots: $1,1,0$. Two are nonzero, hence rank two.
````

````{solution-step} 4 — Connect calibrated and pixel coordinates
**Why:** Intrinsic matrices convert between the essential and fundamental relations.

For calibrated normalized image coordinates $\hat x,\hat x'$, corresponding points satisfy $\hat x'^TE\hat x=0$. If pixel intrinsics are known, $E=K_R^TFK_L$.
````

````{solution-step} 5 — List the pose ambiguity
**Why:** The SVD gives two rotations and two translation signs.

Decomposing a general essential matrix via SVD gives two rotation candidates $R_1,R_2$ and a translation *direction* with two signs, i.e. four candidates $(R_1,+t)$, $(R_1,-t)$, $(R_2,+t)$, $(R_2,-t)$.
````

````{solution-step} 6 — Apply the positive-depth test
**Why:** The visible scene must lie in front of both observing cameras.

Triangulate one or more matched 3D points under each candidate. Keep the one for which the points have positive camera-frame $Z$ in *both* views (cheirality). The magnitude of $t$ remains unobservable without external scale.
````
