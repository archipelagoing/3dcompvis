(lec01-quiz-practice)=
(lec02-geometry)=
# Foundation quiz practice

Apply the geometry and camera formulas from this chapter to **Spring 2020 Quiz 1**. The supplied quiz map assigns it to Lecture 2. Its [complete quiz workbook](../lecture02/quiz-workbook.md) now contains the original problems and colored step-by-step solutions; this page connects them to the foundational rules.

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

**Worked example 1.17 — the dot/cross quiz.** {ref}`Read the original problem and every worked step <quiz-8-q1>`.

## Quiz Problem 2: what size is a camera matrix?

**Worked example 1.18 — dimensions before arithmetic.** {ref}`Read the original problem and every worked step <quiz-8-q2>`.

## Quiz Problem 3: how many intersections?

```{figure} ../../images/lecture02/quiz-lines.*
:name: fig-lec02-lines
:width: 85%
:alt: Two vertical lines cross a horizontal line at two finite points and share a vertical ideal point.

The third intersection is at infinity. It has no ordinary position on this finite drawing. Original diagram of Quiz Problem 3.
```

**Worked example 1.19 — count in the projective plane.** {ref}`Read the original problem and every worked step <quiz-8-q3>`.

```{understanding-check} Check 1.8 — test a point off the line
Replace $c$ in Example 1.17 by $(5,1,1)^T$. What changes?
```

```{admonition} Answer
:class: dropdown
The dot product is $2$: the three points are not collinear.
```

```{index} collinearity
```
