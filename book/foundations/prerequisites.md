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
