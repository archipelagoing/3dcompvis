(lec01-transformations)=
# Move points without losing the geometry

Suppose a point is one unit to the right of a pivot. A quarter-turn should put it one unit above that pivot. Rotating around the coordinate origin instead gives the wrong answer unless the pivot happens to be the origin. A small coordinate diagram makes this distinction easier than memorizing a large matrix.

**Lecture source:** `wk1_2_cs532s26_IntroToGeometry.pdf`, PDF pages 72–79 (printed slides 73–80).

Throughout the 2D rotation examples, $x$ points right and $y$ points **up** in a Cartesian diagram. This differs from the downward pixel $v$ axis in the notation guide. We use active rotations of points and the right-hand rule; do not transfer a screen-clockwise interpretation without checking the axes.

## Derive rotation from the basis vectors

A counterclockwise rotation by $	heta$ sends $(1,0)^T$ to $(\cos	heta,\sin	heta)^T$. It sends $(0,1)^T$ to $(-\sin	heta,\cos	heta)^T$. A point $(x,y)^T$ is $x$ times the first basis vector plus $y$ times the second. Rotating both basis vectors and combining them gives the columns of the rotation matrix.

````{formula-box} Formula — 2D rotation
```{math}
:label: eq-lec01-rotation2
\mathbf{p}'=R(\theta)\mathbf{p},\qquad
R(\theta)=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}.
```

$\mathbf{p}$ and $\mathbf{p}'$ are $2\times1$ positions relative to the rotation center; $R$ is $2\times2$ and unitless. Thus $x'=x\cos\theta-y\sin\theta$ and $y'=x\sin\theta+y\cos\theta$.

**Conditions and limits:** Exact for a planar rotation. State angle units before evaluating trigonometric functions. This rotates around the origin and preserves lengths and angles; translation is a separate operation.
````

```{application} How to use it — 2D rotation
1. Choose a Cartesian axis convention and rotation center.
2. Convert the angle to the units expected by the computation.
3. Multiply the matrix by the point; check that its distance from the center is unchanged.

**Worked connection:** {ref}`Example 1.2 <ex-lec01-pivot>`.
```

````{formula-box} Formula — translation and rotation about a pivot
```{math}
:label: eq-lec01-rigid2
\begin{aligned}
\begin{pmatrix}\mathbf{p}'\\1\end{pmatrix}
&=\begin{pmatrix}R&\mathbf{t}\\0&1\end{pmatrix}
\begin{pmatrix}\mathbf{p}\\1\end{pmatrix},\\
\mathbf{p}'&=\mathbf{c}+R(\mathbf{p}-\mathbf{c}),\qquad
H_c=T(\mathbf{c})\operatorname{diag}(R,1)T(-\mathbf{c}).
\end{aligned}
```

$\mathbf{p},\mathbf{c},\mathbf{t}$ are $2\times1$ vectors in the same length unit. $T(\mathbf{t})$ is the $3\times3$ homogeneous translation matrix with identity upper-left block and last column $(t_x,t_y,1)^T$.

**Conditions and limits:** Exact rigid geometry; the rightmost matrix acts first. A direction has homogeneous last coordinate zero, so a translation does not change it. A position has last coordinate one.
````

```{application} How to use it — translation and rotation about a pivot
1. Subtract the pivot to express the point relative to it.
2. Apply the rotation.
3. Add the pivot back. In homogeneous form multiply in that same right-to-left order.
4. Check that the pivot itself stays fixed.

**Worked connection:** {ref}`Example 1.2 <ex-lec01-pivot>`.
```
```{figure} ../../images/lecture01/rotation-center.*
:name: fig-lec01-pivot
:width: 85%
:alt: A point at 3,1 rotates 90 degrees about pivot 2,1 to position 2,2.

Translate to the pivot, rotate the offset, then translate back. Original solution diagram for the hands-on question on PDF page 77, printed slide 78.
```

(ex-lec01-pivot)=
```{worked-example} Worked example 1.2 — a quarter-turn around a chosen center
**Source:** numerical adaptation of the hands-on tasks on PDF page 77.

Let $p=(3,1)^T$, $c=(2,1)^T$, and $\theta=90^\circ$.

1. The offset is $p-c=(1,0)^T$.
2. A quarter-turn sends that offset to $(0,1)^T$.
3. Adding the center gives $p'=(2,2)^T$.
4. Both offsets have length one, and applying the same operation to $c$ gives $c$.

Rotating $p$ directly around the origin would give $(-1,3)^T$, demonstrating why the chosen center matters.
```

## Transformation families: what stays unchanged?

The **degrees of freedom (DOF)** count independent parameters, not the number of printed matrix entries. A general invertible $3\times3$ homogeneous matrix has nine entries, but its overall nonzero scale is irrelevant, leaving eight DOF.

````{formula-box} Formula — 2D transformation hierarchy
```{math}
:label: eq-lec01-hierarchy
H_E=\begin{pmatrix}R&t\\0^T&1\end{pmatrix},\quad
H_S=\begin{pmatrix}sR&t\\0^T&1\end{pmatrix},\quad
H_A=\begin{pmatrix}A&t\\0^T&1\end{pmatrix},\quad
H_P=\begin{pmatrix}A&t\\v^T&\alpha\end{pmatrix}.
```

Blocks $R,A$ are $2\times2$; $t,v$ are $2\times1$ and $\alpha,s$ are scalars. Euclidean, similarity, affine, and projective maps have respectively 3, 4, 6, and 8 DOF in 2D. Here $s>0$ and $R$ is a proper rotation.

**Conditions and limits:** Each full mapping must be invertible; affine $A$ must be invertible. Projective division is required after multiplication and can map finite points to infinity. The Euclidean form here excludes reflections; allowing reflections adds a discrete choice, not another continuous DOF.
````

```{application} How to use it — 2D transformation hierarchy
1. Ask what the data require: rigid motion, uniform scale, shear, or perspective.
2. Identify the smallest valid transformation family.
3. Check its invariants using the table below and normalize transformed finite points.

**Worked connection:** {ref}`Example 1.3 <ex-lec01-family>`.
```
| Family | What it preserves | What it can change |
| --- | --- | --- |
| Euclidean | Lengths, angles, incidence, parallelism | Position and orientation |
| Similarity | Angles and ratios of lengths | Overall scale |
| Affine | Incidence, parallelism, ratios along a line, ratios of areas | Angles and unequal directional scales |
| Projective | Incidence, straightness, cross-ratio where defined | Parallelism, lengths, angles, ordinary area ratios |

The table summarizes PDF page 78. “Preserves ratios” for an affine map means the relevant ratio within the same transformation, not that every arbitrary pair of vector lengths is preserved. A projectivity also preserves tangency where defined; it need not preserve a visible square's appearance.

(ex-lec01-family)=
```{worked-example} Worked example 1.3 — shear is not a rotation
**Source:** original computation developing the transformation hierarchy on PDF page 78.

Take $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$. It sends the basis vectors to $(1,0)^T$ and $(1,1)^T$.

1. Their original dot product is zero; their new dot product is one. The right angle changed.
2. Horizontal parallel lines remain horizontal and parallel.
3. The determinant is one, so oriented area is unchanged for this particular shear.

This is affine, but not Euclidean or similarity. General affine maps multiply every area by the same determinant magnitude, which explains why area ratios are preserved even when areas themselves change.
```

The hierarchy slide also names the **{term}`circular points <Circular points>`**: two complex points at infinity shared by all Euclidean circles in a plane. Their invariance under similarities is a projective way of encoding angle information; they are not finite pixels you could photograph. In 3D, the analogous **{term}`absolute conic <Absolute conic>`** is a complex conic on the plane at infinity that encodes the Euclidean metric. These are vocabulary previews for reconstruction upgrades in Lecture 6, not additional numerical tasks for Lecture 1.

## Lines transform differently from points

A line is a set of points satisfying $\ell^Tx=0$. If $x'=Hx$, then $x=H^{-1}x'$. Substituting gives $\ell^TH^{-1}x'=0$. Transpose the coefficient product: $(H^{-T}\ell)^Tx'=0$. That is why multiplying a line by $H$ generally gives the wrong result.

````{formula-box} Formula — transform line and plane coefficients
```{math}
:label: eq-lec01-dual
\mathbf{x}'\sim H\mathbf{x},\qquad
\boldsymbol\ell'\sim H^{-T}\boldsymbol\ell;
\qquad
\mathbf{X}'\sim G\mathbf{X},\quad\boldsymbol\pi'\sim G^{-T}\boldsymbol\pi.
```

$H$ is an invertible $3\times3$ planar projectivity; $G$ is an invertible $4\times4$ spatial projectivity. Lines and planes are **dual** coefficients of incidence equations, so they transform with the inverse transpose.

**Conditions and limits:** Exact projective incidence. The inverse does not exist for a singular transformation; such a map is not a projectivity. Coefficient normalization does not change the represented line or plane.
````

```{application} How to use it — transform line and plane coefficients
1. Confirm whether the object is a point/direction or an incidence coefficient vector.
2. Use the forward matrix for points and its inverse transpose for lines/planes.
3. Transform a known incident point and verify that its new incidence residual is zero.

**Worked connection:** {ref}`Example 1.4 <ex-lec01-line-transform>`.
```
(ex-lec01-line-transform)=
```{worked-example} Worked example 1.4 — translate a line
**Source:** original verification of PDF page 79's line-transformation rule.

Translate every point by $(2,0)^T$. The line $x=0$ should become $x'=2$.

Its coefficients are $\ell=(1,0,0)^T$. With $H=\begin{pmatrix}1&0&2\\0&1&0\\0&0&1\end{pmatrix}$, the correct result is $H^{-T}\ell=(1,0,-2)^T$, or $x'-2=0$. Applying $H$ directly to $\ell$ would leave the line at $x'=0$, which fails the geometric check.
```

```{understanding-check} Check 1.3 — reverse the operation
After the pivot rotation in Example 1.2, how do you recover the original point?
```

```{admonition} Solution
:class: dropdown
Subtract the same pivot, rotate by $-90^\circ$, then add the pivot back. The inverse reverses the operation order: $(ABC)^{-1}=C^{-1}B^{-1}A^{-1}$. For this pivot sandwich the result is $T(c)R(-90^\circ)T(-c)$.
```
