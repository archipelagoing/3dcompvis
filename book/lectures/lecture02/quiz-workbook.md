(lec02-quiz-workbook)=
# Original quiz questions and worked solutions

**Read the problem in black. Follow the numbered red steps. Work through the blue mathematics.** Every step explains why it is needed. Matrix calculations show the inputs and intermediate results; written-reasoning questions explain the decision instead of inventing numerical data.

**Source:** the supplied lecture-organized quiz booklet. Full problems follow its wording and givens, with typography normalized; the historical PDF filenames appear below. Source-key corrections and added numerical companions are marked.

**Retests have their own questions and full solutions.** Problems labeled **Original practice** are the booklet’s seven supplemental examples, separate from the 18 historical quizzes. Colored steps remain numbered and readable in grayscale.

## Jump to a quiz

- {ref}`Spring 2020 Quiz 1 — Projective points and camera projection <quiz-source-8>`

---

(quiz-source-8)=
## Spring 2020 Quiz 1 — Projective points and camera projection

**Historical source:** `3dcvMid/olderquizzes/cs532s20_quiz1.pdf`.

(ex-lec02-collinear)=
(quiz-8-q1)=
### Problem 1

````{original-question}
For projective-plane points $a,b,c$, use only dot and cross products to test whether they are collinear. In what case does the test fail?
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Join two projective points
**Why:** The cross product constructs their homogeneous line.

Recall that the homogeneous *line through two distinct points* is their cross product: $\ell=a\times b$.
````

````{solution-step} 2 — Test the third point
**Why:** A point is on a line exactly when their dot product is zero.

A third point $c$ lies on $\ell$ exactly when its dot product with $\ell$ is zero. Thus test $\boxed{c^T(a\times b)=0}$. This equals the determinant of the matrix with columns $a,b,c$.
````

````{solution-step} 3 — Handle repeated points
**Why:** A zero cross product cannot identify a unique joining line.

If $a\sim b$, then $a\times b=0$, so it does not construct a unique line. Choose a distinct pair instead. The determinant still correctly says the three representatives are linearly dependent: any repeated point together with a third point lies on at least one line. A zero homogeneous point itself is invalid.
````

````{solution-step} 4 — Expand a numerical test
**Why:** Actual products show both a passing and a failing candidate.

Original numerical companion: take $a=(0,0,1)^T$, $b=(2,0,1)^T$, $c=(5,0,1)^T$. Then

$$
a\times b=\begin{pmatrix}0(1)-1(0)\\1(2)-0(1)\\0(0)-0(2)\end{pmatrix}
=\begin{pmatrix}0\\2\\0\end{pmatrix},\qquad
c^T(a\times b)=\begin{pmatrix}5&0&1\end{pmatrix}\begin{pmatrix}0\\2\\0\end{pmatrix}=0.
$$

The points lie on $Y=0$. Replacing $c$ by $(5,1,1)^T$ gives $5(0)+1(2)+1(0)=2$, so that point is off the line.
````


(ex-lec02-projection)=
(quiz-8-q2)=
### Problem 2(a–b)

````{original-question}
Let $X=(X,Y,Z,W)^T$ be a homogeneous 3D point and $x\sim MX$ a homogeneous 2D image point. Find (a) the dimensions of $M$; (b) explicit inhomogeneous image coordinates from the entries $m_{ij}$ and $X$.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Count input and output entries
**Why:** Matrix multiplication determines the camera matrix's dimensions.

A 3D homogeneous point has four components; a 2D homogeneous image point has three. Therefore $\boxed{M\in\mathbb R^{3\times4}}$ and $Mx\!$ is *not* the mapping; the correct product is $MX\in\mathbb R^{3\times1}$.
````

````{solution-step} 2 — Multiply the full projection matrix
**Why:** Every output entry is one row dotted with the world point.

Show the full matrix-vector product:

$$
\begin{aligned}
q&=\begin{pmatrix}m_{11}&m_{12}&m_{13}&m_{14}\\m_{21}&m_{22}&m_{23}&m_{24}\\m_{31}&m_{32}&m_{33}&m_{34}\end{pmatrix}
\begin{pmatrix}X\\Y\\Z\\W\end{pmatrix}\\
&=\begin{pmatrix}m_{11}X+m_{12}Y+m_{13}Z+m_{14}W\\m_{21}X+m_{22}Y+m_{23}Z+m_{24}W\\m_{31}X+m_{32}Y+m_{33}Z+m_{34}W\end{pmatrix}.
\end{aligned}
$$
````

````{solution-step} 3 — Divide by the last coordinate
**Why:** Homogeneous image coordinates represent ratios.

A finite homogeneous point represents ratios, so divide the first two entries by the third:

$$
\begin{aligned}
u&=\frac{m_{11}X+m_{12}Y+m_{13}Z+m_{14}W}{m_{31}X+m_{32}Y+m_{33}Z+m_{34}W},\\
v&=\frac{m_{21}X+m_{22}Y+m_{23}Z+m_{24}W}{m_{31}X+m_{32}Y+m_{33}Z+m_{34}W}.
\end{aligned}
$$

For a finite world point choose $W=1$. If $q_3=0$ and $q\ne0$, the result is an ideal image point; if $q=0$, projection is undefined.
````


(ex-lec02-intersections)=
(quiz-8-q3)=
### Problem 3(a–b)

````{original-question}
Let $\ell_1,\ell_2$ be two distinct vertical lines each at distance $d>0$ from the 2D origin, and $\ell_3$ the horizontal line through the origin. Give their homogeneous line vectors and count the possible pairwise intersections.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Represent the vertical lines
**Why:** Their equations fix the signs of the constant coefficients.

Choose $\ell_1:x=d$ and $\ell_2:x=-d$; as $ax+by+c=0$, their vectors are $\boxed{\ell_1=(1,0,-d)^T}$, $\boxed{\ell_2=(1,0,d)^T}$.
````

````{solution-step} 2 — Represent the horizontal line
**Why:** The line through the origin has no constant offset.

For the horizontal line $y=0$, use $\boxed{\ell_3=(0,1,0)^T}$. Line vectors are homogeneous, so nonzero multiples are equivalent.
````

````{solution-step} 3 — Compute both finite intersections
**Why:** Cross products intersect homogeneous lines.

Compute both finite intersections component by component:

$$
\begin{aligned}
\ell_1\times\ell_3&=\begin{pmatrix}0(0)-(-d)(1)\\(-d)(0)-1(0)\\1(1)-0(0)\end{pmatrix}
=\begin{pmatrix}d\\0\\1\end{pmatrix},\\
\ell_2\times\ell_3&=\begin{pmatrix}0(0)-d(1)\\d(0)-1(0)\\1(1)-0(0)\end{pmatrix}
=\begin{pmatrix}-d\\0\\1\end{pmatrix}.
\end{aligned}
$$

Their final coordinates are already one, giving ordinary points $(d,0)$ and $(-d,0)$.
````

````{solution-step} 4 — Intersect the parallel lines
**Why:** A zero last coordinate represents a point at infinity.

The parallel vertical lines give

$$
\ell_1\times\ell_2=\begin{pmatrix}0(d)-(-d)(0)\\(-d)(1)-1(d)\\1(0)-0(1)\end{pmatrix}
=\begin{pmatrix}0\\-2d\\0\end{pmatrix}\sim\begin{pmatrix}0\\1\\0\end{pmatrix}.
$$

The last coordinate is zero, so do not divide: this is a point at infinity in the vertical direction.
````

````{solution-step} 5 — Count in the stated geometry
**Why:** Projective and finite-plane intersection counts differ.

Thus $\boxed{3\text{ projective intersections}}$ among the 3 line pairs, of which $\boxed{2\text{ are finite}}$. Say both numbers to clarify the geometric convention.
````

```{figure} ../../images/lecture02/quiz-lines.*
:width: 70%
:alt: Two finite intersections and one vertical point at infinity.

Two finite intersections and one vertical point at infinity.
```
