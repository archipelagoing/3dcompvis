(lec03-dlt-practice)=
# Recover a genuinely projective homography

The earlier DLT example recovered a shifted, stretched rectangle. This one adds a **changing denominator**: a square becomes a trapezoid, and its center does not map to the average of the destination corners.

**Source:** original numerical companion to lecture PDF pages 34–45, addressing the DLT/SVD priority in `ExamToDo.md`. Use the canonical [DLT rows and SVD procedure](../lecture02/estimation.md); this section follows those steps with complete projective data.

(ex-lec03-dlt)=
````{worked-example} Worked example 3.5 — normalize, solve, and recover
**Given:** the following four exact correspondences, in the same order.

| Source $(u,v)$ | Destination $(u',v')$ |
| --- | --- |
| $(0,0)$ | $(0,0)$ |
| $(1,0)$ | $(2,0)$ |
| $(1,1)$ | $(2,1)$ |
| $(0,1)$ | $(0,2)$ |

**1. Normalize each image independently.** For the source square, centroid $(0.5,0.5)$ and mean radius $1/\sqrt2$ give scale $2$. For the destination, centroid $(1,0.75)$ and mean radius $1.28288937$ give scale $1.10236596$. Thus

$$
T=\begin{pmatrix}2&0&-1\\0&2&-1\\0&0&1\end{pmatrix},\qquad
T'\approx\begin{pmatrix}1.102366&0&-1.102366\\0&1.102366&-0.826774\\0&0&1\end{pmatrix}.
$$

The destination mean radius is the average of $1.25,1.25,\sqrt{1.0625},\sqrt{2.5625}$. This is **mean distance**, not root-mean-square distance.

**2. Fill the normalized DLT rows.** For the first pair,
$\widetilde x=(-1,-1,1)^T$ and $\widetilde x'\approx(-1.102366,-0.826774,1)^T$.
Its two rows, using {eq}`eq-lec02-dlt`, are approximately

$$
\begin{aligned}
(&-1,-1,1,0,0,0,-1.102366,-1.102366,1.102366),\\
(&0,0,0,-1,-1,1,-0.826774,-0.826774,0.826774).
\end{aligned}
$$

The other three pairs supply six more rows. The stacked matrix $\widetilde A$ is $8\times9$ with rank eight.

**3. Read the full right null vector.** A full SVD returns a $9\times9$ right-vector basis. One unit null vector, rounded here, is

$$
h\approx(0.627538,0,0.209179,-0.156884,0.418359,-0.052295,
0.189755,0,0.569265)^T.
$$

Its negative is equally valid. Reshape **row by row**, then rescale for display so the last entry is one:

$$
\widetilde H\approx\begin{pmatrix}
1.102366&0&0.367455\\
-0.275591&0.734911&-0.091864\\
1/3&0&1
\end{pmatrix}.
$$

Request the full basis: the eight singular values returned for an $8\times9$ matrix do not themselves include a ninth listed zero. The extra right vector supplies its exact nullspace.

**4. Undo normalization.** Apply {eq}`eq-lec02-normalize`, using unrounded numbers in the calculation:

$$
H=(T')^{-1}\widetilde H T
\ \sim\ \begin{pmatrix}4&0&0\\0&2&0\\1&0&1\end{pmatrix}.
$$

**5. Check a corner and a point you did not fit.** For $(1,1)$, the homogeneous result is $(4,2,2)^T$, hence $(2,1)$: correct. The unmeasured square center gives

$$
H(1/2,1/2,1)^T=(2,1,3/2)^T
\quad\Rightarrow\quad (u',v')=(4/3,2/3).
$$

That differs from the destination vertex average $(1,3/4)$. Perspective does not preserve ordinary averages. The nonzero $h_{31}$ makes the denominator depend on $u$.
````

```{figure} ../../images/lecture03/projective-dlt.*
:name: fig-lec03-dlt
:width: 90%
:alt: A square maps to a trapezoid. The mapped source center is marked separately from the average of the destination vertices.

The orange point is the mapped source center. The destination's marked vertex average is elsewhere; averaging coordinates is not a projective operation.
```

## Use the matrix to make an image

The [court-rectification example](../lecture02/homographies.md) is the slide deck's real-image application, repeated here on PDF page 22. Its [inverse-warping procedure](../lecture02/warping.md) tells you how to fill output pixels after estimating $H$. Keep the directions separate: the matrix above sends source coordinates to destination coordinates; filling a destination pixel requires the reverse map.

**Exam check:** can you explain where each of the nine entries came from, why four matches give eight independent equations, and why the coordinate transforms must be undone in that order? The answer should describe the calculation, not just name “SVD.”
