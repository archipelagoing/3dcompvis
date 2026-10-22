(notation)=
# Notation and coordinate conventions

These conventions apply throughout the book. A source using another convention will be translated explicitly.

| Symbol | Meaning | Shape / units |
| --- | --- | --- |
| $\mathbf{X}$ | Homogeneous 3D point | $4\times1$; scale arbitrary |
| $\mathbf{x}$ | Homogeneous image point | $3\times1$; scale arbitrary |
| $(u,v)$ | Inhomogeneous pixel coordinates | pixels |
| $\mathbf{X}_c$ | Euclidean camera point $(X_c,Y_c,Z_c)^T$ | $3\times1$; one consistent length unit |
| $\mathbf{K}$ | Camera intrinsic matrix | $3\times3$; focal entries in pixels |
| $\mathbf{R},\mathbf{t}$ | World-to-camera rotation and translation | $3\times3$, $3\times1$ |
| $\mathbf{C}$ | Camera center in world coordinates | $3\times1$; $\mathbf{C}=-\mathbf{R}^T\mathbf{t}$ |
| $\mathbf{P}$ | Homogeneous camera projection matrix | $3\times4$ |
| $\mathbf{H},\mathbf{F},\mathbf{E}$ | Homography, fundamental matrix, essential matrix | each $3\times3$, with different constraints |
| $\boldsymbol\ell,\boldsymbol\pi$ | Homogeneous line / plane coefficients | $3\times1$ / $4\times1$ |

## Frames, axes, and transformations

Vectors are columns. Image $u$ increases rightward and $v$ downward. Use right-handed camera axes with positive $Z_c$ forward. Specify any different image-plane convention in the figure and derivation.

Write $\mathbf{T}_{B\leftarrow A}$ for a transform that maps coordinates from frame $A$ into frame $B$. In a product, the rightmost transform acts first. State whether a rotation acts on points or changes the coordinate frame. Use scalar-first unit quaternions $(q_w,q_x,q_y,q_z)$ and define the rotation convention before applying them.

```{figure} ../images/lecture01/pixel-axes.*
:name: fig-pixel-axes
:width: 85%
:alt: Pixel origin at the upper left, with u increasing right and v increasing downward.

The pixel-axis convention used throughout the book. The marked pixel is illustrative, not a calibrated measurement. Original diagram; editable TikZ source is retained with the figure assets.
```

## Equality and homogeneous scale

**Homogeneous coordinates** represent a point by a nonzero vector up to nonzero scale; see {term}`homogeneous coordinates`. Use $=$ for equality of vectors and $\sim$ for equality up to scale. A zero vector is never a projective point.

```{index} homogeneous coordinates; scale equivalence
```

````{formula-box} Formula — homogeneous scale equivalence
```{math}
:label: eq-homogeneous-scale
\mathbf{x}\sim\lambda\mathbf{x},\qquad \lambda\ne0.
```

**Meaning:** scaling all coordinates by the same nonzero number preserves the represented point. Here $\mathbf{x}\in\mathbb{R}^3\setminus\{\mathbf{0}\}$ and $\lambda$ is a scalar. This is an exact projective equivalence, not a numerical approximation.

When the third coordinate $w$ is nonzero, the corresponding Euclidean point is $(x_1/w,x_2/w)$. When $w=0$, the point is ideal and this division is invalid.
````

```{application} Application — compare two representations
1. Check that neither vector is zero.
2. Determine whether one nonzero scalar multiplies every component of the first vector to produce the second.
3. For finite points, divide by the last coordinate and compare the resulting Euclidean coordinates.

For example, $(2,4,2)^T$ and $(1,2,1)^T$ represent the same finite point $(1,2)$, although the two vectors are not equal. This is an original notation example; lecture-specific derivations and slide references will be added with the chapters.
```

## Numerical checks

Keep pixels distinct from physical lengths. Convert centimeters and meters before substitution. Report exact values before rounded approximations. Distinguish a formula's mathematical conditions from numerical conditioning and state a justified tolerance when checking floating-point results.
