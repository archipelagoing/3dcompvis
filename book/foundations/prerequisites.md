(prerequisites)=
# Prerequisite refresher

You should be comfortable with algebra, trigonometry, basic probability, matrix operations, and introductory calculus. You do not need previous experience with 3D computer vision. Each lecture will refresh the specific tools it uses.

## A quick readiness check

- **Vectors:** interpret a dot product, a cross product, and vector length geometrically.
- **Matrices:** check multiplication dimensions, distinguish an inverse from a transpose, and solve a small linear system.
- **Calculus:** interpret a derivative as local sensitivity and a first-order Taylor expansion as a local approximation.
- **Linear algebra:** distinguish eigenvectors from singular vectors and understand a nullspace as the set of solutions to a homogeneous linear system.
- **Probability:** calculate the complement of repeated independent failures.

Attempt the check below. Further numerical refreshers will be added when the corresponding lectures are written.

```{understanding-check} Check — can these matrices be multiplied?
A matrix $A$ has shape $3\times4$ and a vector $X$ has shape $4\times1$. What is the shape of $AX$? Can $XA$ be formed?
```

```{admonition} Solution
:class: dropdown
The inner dimensions of $AX$ agree, so its shape is $3\times1$. The product $XA$ cannot be formed: its inner dimensions would be $1$ and $3$. This is the dimension check used later in camera projection.
```

## Matrix and vector tools used in Lecture 1

A **basis** is a set of independent directions that can build every vector in the space. In 2D, $(1,0)$ and $(0,1)$ are the standard basis. The columns of a transformation matrix tell you where these basis vectors go. This is the derivation behind the rotation matrix in {ref}`lec01-transformations`.

A **dot product** multiplies matching entries and adds them. For perpendicular vectors it is zero. In geometry it can test whether a point satisfies line or plane coefficients; the roles of the input vectors matter. A **cross product** of two 3-vectors is perpendicular to both, with magnitude equal to the area of their spanned parallelogram. Parallel inputs give zero. See {eq}`eq-lec01-cross` for its components and a geometric application.

The **transpose** swaps rows and columns; it does not generally invert a matrix. An **inverse** undoes the transformation and exists only for an invertible square matrix. Rotation matrices are special: their inverse equals their transpose. A **determinant** is a signed area/volume scale for a square linear map. Zero means collapse of at least one independent direction; a proper rotation has determinant $+1$.

## Rank, nullspaces, and SVD

**Rank** counts independent output directions. If a matrix sends a nonzero vector to zero, that vector belongs to its **nullspace**. A $3\times4$ matrix of rank three has a one-dimensional nullspace: every solution is a scalar multiple of one nonzero vector. This is precisely the scale ambiguity of a homogeneous plane or point.

A **singular value decomposition (SVD)** writes a real matrix as $A=U\Sigma V^T$, where $U,V$ have orthonormal columns in their full forms and $\Sigma$ contains nonnegative singular values. Geometrically, the map changes orthonormal coordinates, scales directions, then changes coordinates again. A right singular vector belonging to zero singular value is mapped to zero.

For the $3\times4$ incidence systems in {ref}`lec01-planes`, a full SVD supplies a $4\times4$ $V$: its last column spans the nullspace when rank is three. A reduced decomposition may omit that column. This implementation detail matters even when the geometric derivation is correct.

An **eigenvector** satisfies $Av=\lambda v$: its direction is preserved, though its scale may change. A rotation axis has eigenvalue one. Eigenvectors and singular vectors solve different questions and should not be interchanged.

```{understanding-check} Refresher — a null vector is not the zero answer
For $A=\begin{pmatrix}1&0&-2\\0&1&-3\end{pmatrix}$, verify a nonzero null vector and explain what “up to scale” means.
```

```{admonition} Solution
:class: dropdown
$A(2,3,1)^T=(0,0)^T$. Every nonzero multiple of $(2,3,1)^T$ is another valid null vector. The zero vector is also an algebraic solution, but it cannot represent a projective point. The matrix has rank two and one free scale direction.
```
