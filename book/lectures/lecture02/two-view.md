(lec02-two-view)=
# Distortion and two-view geometry

A planar warp is powerful, but it cannot explain curved lens distortion or general 3D parallax. The final slides introduce the tools for those cases.

**Source:** PDF pages 105–129, printed slides 106–130; the section credits R. Hartley, A. Zisserman, and M. Pollefeys. The assigned epipolar/stereo quizzes and a fuller estimation treatment belong to Lecture 4.

## Straight lines first: correct lens distortion

**{term}`Radial distortion <Radial distortion>`** moves points along directions from a distortion center. Straight scene edges can become curved. A homography preserves lines, so it cannot generally undo this bending.

````{formula-box} Formula — radial correction model
```{math}
:label: eq-lec02-radial
r^2=(u-c_u)^2+(v-c_v)^2,\quad
\begin{pmatrix}\widehat u\\\widehat v\end{pmatrix}
=\begin{pmatrix}c_u\\c_v\end{pmatrix}
+(1+k_1r^2+k_2r^4+\cdots)
\begin{pmatrix}u-c_u\\v-c_v\end{pmatrix}.
```

Here $(u,v)$ are measured distorted coordinates and hats denote corrected coordinates. The coefficients belong to **this correction direction**; a forward-distortion model generally needs different coefficients or numerical inversion. Use calibrated units: if $r$ is in pixels, $k_1$ has units pixel$^{-2}$ and $k_2$ pixel$^{-4}$; normalized coordinates are also common.

This low-order model describes radial effects, not every lens defect. The distortion center may differ from the principal point. PDF page 109 mixes radius and squared-radius notation; writing $r^2$ explicitly avoids that ambiguity.
````

```{application} Correct a point before geometric estimation
1. Use the calibrated center, units, coefficients, and mapping direction.
2. Compute $r^2$ and the radial factor, then correct the coordinate.
3. Check that straight scene edges become straighter; resample images with an appropriate inverse map.

For center $(0,0)$, point $(100,0)$ pixels, $k_1=10^{-6}$ pixel$^{-2}$, and no higher terms, the factor is $1.01$ and the corrected point is $(101,0)$. A positive coefficient here expands radii; never transfer that sign interpretation to the inverse convention blindly.
```

The slides suggest estimating distortion jointly with other camera parameters or by straightening known straight edges. Their room-image before/after sequence illustrates why this matters: ideal projective geometry should be applied to undistorted coordinates.

## One point becomes a line in the other image

With two camera centers $C,C'$ and a scene point $X$, the three define an **epipolar plane**. It cuts each image plane in an **{term}`epipolar line <Epipolar line>`**. If the first image point is known but its depth is not, its possible matches lie along that line in the second image.

The **{term}`epipole <Epipole>`** is the image of the other camera center; every epipolar line in an image passes through its epipole. The line between camera centers is the **baseline**.

```{figure} ../../images/lecture02/epipolar.*
:name: fig-lec02-epipolar
:width: 100%
:alt: In rectified views, a known left point restricts its right match to the same horizontal row, with depth still unknown.

A special, rectified case: the right match must lie on the corresponding row. Its location along that row still depends on depth. Original schematic developing PDF pages 113–119.
```

## The fundamental matrix maps points to lines

````{formula-box} Formula — epipolar constraint and epipoles
```{math}
:label: eq-lec02-fundamental
\begin{aligned}
\ell'&=Fx,\qquad \ell=F^Tx',\qquad x'^TFx=0,\\
Fe&=0,\qquad F^Te'=0,\qquad \operatorname{rank}F=2.
\end{aligned}
```

$x,x'$ are homogeneous image $3\times1$ points; $\ell,\ell'$ are line coefficients, $e,e'$ epipoles. $F$ is a $3\times3$ **{term}`fundamental matrix <Fundamental matrix>`**, defined up to nonzero scale. It has seven DOF: nine entries minus scale minus the rank-two constraint. Reversing the image order transposes $F$.

This ideal constraint assumes corresponding undistorted points and distinct camera centers. At an epipole, the corresponding line vector can vanish. Pure rotation has no nonzero baseline and does not determine a nonzero fundamental matrix from the camera pair. The equation constrains correspondence; it does not identify a unique match.
````

```{application} Turn a point into a correspondence constraint
1. Multiply $F$ by the first image point to obtain the second image's line.
2. Test a candidate match by its dot product with that line.
3. For noisy data, use a scale-normalized geometric error instead of comparing raw $x'^TFx$ values across arbitrary scalings.

Check matrix rank and image order. See Example 2.6.
```

(ex-lec02-fundamental)=
```{worked-example} Worked example 2.6 — a horizontal epipolar line
**Source:** original numerical companion to the parallel-camera example, PDF page 119.

Let $F=\begin{pmatrix}0&0&0\\0&0&-1\\0&1&0\end{pmatrix}$ and $x=(2,3,1)^T$. Then $Fx=(0,-1,3)^T$: candidate matches satisfy $-v'+3=0$.

Both $(5,3,1)^T$ and $(8,3,1)^T$ satisfy the constraint; $(5,4,1)^T$ does not. The two valid candidates show why an epipolar line is not a point prediction. The matrix has rank two and both epipoles are $(1,0,0)^T$, the horizontal ideal direction.
```

## Where does the matrix come from?

The source derives $F$ by projecting two points on the first camera's viewing ray into the second image. Their join is the epipolar line.

````{formula-box} Formula — construct F from two camera matrices
```{math}
:label: eq-lec02-fcamera
PC=0,\qquad e'=P'C,\qquad
F=[e']_\times P'P^+.
```

$P,P'$ are rank-three $3\times4$ camera matrices; $C$ is the first camera center as a homogeneous 4-vector; $P^+$ is a $4\times3$ right pseudoinverse with $PP^+=I_3$. The matrix $[e']_\times$ takes a cross product with $e'$.

For distinct centers, $P^+x$ is one 3D point projecting to $x$; adding $\lambda C$ stays on its projective ray. Its second image lies on the line joining $P'P^+x$ to $P'C$, producing the formula. Coincident centers give $P'C=0$, so this construction gives zero, not a valid rank-two $F$.
````

```{application} Check a camera-derived epipolar geometry
1. Find a nonzero null vector $C$ of $P$ and compute $e'=P'C$.
2. Form the pseudoinverse and cross-product matrix, then multiply in the stated order.
3. Project a test 3D point in both cameras and verify the scalar constraint.

The cameras $P=[I\mid0]$, $P'=[I\mid(-1,0,0)^T]$ give Example 2.6's matrix up to sign. A scene point $(2,3,1,1)^T$ projects to $(2,3,1)^T$ and $(1,3,1)^T$, on the same row.
```

For a fixed nondegenerate camera pair, $F$ is unique **up to scale**. Estimating it from a finite set of matches can be ambiguous, particularly with planar scene points.

````{formula-box} Formula — linear equations for F from matches
```{math}
:label: eq-lec02-eightpoint
\begin{pmatrix}u'u&u'v&u'&v'u&v'v&v'&u&v&1\end{pmatrix}f=0,
\qquad Af=0.
```

$f=(F_{11},F_{12},F_{13},F_{21},\ldots,F_{33})^T$ is $9\times1$; one finite match contributes one row. At least eight suitably independent matches give the linear estimate. This differs from homography DLT's **two** equations per match. Noisy linear solutions need a rank-two correction.
````

```{application} Recognize the eight-point estimation route
1. Normalize both sets of image coordinates and stack the rows.
2. Find the smallest right singular vector and reshape it into a matrix.
3. Enforce rank two by setting its smallest singular value to zero.
4. Undo normalization: if normalized points are $Tx,T'x'$, then $F=T'^T\widetilde F T$; verify on held-out matches.

For Example 2.6 and match $(u,v)=(2,3)$, $(u',v')=(5,3)$, the row is $(10,15,5,6,9,3,2,3,1)$. Dotting it with the row-stacked $F$ gives $-3+3=0$. Lecture 4 will develop noisy estimation and its assigned quiz calculations.
```

## Motion patterns and rectification

The three slide examples show different locations for the epipoles:

- **Converging cameras:** epipolar lines fan toward finite epipoles, possibly outside the images.
- **Translation parallel to the image plane:** epipoles are ideal; for a horizontal baseline and aligned cameras, epipolar lines are horizontal.
- **Forward translation:** epipoles can lie inside the images, with radial epipolar lines. Ordinary rectangular planar rectification becomes problematic near that epipole.

**{term}`Rectification <Rectification>`** warps two views so corresponding epipolar lines become matching horizontal rows. It simplifies the search from two dimensions to one; it does not eliminate matching ambiguity or depth variation.

````{formula-box} Formula — rectified coordinates and line geometry
```{math}
:label: eq-lec02-rectify
\bar x\sim Hx,\quad \bar x'\sim H'x',\quad
\bar F=H'^{-T}FH^{-1},\qquad
He\sim H'e'\sim(1,0,0)^T.
```

$H,H'$ are nonsingular $3\times3$ image warps. Moving both epipoles to the horizontal ideal point makes epipolar lines horizontal; the two warps must also align the corresponding row coordinates. A finite epipole is sent to infinity, so its neighborhood cannot retain a finite undistorted rectangular image.
````

```{application} Interpret a rectified pair
1. Estimate camera/epipolar geometry and choose compatible rectifying warps.
2. Resample both images by inverse warping.
3. Check that known matches share the same row; then search along that row.

Example 2.6 is already rectified: identity warps preserve its horizontal lines and equal-row constraint. The final slide's paired objects illustrate the visual goal. Detailed stereo depth follows in Lecture 4.
```

```{index} radial distortion
```

```{index} epipolar line
```

```{index} epipole
```

```{index} fundamental matrix
```

```{index} rectification
```
