(lec04-epipolar-practice)=
# Solve the epipolar quizzes

The [fundamental-matrix box](../lecture02/two-view.md) gives the rule. These questions test whether you can use it without confusing a **point**, a **line**, and a **scalar constraint**.

**Sources:** lecture PDF pages 18–21; `cs532f15_quiz4.pdf` and `cs532s19_quiz4.pdf`, P1–P2, PDF page 1, both printed Spring 2019 Quiz 4; Fall 2025 Quiz 2, `cs532f25_quiz_2_solution.pdf`, Q1–Q2, PDF page 1.

## A symbolic matrix is still a calculation

(ex-lec04-symbolic)=
````{worked-example} Worked example 4.1 — expand the assigned constraint
**Adapted from:** Spring 2019 Quiz 4, P1–P2. The two filenames contain the same questions; use the second as a closed-notes retest.

**P1:** Let $x_A=(x,y,w)^T$. Write the rows of $F_{AB}$ as $f_1^T,f_2^T,f_3^T$, where each $f_i$ is a three-entry column vector. The line in image B is

$$
\ell_B=F_{AB}x_A=
\begin{pmatrix}f_{11}x+f_{12}y+f_{13}w\\
f_{21}x+f_{22}y+f_{23}w\\
f_{31}x+f_{32}y+f_{33}w\end{pmatrix}
=\begin{pmatrix}f_1^Tx_A\\f_2^Tx_A\\f_3^Tx_A\end{pmatrix}.
$$

Those are **line coefficients**. If $\ell_B=(a,b,c)^T$, an ordinary candidate $(u_B,v_B)$ must satisfy $au_B+bv_B+c=0$. There is generally a whole line of candidates. For the requested sketch, draw the known point in A and the predicted line in B, as in the existing schematic {numref}`fig-lec02-epipolar` (a rectified special case).

**P2:** Substitute $x_A=(1,0,1)^T$ and $x_B=(0,1,1)^T$. First multiply by $x_A$: this adds columns 1 and 3 of $F$. Left multiplication by $x_B^T$ then adds entries 2 and 3:

$$x_B^TF_{AB}x_A=f_{21}+f_{23}+f_{31}+f_{33}=0.$$

In vector-product form this is
$\bigl(f_2+f_3\bigr)^T x_A=0$, equivalently $x_B\cdot(F_{AB}x_A)=0$.

**Check:** the final result is one scalar, not a three-entry point.
````

## Use two views to predict a point in a third

(ex-lec04-third-view)=
````{worked-example} Worked example 4.2 — two predicted lines meet
**Adapted from:** Fall 2025 Quiz 2, Q1. The following numbers are an original companion.

Given $x_A\leftrightarrow x_B$, generate two lines **in image C**:
$\ell_A^C=F_{AC}x_A$ and $\ell_B^C=F_{BC}x_B$. Their homogeneous intersection is
$x_C\sim\ell_A^C\times\ell_B^C$.

For example, take normalized image coordinates
$x_A=(1/2,3/4,1)^T$, $x_B=(1/4,3/4,1)^T$, and

$$
F_{AC}=\begin{pmatrix}0&0&-1\\0&0&0\\1&0&0\end{pmatrix},\qquad
F_{BC}=\begin{pmatrix}0&0&-1\\0&0&-1\\1&1&0\end{pmatrix}.
$$

1. Multiply: $\ell_A^C=(-1,0,1/2)^T$, $\ell_B^C=(-1,-1,1)^T$.
2. Intersect: their cross product is $(1/2,1/2,1)^T$.
3. Check: both line dot products are zero. Thus $(u_C,v_C)=(1/2,1/2)$.

These matrices are compatible: aligned cameras at $(0,0,0)$, $(1,0,0)$, $(0,1,0)$ observing point $(2,3,4)$ produce these image coordinates. The calculation predicts a location, but image evidence must still confirm that the point is visible there.
````

```{figure} ../../images/lecture04/third-view.*
:name: fig-lec04-third-view
:width: 75%
:alt: A vertical line u equals one half and a diagonal line u plus v equals one cross at the predicted third-image coordinate one half, one half.

Two independent line predictions locate the third-image point. This applies the incidence operations from Lecture 1 to a new three-view task.
```

**Check the intersection before dividing:** coincident lines give a zero cross product and no unique prediction. Distinct parallel lines meet at an ideal point, not a finite pixel. With noise, nearly parallel lines give an unstable location; incompatible matrices or an incorrect A–B match can also spoil the prediction.

## Check the supplied matrix before trusting its name

(ex-lec04-invalid-f)=
````{worked-example} Worked example 4.3 — correct the supplied solution
**Adapted from:** Fall 2025 Quiz 2, Q2.

The question supplies $x'=(1,2,1)^T$ and
$F=\begin{pmatrix}1&2&1\\0&1&2\\1&0&1\end{pmatrix}$.
It asks for an epipolar-consistent $x$.

1. Multiply the row: $x'^TF=(2,4,6)$.
2. The required condition is **$x'^TFx=0$**, hence $2u+4v+6w=0$.
3. For a finite point with $w=1$, choose $v=0$, giving $u=-3$. Thus $x=(-3,0,1)^T$ works. Another choice is $(-5,1,1)^T$.
4. Check directly: $(2,4,6)(-3,0,1)^T=0$.

**Two source issues:** the solution writes $x'^TF=x$, equating a line row with a point. Its final line equation is usable, but that equality is wrong. Also, $\det F=4$, so the supplied matrix has rank three and cannot be a genuine fundamental matrix for two pinhole cameras.

These points satisfy the **given bilinear equation**; the matrix still cannot describe valid camera geometry.
````
