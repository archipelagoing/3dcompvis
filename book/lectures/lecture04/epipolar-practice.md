(lec04-epipolar-practice)=
# Epipolar geometry: visual guide and worked quiz examples

**You know a point in the first photo. Where should you look in the second?** Epipolar geometry narrows the search from a whole image to **one line**. It does not choose the correct match on that line; appearance or another view must finish the job.

**Jump to a calculation:** [point → line](#epipolar-point-line), [test candidate matches](#epipolar-test-match), [reverse direction and epipoles](#epipolar-reverse), [Quiz 4: symbolic expansion](#ex-lec04-symbolic), [Quiz 2: third-view intersection](#ex-lec04-third-view), [Quiz 2: supplied-matrix correction](#ex-lec04-invalid-f). Then continue to [stereo depth, sensitivity and signed errors](stereo.md).

The [Lecture 2 formula reference](../lecture02/two-view.md) remains the canonical introduction. Here we work through the geometry and arithmetic slowly enough to use those formulas in an exam.

**Sources:** lecture PDF pages 18–21; `cs532f15_quiz4.pdf` and `cs532s19_quiz4.pdf`, P1–P2, PDF page 1, both printed Spring 2019 Quiz 4; Fall 2025 Quiz 2, `cs532f25_quiz_2_solution.pdf`, Q1–Q2, PDF page 1.

(epipolar-ray-plane)=
## Why a point turns into a line

Imagine a lamp seen by two cameras. In image A you click its tip.

1. **One pixel gives a ray, not a depth.** The tip could be anywhere along the ray from camera A through that pixel.
2. **Add camera B.** The ray and the two camera centers define an **epipolar plane** (except when the ray is the baseline itself).
3. **Slice image B with that plane.** Their intersection is the **epipolar line**. Every possible position along A's ray projects onto this line in B.
4. **Find the actual match.** Compare image content along the line. The two viewing rays can then locate the 3D point; noisy rays require triangulation with an error criterion.

**The useful shortcut:** a two-dimensional image search becomes a one-dimensional line search. A point on the line is *geometrically possible*, not necessarily the same physical feature.

```{figure} ../../images/lecture04/epipolar-search.*
:name: fig-lec04-epipolar-search
:width: 95%
:alt: One known pixel in image A predicts the sloping line u minus four v plus seven equals zero in image B. Two candidates lie on the line and one lies off it.

One known pixel predicts a whole line. The numbers are worked out below; the two orange candidates pass the geometry test, so appearance must distinguish them.
```

**Keep these words straight:** the **baseline** joins the camera centers. An **epipole** is the other camera center's image; all epipolar lines in that image pass through it. For parallel rectified cameras, the epipoles are at infinity and the lines are horizontal. General epipolar lines can slope.

```{index} Epipolar geometry
```

```{index} Fundamental matrix
```

## Read the symbols before multiplying

| Symbol | Shape | Meaning |
| --- | --- | --- |
| $x_A=(u_A,v_A,1)^T$ | $3\times1$ | Known finite image point, in homogeneous coordinates |
| $F_{AB}$ | $3\times3$ | Fundamental matrix mapping a point in A to a line in B |
| $\ell_B=(a,b,c)^T$ | $3\times1$ | Line coefficients, meaning $au_B+bv_B+c=0$ |
| $x_B=(u_B,v_B,1)^T$ | $3\times1$ | A candidate point in B |
| $x_B^T\ell_B$ | $1\times1$ | A scalar: zero exactly when the candidate lies on the line |

The superscript $T$ **transposes** a column into a row. A row times a column means multiply matching entries and add. A matrix times a column repeats that operation for each row. The last coordinate $1$ lets the constant term $c$ participate in the same multiplication.

```{raw} latex
\Needspace{7\baselineskip}
```

```{tip}
**Point → line → test.** First compute $\ell_B=F_{AB}x_A$. Then test $x_B^T\ell_B=0$. The first result has three entries; the second has just one. Neither calculation gives depth by itself.
```

The familiar constraint $x_B^TF_{AB}x_A=0$ simply combines those two steps. Its canonical formula and application box is {eq}`eq-lec02-fundamental`. We use the convention that the subscript $AB$ means **point in A → line in B** throughout this chapter.

(epipolar-point-line)=
## Guided calculation A: multiply a point into its epipolar line

Use this original, valid rank-two fundamental matrix and known point:

$$
F_{AB}=\begin{pmatrix}-1&0&2\\0&-1&-1\\1&2&0\end{pmatrix},
\qquad x_A=\begin{pmatrix}1\\3\\1\end{pmatrix}.
$$

**Step 1 — take one row at a time.**

$$
\ell_B=F_{AB}x_A
=\begin{pmatrix}
(-1)(1)+(0)(3)+(2)(1)\\
(0)(1)+(-1)(3)+(-1)(1)\\
(1)(1)+(2)(3)+(0)(1)
\end{pmatrix}
=\begin{pmatrix}1\\-4\\7\end{pmatrix}.
$$

**Step 2 — turn the coefficients into a line equation.** The result means

$$u_B-4v_B+7=0
\quad\Longrightarrow\quad
4v_B=u_B+7
\quad\Longrightarrow\quad
v_B=\frac{u_B+7}{4}.$$

For every chosen $u_B$, there is a corresponding $v_B$. **You have a line of candidates, not a unique pixel.** Do not divide the line's coefficients by its last entry and call them a point.

(epipolar-test-match)=
## Guided calculation B: which candidates pass?

A candidate passes if its coordinates make the line equation zero. For $x_B=(5,3,1)^T$, show the full row-column multiplication:

$$
x_B^T\ell_B=
\begin{pmatrix}5&3&1\end{pmatrix}
\begin{pmatrix}1\\-4\\7\end{pmatrix}
=5(1)+3(-4)+1(7)=5-12+7=0.
$$

| Candidate $(u_B,v_B)$ | Substitute into $u_B-4v_B+7$ | Decision |
| --- | --- | --- |
| $(3,5/2)$ | $3-4(5/2)+7=3-10+7=0$ | On the line |
| $(5,3)$ | $5-12+7=0$ | Also on the line |
| $(1,3)$ | $1-12+7=-4$ | Off the line |

**Two candidates pass.** Epipolar consistency is a filter, not proof of correspondence. A repeated texture can produce several plausible matches.

With real measurements, expect a small nonzero residual. Do not interpret the raw residual $-4$ as a distance: multiplying $F$ by ten multiplies that number by ten without changing the geometry. Normalize by the line's first two coefficients:

$$\text{distance}=\frac{|au_B+bv_B+c|}{\sqrt{a^2+b^2}}
=\frac{|-4|}{\sqrt{1^2+(-4)^2}}
=\frac4{\sqrt{17}}\approx0.970.$$

This is a perpendicular distance in **pixels if these coordinates are pixels**. The [estimation section](estimation.md) gives the full symmetric-error formula and a procedure for noisy matches. Scaling the line to $(2,-8,14)^T$ doubles both numerator and denominator, leaving this distance unchanged.

(epipolar-reverse)=
## Guided calculation C: reverse direction, then find the epipoles

**Reverse direction with the transpose.** Given the candidate $x_B=(5,3,1)^T$, its line in A is $F_{AB}^Tx_B$, not $F_{AB}x_B$:

$$
\begin{aligned}
\ell_A&=\begin{pmatrix}-1&0&1\\0&-1&2\\2&-1&0\end{pmatrix}
\begin{pmatrix}5\\3\\1\end{pmatrix}\\
&=\begin{pmatrix}-5+0+1\\0-3+2\\10-3+0\end{pmatrix}
=\begin{pmatrix}-4\\-1\\7\end{pmatrix}.
\end{aligned}
$$

Check the original point: $(-4)(1)+(-1)(3)+7=0$. The same correspondence passes from either direction because transposing a scalar leaves it unchanged.

**Find an epipole by solving a nullspace equation.** The epipole in A satisfies $F_{AB}e_A=0$. Write $e_A=(r,s,w)^T$. Then

$$
-r+2w=0,\qquad -s-w=0,\qquad r+2s=0.
$$

The first two equations give $r=2w$ and $s=-w$. The third becomes $2w+2(-w)=0$, so it adds no independent condition. Choose $w=1$: **$e_A=(2,-1,1)^T$**. This is the one-dimensional nullspace expected of a rank-two $3\times3$ matrix. The first two rows are independent and the nonzero null vector rules out rank three.

Likewise $F_{AB}^Te_B=0$ gives

$$-r+w=0,\qquad -s+2w=0,\qquad 2r-s=0,$$

so **$e_B=(1,2,1)^T$**. Check it on our predicted line: $1-4(2)+7=0$.

**Why does every line pass through $e_B$?** For any $x_A$,
$e_B^T(F_{AB}x_A)=(F_{AB}^Te_B)^Tx_A=0$.
That is the algebraic version of the epipolar-plane picture.

```{warning}
**Special case:** putting $x_A=e_A$ gives $F_{AB}e_A=(0,0,0)^T$. This is not a valid line: the baseline projects to the epipole, so it does not select a unique epipolar plane. Also remember that $F$ and any nonzero multiple of $F$ describe the same geometry.
```

## Worked quiz examples: now use the same steps

### Quiz 4: expand a symbolic matrix

**Worked example 4.1 — expand the assigned constraint.** {ref}`Read the original problem and every worked step <quiz-1-q1>`.

### Quiz 2, Q1: use two views to predict a point in a third

**Worked example 4.2 — two predicted lines meet.** {ref}`Read the original problem and every worked step <quiz-3-q1>`.

```{figure} ../../images/lecture04/third-view.*
:name: fig-lec04-third-view
:width: 60%
:alt: A vertical line u equals one half and a diagonal line u plus v equals one cross at the predicted third-image coordinate one half, one half.

Two independent line predictions locate the third-image point. This applies the incidence operations from Lecture 1 to a new three-view task.
```

**Check the intersection before dividing:** coincident lines give a zero cross product and no unique prediction. Distinct parallel lines meet at an ideal point, not a finite pixel. With noise, nearly parallel lines give an unstable location; incompatible matrices or an incorrect A–B match can also spoil the prediction.

### Quiz 2, Q2: check the supplied matrix before trusting its name

**Worked example 4.3 — correct the supplied solution.** {ref}`Read the original problem and every worked step <quiz-3-q2>`.

## Before moving on

You should be able to explain **why the answer is a line**, multiply a matrix row by row, test a candidate with a scalar dot product, reverse direction with $F^T$, and intersect two lines in the **same** image.

Next: [estimate F from noisy matches](estimation.md), or go directly to [stereo depth, sensitivity and errors](stereo.md). Rectification makes the lines horizontal; it makes matching simpler, but it does not remove depth uncertainty.
