(lec01-planes)=
# Points, planes, and lines in 3D

A 2D line is described by one linear equation. In 3D, one linear equation describes a plane instead. A spatial line therefore needs more structure: it is the intersection of two planes, or a point together with a direction.

**Lecture source:** `wk1_2_cs532s26_IntroToGeometry.pdf`, PDF pages 80–87, printed slides 81–88.

## Homogeneous 3D points

Represent a finite point $(X,Y,Z)$ by $(X,Y,Z,1)^T$. Divide a general homogeneous point $(X_1,X_2,X_3,X_4)^T$ by $X_4$ when $X_4\ne0$. When $X_4=0$, it represents an ideal direction. The zero vector is invalid.

An invertible $4\times4$ matrix $G$ acts by $\mathbf{X}'\sim G\mathbf{X}$. It has $16-1=15$ projective DOF because one overall scale is redundant. A plane transforms by $G^{-T}$; the incidence derivation in {ref}`lec01-transformations` applies without change.

## A plane is a normal and an offset

A **{term}`surface normal <Surface normal>`** is perpendicular to the surface's local tangent directions. For a plane it is constant everywhere. If $n=(a,b,c)^T$, the equation $n^Tq+d=0$ describes points whose displacement from a point on the plane is perpendicular to $n$.

```{index} plane; normal
```

```{index} surface normal
```

```{index} nullspace
```

```{index} Plücker coordinates
```

````{formula-box} Formula — plane incidence and Euclidean distance
```{math}
:label: eq-lec01-plane
\pi^T X=0,\quad \pi=(a,b,c,d)^T,\qquad
D(q,\pi)=\frac{|n^Tq+d|}{\|n\|}.
```

$X=(q^T,1)^T$ is $4\times1$; $q,n$ are $3\times1$. $D$ is unsigned point-to-plane distance in the coordinate length unit. The signed version omits the absolute value and depends on normal orientation.

**Conditions:** $n\ne0$ for a finite Euclidean plane. The plane at infinity $(0,0,0,1)^T$ is projectively valid but has no finite distance formula. Exact geometry; normal scale is arbitrary.
````

```{application} How to use it — test incidence or measure distance
1. Put the point and plane in the same frame.
2. Evaluate $n^Tq+d$; zero means incidence.
3. Divide its magnitude by $\|n\|$ for distance.
4. Check that rescaling all four coefficients leaves the distance unchanged.

See Example 1.5 below.
```

````{formula-box} Formula — plane through three noncollinear points
```{math}
:label: eq-lec01-plane-points
n=(B-A)\times(D-A),\qquad d=-n^TA,\qquad \pi=(n^T,d)^T.
```

$A,B,D$ are $3\times1$ Euclidean positions. Their differences lie in the plane, so their cross product is perpendicular to it. Substituting $A$ fixes $d$.

**Conditions:** the points must be noncollinear. A zero cross product means no unique plane. Reversing its order reverses the normal but preserves the unoriented plane. If coordinates have length units, the unnormalized normal has squared-length units; normalize before metric interpretation.
````

```{application} How to use it — construct and verify a plane
1. Subtract the same anchor point to form two directions.
2. Cross them and check for a nonzero result.
3. Compute $d$ and substitute all three points into the plane equation.
4. Normalize $n$ only when a unit normal or signed metric distance is needed.

See {ref}`Example 1.5 <ex-lec01-plane>` and the camera/object quiz in {ref}`lec01-frames`.
```

```{figure} ../../images/lecture01/planes.*
:name: fig-lec01-plane
:width: 95%
:alt: Two independent vectors in a plane determine a normal by their cross product.

A normal comes from two in-plane directions. Original schematic developing PDF pages 82–84. Apparent angles in this drawing are not measurements of the 3D angles.
```

(ex-lec01-plane)=
```{worked-example} Worked example 1.5 — find a plane, then check a distance
**Source:** original numerical development of PDF pages 82–84.

Let $A=(1,0,0)$, $B=(0,1,0)$, and $D=(0,0,1)$.

1. $B-A=(-1,1,0)$ and $D-A=(-1,0,1)$.
2. Their cross product is $(1,1,1)$, so $d=-1$.
3. The plane is $x+y+z-1=0$. All three input points satisfy it.
4. The origin's distance is $1/\sqrt3$ units, not one: the normal is not unit length.
```

## The same geometry from a nullspace

A **{term}`nullspace <Nullspace>`** consists of vectors a matrix sends to zero. Stacking homogeneous input points as rows makes a plane coefficient vector orthogonal to every row. Conversely, stacking planes gives the point incident to all of them.

````{formula-box} Formula — point/plane incidence systems
```{math}
:label: eq-lec01-plane-null
\underbrace{\begin{pmatrix}X_A^T\\X_B^T\\X_D^T\end{pmatrix}}_{M\;:\;3\times4}\pi=0,
\qquad
\underbrace{\begin{pmatrix}\pi_1^T\\\pi_2^T\\\pi_3^T\end{pmatrix}}_{N\;:\;3\times4}X=0.
```

Each unknown is a nonzero $4\times1$ vector, unique up to scale when the coefficient matrix has rank three. An SVD $M=U\Sigma V^T$ supplies the null vector as the last column of the full $4\times4$ matrix $V$.

**Conditions:** exact rank-three incidence. Lower rank means nonuniqueness. A reduced SVD of a $3\times4$ matrix can omit the null vector: request the full right-singular basis. An intersection with last coordinate zero is ideal, not finite.
````

```{application} How to use it — solve homogeneous incidence
1. Put point or plane coefficients in rows.
2. Check rank and solve for a nonzero right-null vector.
3. Normalize only when valid; substitute back into every equation.
4. For numerical data state a rank tolerance and inspect the residual.

See {ref}`Example 1.6 <ex-lec01-null>`.
```

The determinant construction on PDF page 84 is another way to express the same plane. Four coplanar homogeneous point columns are linearly dependent, so their $4\times4$ determinant vanishes. Expanding along the variable point column yields the plane coefficients.

````{formula-box} Formula — plane coefficients by cofactors
```{math}
:label: eq-lec01-cofactor
\det\begin{pmatrix}X&X_A&X_B&X_D\end{pmatrix}=0,
\qquad \pi=(D_{234},-D_{134},D_{124},-D_{123})^T.
```

$D_{ijk}$ is the $3\times3$ determinant formed from rows $i,j,k$ of the last three columns. Expansion gives $X_1D_{234}-X_2D_{134}+X_3D_{124}-X_4D_{123}=0$.

**Conditions:** independent input point columns. This exact construction equals the nullspace result; near degeneracy can make direct cofactor evaluation poorly conditioned.
````

```{application} How to use it — evaluate plane cofactors
1. Form the $4\times3$ matrix of the input point columns.
2. Delete each row and calculate the remaining determinant.
3. Apply alternating signs and verify incidence at each input point.

See {ref}`Example 1.6 <ex-lec01-null>`.
```

(ex-lec01-null)=
```{worked-example} Worked example 1.6 — duality in numbers
For Example 1.5 the point rows are $(1,0,0,1)$, $(0,1,0,1)$, and $(0,0,1,1)$. Multiplying by $(1,1,1,-1)^T$ gives zero. The cofactors are $1,-1,1,1$ in the order above, giving the same plane after alternating signs.

Conversely, the planes $x=1$, $y=2$, and $z=3$ have rows $(1,0,0,-1)$, $(0,1,0,-2)$, and $(0,0,1,-3)$. Their null vector is $(1,2,3,1)^T$, so their intersection is $(1,2,3)$.

**Source:** original numerical expansions of PDF pages 83–85.
```

## Plücker coordinates: a line is a direction and a moment

**{term}`Plücker coordinates`** encode a nonzero direction $d$ and a moment $m=p\times d$, where $p$ is any point on the line. Choosing a different point along the line should not change its representation.

```{figure} ../../images/lecture01/plucker.*
:name: fig-lec01-plucker
:width: 90%
:alt: A chosen point shifts along a line without changing its direction or moment.

The chosen point may move along the line without changing its moment. Original diagram developing PDF pages 86–87.
```

````{formula-box} Formula — finite-line Plücker coordinates
```{math}
:label: eq-lec01-plucker
L=(d,m),\qquad m=p\times d,\qquad d^Tm=0,\qquad
p_\perp=\frac{d\times m}{\|d\|^2}.
```

All component vectors are $3\times1$. $p_\perp$ is the closest point on the line to the origin. With unitless $d$, $p,m,p_\perp$ have length units. A common nonzero scale on $(d,m)$ represents the same line.

**Conditions:** $d\ne0$. Six entries minus one scale and one orthogonality constraint leave four line DOF. Not every six-vector is valid. Lines entirely at infinity require a more general treatment than this finite-line form.
````

```{application} How to use it — encode or recover a spatial line
1. Choose a point and a nonzero direction; calculate $m=p\times d$.
2. Check $d^Tm=0$.
3. Recover $p_\perp$ if useful and check it belongs to the same line.
4. Keep the direction/moment order and cross-product sign consistent.

See {ref}`Example 1.7 <ex-lec01-plucker>`.
```

Replacing $p$ by $p+\alpha d$ leaves the moment unchanged because $d\times d=0$. The closest-point formula follows from

$$d\times(p\times d)=\|d\|^2p-(d^Tp)d.$$

After division by $\|d\|^2$, the component along the line is removed, leaving the perpendicular displacement from the origin.

````{formula-box} Formula — reciprocal product and line distance
```{math}
:label: eq-lec01-line-distance
\begin{aligned}
\rho&=d_1^Tm_2+d_2^Tm_1,\\
D&=\frac{|\rho|}{\|d_1\times d_2\|}\quad(d_1\times d_2\ne0),\\
D_\parallel&=\frac{\|(p_2-p_1)\times d_1\|}{\|d_1\|}.
\end{aligned}
```

$L_i=(d_i,m_i)$ denotes each valid finite line; $p_i$ is any point on it. The **{term}`reciprocal product <Reciprocal product>`** $\rho$ is zero for coplanar lines, including both intersecting and parallel lines. $D$ is their shortest distance in the coordinate length unit.

**Conditions:** nonzero directions. Use the parallel expression when directions are parallel; the nonparallel formula is unstable near parallelism. A zero reciprocal product alone does not distinguish intersection from parallelism.
````

```{application} How to use it — measure separation
1. Check the direction cross product to classify the case.
2. For nonparallel lines, divide the reciprocal-product magnitude by the cross-product norm.
3. For parallel lines, measure the perpendicular part of the displacement between two points.
4. Check nonnegativity, units, and invariance under common rescaling of a line's coordinates.

See {ref}`Example 1.7 <ex-lec01-plucker>`.
```

The nonparallel formula measures displacement along a common perpendicular. Substituting $m_i=p_i\times d_i$ gives $\rho=(p_1-p_2)^T(d_1\times d_2)$. The denominator turns the common perpendicular into a unit vector.

(ex-lec01-plucker)=
```{worked-example} Worked example 1.7 — two skew lines are two units apart
**Source:** original numerical companion to PDF page 87; supplementary relative to the exam priorities.

Let $p_1=(0,1,0)$, $d_1=(1,0,0)$, $p_2=(0,0,2)$, and $d_2=(0,1,0)$.

1. $m_1=(0,0,-1)$ and $m_2=(-2,0,0)$; each satisfies $d_i^Tm_i=0$.
2. $d_1\times d_2=(0,0,1)$ has norm one.
3. $\rho=-2$, so $D=2$.
4. The first line lies at $z=0$ and the second at $z=2$. Their closest points have equal $x,y$, confirming the result.
```

```{understanding-check} Check 1.4 — does any triplet determine a plane?
What happens for $(0,0,0)$, $(1,0,0)$, and $(2,0,0)$?
```

```{admonition} Solution
:class: dropdown
The points are collinear. Their displacement cross product is zero, so infinitely many planes contain the common line. Do not normalize the zero vector or claim a unique solution.
```
