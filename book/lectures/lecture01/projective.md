(lec01-projective)=
# Points, lines, and the meaning of infinity

Railway tracks are parallel in the world, yet their image traces appear to converge. Is that a contradiction? No: the world plane and the image plane are related by perspective, which does not preserve parallelism.

**Lecture source:** `wk1_2_cs532s26_IntroToGeometry.pdf`, PDF pages 64–71 (printed slides 65–72).

```{figure} ../../images/lecture01/railway.png
:name: fig-lec01-railway
:width: 32%
:alt: Railway tracks converge toward a point near the horizon in a perspective photograph.

The railway example from PDF page 68, printed slide 69. Source: supplied lecture deck; original photographer unspecified. The source image has limited resolution, so it is intentionally displayed at a modest size.
```

## Add a coordinate, not an extra physical dimension

An ordinary point $(u,v)$ can be represented by $\mathbf{x}=(u,v,1)^T$. Multiplying all three components by a nonzero scalar gives the same projective point. The added coordinate makes certain geometric operations easier; it does not give a 2D point an extra physical dimension.

Recall from {ref}`notation` that $\sim$ means equality up to nonzero scale. A finite point $(x_1,x_2,w)^T$ becomes $(x_1/w,x_2/w)$ when $w
e0$. For example, $(6,9,3)^T$ represents $(2,3)$.

The **{term}`projective plane <Projective plane>`** $\mathbb P^2$ is the set of nonzero vectors in $\mathbb R^3$ **identified under scale**. This last clause matters: the slide's shorthand $\mathbb R^3\setminus\{0\}$ must be understood with this identification. Three homogeneous entries have only two degrees of freedom because one overall scale is redundant.

```{index} projective plane
```

```{index} incidence
```

```{index} point at infinity
```

```{index} line at infinity
```

````{formula-box} Formula — point–line incidence
```{math}
:label: eq-lec01-incidence
\boldsymbol\ell^T\mathbf{x}=a x_1+b x_2+c w=0.
```

Here $\boldsymbol\ell=(a,b,c)^T\ne0$ is a homogeneous line and $\mathbf{x}=(x_1,x_2,w)^T\ne0$ is a point. For $w=1$, this is the familiar $au+bv+c=0$. The scalar zero tests **{term}`incidence <Incidence>`**: whether the point lies on the line.

**Conditions and limits:** This is exact. Both line and point coefficients may be rescaled. It tests incidence, not Euclidean distance; a nonzero residual has no scale-independent magnitude unless you normalize it. At least one of $a,b$ must be nonzero for an ordinary finite line.
````

```{application} How to use it — point–line incidence
1. Express the point and line in the same coordinates.
2. Multiply corresponding entries and add them.
3. Check whether the result is zero (or numerically small under a specified normalization).

**Worked connection:** {ref}`Example 1.1 <ex-lec01-intersections>`.
```
### Why a cross product appears

The cross product of two 3-vectors is perpendicular to both. Therefore, if two vectors encode points, their cross product supplies line coefficients orthogonal to both points. If the vectors encode lines, their cross product supplies a point incident to both lines. The algebra is the same; the geometric interpretation changes.

````{formula-box} Formula — join two points or intersect two lines
```{math}
:label: eq-lec01-cross
\begin{aligned}
\boldsymbol\ell&\sim\mathbf{x}\times\mathbf{y},&
\mathbf{p}&\sim\boldsymbol\ell_1\times\boldsymbol\ell_2,\\
\mathbf{a}\times\mathbf{b}
&=\begin{pmatrix}a_2b_3-a_3b_2\\a_3b_1-a_1b_3\\a_1b_2-a_2b_1\end{pmatrix}.
\end{aligned}
```

Each input and output is a $3\times1$ homogeneous vector. Joining two distinct points gives a line; intersecting two distinct lines gives a point. The components have coefficient-dependent units, so interpret the result after the appropriate homogeneous normalization.

**Conditions and limits:** The result must be nonzero. Equal points up to scale do not define a unique line; equal lines do not define a unique intersection. Reversing the order changes the sign and therefore preserves the represented object.
````

```{application} How to use it — join two points or intersect two lines
1. Decide whether the inputs represent points or lines.
2. Evaluate the three cross-product components.
3. If the result is zero, diagnose coincident/degenerate inputs.
4. For a point, divide by the last component only if it is nonzero. Verify incidence by dot products.

**Worked connection:** {ref}`Example 1.1 <ex-lec01-intersections>`.
```
(ex-lec01-intersections)=
```{worked-example} Worked example 1.1 — parallel lines have a projective intersection
**Source:** original numerical expansion of the railway/ideal-point example, PDF pages 67–71. The related Spring 2020 Quiz 1 is solved in {ref}`lec01-quiz-practice`.

Take $y=1$ and $y=2$, represented by $\ell_1=(0,1,-1)^T$ and $\ell_2=(0,1,-2)^T$.

1. Their cross product is $(-1,0,0)^T\sim(1,0,0)^T$.
2. The last coordinate is zero, so this is an **{term}`ideal point <Ideal point>`**, not a finite Euclidean position.
3. Check incidence: both $\ell_1^T(1,0,0)$ and $\ell_2^T(1,0,0)$ are zero.
4. Its first two coordinates identify the horizontal direction. Division by the last coordinate is neither required nor allowed.

For comparison, intersecting $x=2$, or $(1,0,-2)^T$, with $y=3$, or $(0,1,-3)^T$, gives $(2,3,1)^T$, a finite point.
```

````{formula-box} Formula — ideal points and the line at infinity
```{math}
:label: eq-lec01-ideal
\begin{aligned}
\boldsymbol\ell_1\times\boldsymbol\ell_2
&=(c_2-c_1)(b,-a,0)^T,\\
\boldsymbol\ell_\infty&=(0,0,1)^T,\qquad
\boldsymbol\ell_\infty^T(d_x,d_y,0)^T=0.
\end{aligned}
```

The parallel finite lines are $\ell_1=(a,b,c_1)^T$ and $\ell_2=(a,b,c_2)^T$. Their ideal intersection records direction $(b,-a)$. All points with last coordinate zero lie on the **{term}`line at infinity <Line at infinity>`**.

**Conditions and limits:** Require $(a,b)\ne(0,0)$ and $c_1\ne c_2$. The factor $c_2-c_1$ may be dropped up to scale, but not when it is zero. “At infinity” is a projective classification, not a very large finite coordinate.
````

```{application} How to use it — ideal points and the line at infinity
1. Put distinct parallel lines into a shared $(a,b)$ normalization.
2. Cross them and recognize the zero last component.
3. Read the direction from the first two components and check it is perpendicular to $(a,b)$.

**Worked connection:** {ref}`Example 1.1 <ex-lec01-intersections>`.
```
```{figure} ../../images/lecture01/projective-lines.*
:name: fig-lec01-projective
:width: 100%
:alt: Parallel world-plane lines and perspective image lines are shown in separate panels.

An ideal point in one plane may map to a finite vanishing point in another. Original diagram developing PDF pages 68–71. The world and image panels are different coordinate spaces, not two claims about the same pair of coordinate lines.
```

## A vanishing point is not automatically an ideal image point

A scene's parallel rails share a direction. Under a perspective mapping, that direction can project to a finite pixel location: the **{term}`vanishing point <Vanishing point>`** in the photograph. The **{term}`horizon <Horizon>`** of a scene plane is the image of that plane's line at infinity. It need not coincide with the image's own line at infinity.

This distinction explains the opening puzzle. The world lines remain parallel in world coordinates, while their images can intersect at an ordinary finite pixel. We will derive the camera mapping later in {ref}`lec01-cameras`.

```{understanding-check} Check 1.2 — does changing scale change the line?
Do $(2,-2,4)^T$ and $(-1,1,-2)^T$ describe different lines? Does $(0,0,0)^T$ describe every line?
```

```{admonition} Solution
:class: dropdown
The first two vectors differ by a factor of $-2$, so they describe the same line. The zero vector is invalid: its equation places no restriction on points and cannot identify a unique line.
```

## What to remember

Use dot products for incidence and cross products for joins/intersections. Normalize a finite point only after checking its last coordinate. Track which space a point belongs to before calling it a vanishing point or a point at infinity.
