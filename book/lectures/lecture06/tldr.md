(lec06-tldr)=
# TLDR

**Tracks give measurements. Camera models turn those measurements into equations. Optimization makes their predictions agree.**

- SfM estimates camera motion and 3D structure together. Without external metric information, common gauge freedoms remain.
- A projective reconstruction preserves the images but may distort 3D angles and parallelism. Additional independent constraints justify affine/metric upgrades; a known length can fix metric scale.
- Under affine cameras, center complete tracks, form the measurement matrix, and retain its leading SVD components. Its ideal rank is at most three. Missing entries are not zeros.
- Triangulation stacks two linear rows per view, takes a right singular vector, and checks dehomogenization, cheirality, reprojection, and parallax. Refine geometric image error when needed.
- Sequential SfM initializes a pair, registers cameras against known 3D points, triangulates new tracks, filters, and bundle-adjusts. Five-point relative pose and P3P solve different problems.
- Bundle adjustment minimizes reprojection error over observed camera–point pairs. Define residual signs, parameter conventions, weights, and gauge before constructing the Jacobian.
- Gauss–Newton solves a local least-squares model; LM adds damping. Always check the actual nonlinear cost. Sparsity and point elimination make large solves practical.

## Short quiz

These are **original practice questions**, separate from the historical/booklet [quiz workbook](quiz-workbook.md). Try each before opening its answer. All answers are printed in the PDF.

### Question 1

```{original-question} Original practice question
If all world points and camera centers double in Euclidean coordinates, with rotations fixed, do image projections change?
```

`````{worked-solution} Answer 1

````{solution-step} 1 — Find camera coordinates
**Why:** Both the scene and camera translation must scale consistently.

$$q\,{}^{new}=R(2X-2C)=2R(X-C)=2q.$$
````

````{solution-step} 2 — Divide by depth
**Why:** Perspective removes a common nonzero scale.

$$u^{new}=f_x\frac{2q_x}{2q_z}+c_x=u.$$
The same holds for the vertical coordinate. Metric scale needs extra information.
````
`````

### Question 2

```{original-question} Original practice question
A complete centered affine measurement matrix has shape $8	imes10$. What factor shapes and ideal rank bound apply?
```

`````{worked-solution} Answer 2

````{solution-step} 1 — Identify cameras and points
**Why:** There are two rows per camera and one column per point.

$$m=4,\quad n=10,\quad M\in\mathbb R^{8\times3},\quad S\in\mathbb R^{3\times10}.$$
````

````{solution-step} 2 — Apply the product rank bound
**Why:** A product cannot have rank greater than either factor.

$$D=MS\quad\Longrightarrow\quad\operatorname{rank}(D)\le3.$$
Rank equals three only for suitable nondegenerate motion and shape.
````
`````

### Question 3

```{original-question} Original practice question
Given $u=2,v=3$ and $P=[I\mid0]$, display the two triangulation rows.
```

`````{worked-solution} Answer 3

````{solution-step} 1 — Write the camera rows
**Why:** Multiplication by the projection denominator removes the unknown image scale.

$$p_1^T=(1,0,0,0),\ p_2^T=(0,1,0,0),\ p_3^T=(0,0,1,0).$$
````

````{solution-step} 2 — Assemble the row pair
**Why:** Each observed image point supplies two constraints.

$$A_i=\begin{pmatrix}-1&0&2&0\\0&-1&3&0\end{pmatrix}.$$
One image still leaves depth undetermined; add another camera's constraints.
````
`````

### Question 4

```{original-question} Original practice question
A centered factorization changes motion to $MC$ for invertible $C$. How must shape change to preserve the image measurements?
```

`````{worked-solution} Answer 4

````{solution-step} 1 — Cancel the inserted transformation
**Why:** The inner factors must multiply to the identity.

$$S^{new}=C^{-1}S.$$
````

````{solution-step} 2 — Verify the product
**Why:** Preserving the product preserves centered image predictions.

$$M^{new}S^{new}=(MC)(C^{-1}S)=MS=D.$$
````
`````

### Question 5

```{original-question} Original practice question
For $r(Z)=260-160/Z-219$ at $Z=4$, compute one undamped Gauss–Newton depth update.
```

`````{worked-solution} Answer 5

````{solution-step} 1 — Evaluate the local model
**Why:** The residual and derivative set the scalar least-squares problem.

$$r=1,\qquad J=160/Z^2=10.$$
````

````{solution-step} 2 — Solve and check
**Why:** The correct sign must reduce the actual nonlinear error.

$$\delta=-\frac{Jr}{J^2}=-0.1,\quad Z_{new}=3.9,$$
$$r(3.9)\approx-0.025641,\quad E_{new}\approx0.00032873<0.5.$$
````
`````

### Question 6

```{original-question} Original practice question
Why are a first-pose constraint and a nonzero baseline constraint useful in calibrated monocular bundle adjustment?
```

`````{worked-solution} Answer 6

````{solution-step} 1 — Identify the freedoms
**Why:** A common rigid transform and scale do not change image predictions.

$$3\text{ translation}+3\text{ rotation}+1\text{ scale}=7\text{ gauge freedoms}.$$
````

````{solution-step} 2 — Anchor the coordinate system
**Why:** A solver should not chase directions that leave the objective unchanged.

Fixing the first pose removes six freedoms. Fixing a nonzero baseline or known length fixes the common scale. Other degeneracies can still remain.
````
`````

