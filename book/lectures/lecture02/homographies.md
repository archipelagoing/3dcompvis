(lec02-homographies)=
# Homographies: straighten a photographed plane

A basketball court is rectangular, but its photograph is not. A **{term}`homography <Homography>`** maps one projective plane to another, letting us turn the photographed floor into a rectangle. It also preserves straight lines, so the court markings stay straight.

**Source:** PDF pages 62–71, printed slides 63–72. The example below develops the actual court-warping assignment.

```{figure} ../../images/lecture02/court-demo.png
:name: fig-lec02-court
:width: 100%
:alt: Lecture basketball-court photograph with four floor corners marked, beside its computed rectangular warp.

Left: the lecture's court photograph, with four approximate floor corners added. Right: a computed rectangular warp of that region. The floor straightens; raised baskets and seating do not become a true overhead view. Source photograph: PDF page 71, printed slide 72; individual photographer uncredited. Warp and annotations are original.
```

## One matrix, followed by a division

````{formula-box} Formula — planar projective mapping
```{math}
:label: eq-lec02-homography
\begin{aligned}
x'&\sim Hx,\qquad H\in\mathbb R^{3\times3},\quad\det H\ne0,\\
u'&=\frac{h_{11}u+h_{12}v+h_{13}}{h_{31}u+h_{32}v+h_{33}},\qquad
v'=\frac{h_{21}u+h_{22}v+h_{23}}{h_{31}u+h_{32}v+h_{33}}.
\end{aligned}
```

$x=(u,v,1)^T$ and $x'=(u',v',1)^T$ are image or plane coordinates. Use consistent units within each plane. The matrix scale follows the convention in {eq}`eq-lec01-hierarchy`.

The ordinary-coordinate fractions require a nonzero denominator. Zero means an ideal destination point. A single $H$ models corresponding images of one plane, or a camera rotating about a fixed center. General camera translation with objects at different depths requires more than one homography.
````

```{application} Map a point or rectify a plane
1. Specify the direction: here $H$ maps source coordinates to destination coordinates.
2. Multiply $H(u,v,1)^T$ and divide by its last entry.
3. Check the result against known correspondences and image bounds.

To recover $H$, use at least four corresponding points in general position: no three collinear in either four-point set. See {ref}`estimation <lec02-estimation>` and {ref}`pixel sampling <lec02-warping>`.
```

(ex-lec02-homography)=
```{worked-example} Worked example 2.2 — perspective changes spacing
**Source:** original small calculation for PDF pages 62–64.

Let $H=\begin{pmatrix}1&0&0\\0&1&0\\1/2&0&1\end{pmatrix}$. The source points $(0,0)$, $(1,0)$, $(2,0)$ map to $(0,0)$, $(2/3,0)$, $(1,0)$.

They stay on a line, but equal source intervals become unequal destination intervals: $2/3$ and $1/3$. The denominator depends on position. This is what an affine map cannot do along a line.

The finite point $(-2,1)$ maps to $(-2,1,0)^T$, an ideal point. The homography remains invertible; only ordinary coordinates fail there.
```

The transformation families and their invariants are taught in {ref}`lec01-transformations`. Here we use their projective case for an actual plane-to-image mapping.

## A new detail: separate an affine map into rotations and scales

PDF page 68 adds a factorization of the affine linear part. It reveals the directions in which the map stretches the image.

````{formula-box} Formula — directional scaling inside an affine map
```{math}
:label: eq-lec02-affine-factors
A=R(\theta)R(-\phi)D R(\phi),\qquad
D=\operatorname{diag}(s_1,s_2).
```

All matrices are $2\times2$; $R$ is the planar rotation from {eq}`eq-lec01-rotation2`. The angles orient the scaling axes and the final rotation. Nonzero signed scales allow any invertible real $A$, including orientation reversal. Translation is handled by the existing affine form in {eq}`eq-lec01-hierarchy`.
````

```{application} Read a directional stretch
1. Apply the rightmost rotation to express a vector in the scaling axes.
2. Scale the two components by $s_1,s_2$, then rotate back by $-\phi$.
3. Apply the final rotation by $\theta$.

For $\theta=0$, $\phi=45^\circ$, and $D=\operatorname{diag}(2,1)$, multiplication gives $A=\begin{pmatrix}3/2&-1/2\\-1/2&3/2\end{pmatrix}$. It doubles the component along $(1,-1)^T$ and leaves the component along $(1,1)^T$ unchanged. This is an original calculation of the slide's added factorization.
```

## Cross-ratio: a ratio perspective cannot change

Ordinary distances change in perspective, but a particular combination of four collinear locations survives.

````{formula-box} Formula — cross-ratio of four collinear points
```{math}
:label: eq-lec02-crossratio
\operatorname{CR}(a,b;c,d)=
\frac{(c-a)(d-b)}{(c-b)(d-a)}.
```

$a,b,c,d$ are distinct scalar positions along one line, in a common coordinate. The result is unitless and depends on the chosen ordering. This finite-coordinate expression assumes nonzero denominators; ideal points are handled by limits or homogeneous coordinates. An invertible projective mapping of the line preserves the result.
````

```{application} Check a projective invariant
1. Keep the same ordering of four distinct collinear points before and after mapping.
2. Compute the two cross-ratios and compare.
3. Do not substitute ordinary image distances for directed line coordinates.

For $a,b,c,d=0,1,2,3$, the result is $4/3$. Under Example 2.2's map, the positions become $0,2/3,1,6/5$; substitution still gives $4/3$.
```

## What is missing from the court assignment?

We need **correspondences and a target shape**. Select four floor corners in cyclic order, match them to a rectangle, then estimate $H$. Its width-to-height ratio must come from known court geometry if we want metric proportions. An arbitrary rectangle can look tidy while having the wrong scale ratio.

Our figure uses approximate source pixels $(24,194)$, $(250,45)$, $(410,70)$, $(280,278)$, matched to $(0,0)$, $(279,0)$, $(279,149)$, $(0,149)$. The chosen aspect ratio is illustrative, not a measurement of the court. Boundary pixels are approximate because the supplied photo is small. **A floor homography cannot reveal hidden floor or flatten raised objects correctly.**

```{index} homography
```

```{index} cross-ratio
```

```{index} invariant
```
