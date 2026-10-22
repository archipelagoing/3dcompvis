(lec05-tldr)=
# TLDR

**Find it → track it → describe it → verify it.** These are different jobs, even when one pipeline does all four.

- A good feature is repeatable, distinctive, compact, and local. Flat patches constrain neither motion direction; edges constrain one; useful corners constrain both.
- The structure tensor collects gradient outer products. Its smallest eigenvalue exposes the weak direction. Two large gradient components at one edge do not imply two independent constraints.
- Harris scores candidates; thresholding removes weak responses; NMS removes nearby duplicates. Shi–Tomasi tests the smallest eigenvalue directly.
- Lucas–Kanade linearizes brightness constancy, stacks patch equations, solves for displacement, warps, and repeats. Pyramids reduce the apparent motion; consistency checks detect drift and failures.
- Exposure normalization can remove positive affine brightness changes, but a flat or clipped patch remains problematic.
- Binary descriptions store intensity comparisons. Hamming distance counts different bits. ORB steers comparisons; BRISK uses long pairs for orientation and short pairs for bits.
- A ratio test checks distinctiveness; geometry checks whether a match is physically plausible. Precision and recall use different denominators.

## Short quiz

These are **original practice questions**, separate from the historical/booklet [quiz workbook](quiz-workbook.md). Try each before opening its answer. All answers are printed in the PDF.

### Question 1

```{original-question} Original practice question
A patch has two gradient samples $(2,2)^T$, each with weight one. Is it a stable two-directional feature?
```

`````{worked-solution} Answer 1

````{solution-step} 1 — Form the outer products
**Why:** Different pixels help only if they supply independent directions.

$$M=2\begin{pmatrix}4&4\\4&4\end{pmatrix}=\begin{pmatrix}8&8\\8&8\end{pmatrix}.$$
````

````{solution-step} 2 — Test its weak direction
**Why:** A zero eigenvalue means an unconstrained shift.

$$M(1,-1)^T=(0,0)^T,\qquad\lambda=16,0.$$
It is edge-like, not a stable two-directional feature.
````
`````

### Question 2

```{original-question} Original practice question
For $M=\operatorname{diag}(4,9)$ and $k=0.04$, compute the Harris response and Shi–Tomasi score.
```

`````{worked-solution} Answer 2

````{solution-step} 1 — Compute determinant and trace
**Why:** Harris uses both directional responses.

$$\det M=36,\quad\operatorname{tr}M=13,\quad R_H=36-0.04(169)=29.24.$$
````

````{solution-step} 2 — Read the weaker eigenvalue
**Why:** Shi–Tomasi measures the least-constrained direction.

$$R_{ST}=\min(4,9)=4.$$
Compare scores against thresholds defined for these weights and intensity units.
````
`````

### Question 3

```{original-question} Original practice question
Solve $Ad=b$ for $A=\left(\begin{smallmatrix}1&0\\0&1\\1&1\end{smallmatrix}\right)$ and $b=(2,1,3)^T$.
```

`````{worked-solution} Answer 3

````{solution-step} 1 — Write the normal equations
**Why:** All patch rows must contribute to the displacement estimate.

$$A^TA=\begin{pmatrix}2&1\\1&2\end{pmatrix},\quad A^Tb=\begin{pmatrix}5\\4\end{pmatrix}.$$
````

````{solution-step} 2 — Solve and substitute
**Why:** Substitution checks signs and arithmetic.

$$2u+v=5,\quad u+2v=4\Rightarrow d=(2,1)^T,$$
$$Ad=(2,1,3)^T=b.$$
````
`````

### Question 4

```{original-question} Original practice question
A tracker estimates $(3,1)$ pixels at a pyramid level two reductions below full resolution. What full-resolution initialization follows?
```

`````{worked-solution} Answer 4

````{solution-step} 1 — Transfer one level
**Why:** Each finer image has twice as many pixels per displacement.

$$d_{next}=2(3,1)^T=(6,2)^T.$$
````

````{solution-step} 2 — Transfer the next level
**Why:** Repeat the same conversion; refine after each transfer in an actual tracker.

$$d_{full}=2(6,2)^T=(12,4)^T.$$
````
`````

### Question 5

```{original-question} Original practice question
The two nearest descriptor distances are 7 and 8. Does the match pass a strict ratio threshold of 0.8?
```

`````{worked-solution} Answer 5

````{solution-step} 1 — Compute the ratio
**Why:** The second-best candidate measures ambiguity.

$$\rho=7/8=0.875.$$
````

````{solution-step} 2 — Apply the stated rule
**Why:** Being closest does not mean being distinctive.

$$0.875\not<0.8.$$
Reject this proposed match under the given policy.
````
`````

### Question 6

```{original-question} Original practice question
Among accepted matches, 18 are correct and 4 incorrect. Two true matches were missed. What are precision and recall?
```

`````{worked-solution} Answer 6

````{solution-step} 1 — Compute accepted-match reliability
**Why:** Precision counts accepted decisions in its denominator.

$$P=18/(18+4)=9/11\approx81.82\%.$$
````

````{solution-step} 2 — Compute true-match coverage
**Why:** Recall counts all actual matches in its denominator.

$$R=18/(18+2)=90\%.$$
````
`````

