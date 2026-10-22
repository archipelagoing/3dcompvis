(lec01-quiz-practice)=
(lec02-geometry)=
# Foundation quiz practice

Apply the geometry and camera formulas from this chapter to **Spring 2020 Quiz 1**. The supplied quiz map assigns it to Lecture 2; its solutions live here because they test Lecture 1 concepts.

Use {eq}`eq-lec01-incidence` and {eq}`eq-lec01-cross` for Problems 1 and 3, and {eq}`eq-lec01-camera` for Problem 2.

## Quiz Problem 1: are three points collinear?

Combining the two referenced rules gives the quiz's compact three-point test.

````{formula-box} Formula — collinearity test
```{math}
:label: eq-lec02-collinear
s=c^T(a\times b),\qquad s=0\quad\text{for collinear points}.
```

$a,b,c$ are nonzero homogeneous $3\times1$ point vectors. The zero/nonzero result is unchanged by rescaling them. This is an exact determinant test. For measured points, a small unnormalized $s$ is not a meaningful distance threshold.
````

```{application} Check collinearity without accepting an invalid line
1. Check that all point vectors are nonzero.
2. Form $a\times b$. If it vanishes, choose another distinct pair.
3. Dot that line with the third point; zero means incidence.

If all three represent the same point, no unique joining line exists. Any line through that point contains the repeated inputs. See Example 1.17.
```

(ex-lec02-collinear)=
```{worked-example} Worked example 1.17 — the dot/cross quiz
**Source:** `cs532s20_quiz1.pdf`, Problem 1; numerical illustration is original.

Take $a=(0,0,1)^T$, $b=(2,0,1)^T$, and $c=(5,0,1)^T$. Then $a\times b=(0,2,0)^T$ and $c^T(a\times b)=0$: all lie on $y=0$.

The quiz asks when the test fails. If $b=2a$, the cross product is zero and cannot define a line. Its dot product with **any** $c$ is zero. This fails to construct a unique line. Mathematically the determinant still correctly reports linear dependence, and a line through the repeated point and $c$ exists. Distinguish **collinearity as existence** from **construction of a unique line**.
```

## Quiz Problem 2: what size is a camera matrix?

(ex-lec02-projection)=
````{worked-example} Worked example 1.18 — dimensions before arithmetic
**Source:** `cs532s20_quiz1.pdf`, Problem 2, both parts.

A homogeneous 3D point has four entries; an image point has three. Therefore $M$ is **$3\times4$**, since $(3\times4)(4\times1)=3\times1$. See the general mapping in {eq}`eq-lec01-camera`.

For $X=(X_1,X_2,X_3,X_4)^T$, the ordinary coordinates are

$$
u=\frac{m_{11}X_1+m_{12}X_2+m_{13}X_3+m_{14}X_4}
{m_{31}X_1+m_{32}X_2+m_{33}X_3+m_{34}X_4},
$$
$$
v=\frac{m_{21}X_1+m_{22}X_2+m_{23}X_3+m_{24}X_4}
{m_{31}X_1+m_{32}X_2+m_{33}X_3+m_{34}X_4}.
$$

For a finite world point choose $X_4=1$. Both fractions require a nonzero denominator. If $MX$ is nonzero with last entry zero, the image point is ideal; if $MX=0$, projection is undefined, as at the camera center. Nonzero rescaling of $X$ or $M$ changes neither fraction.
````

## Quiz Problem 3: how many intersections?

```{figure} ../../images/lecture02/quiz-lines.*
:name: fig-lec02-lines
:width: 85%
:alt: Two vertical lines cross a horizontal line at two finite points and share a vertical ideal point.

The third intersection is at infinity. It has no ordinary position on this finite drawing. Original diagram of Quiz Problem 3.
```

(ex-lec02-intersections)=
```{worked-example} Worked example 1.19 — count in the projective plane
**Source:** `cs532s20_quiz1.pdf`, Problem 3, both parts.

Assume $d>0$ for two distinct vertical lines each distance $d$ from the origin. Choose $\ell_1=(1,0,-d)^T$ for $x=d$, $\ell_2=(1,0,d)^T$ for $x=-d$, and $\ell_3=(0,1,0)^T$ for $y=0$.

Use {eq}`eq-lec01-cross` for each pair:

1. $\ell_1\times\ell_3=(d,0,1)^T$ gives $(d,0)$.
2. $\ell_2\times\ell_3=(-d,0,1)^T$ gives $(-d,0)$.
3. $\ell_1\times\ell_2=(0,-2d,0)^T\sim(0,1,0)^T$ is the vertical ideal point.

There are **three distinct projective intersections**, of which **two are finite**. The ideal point happens to have the same entries as the horizontal line's coefficients; its geometric type comes from how it is used. Setting $d=0$ violates the distinct-line assumption.
```

```{understanding-check} Check 1.8 — test a point off the line
Replace $c$ in Example 1.17 by $(5,1,1)^T$. What changes?
```

```{admonition} Answer
:class: dropdown
The dot product is $2$: the three points are not collinear.
```

```{index} collinearity
```
