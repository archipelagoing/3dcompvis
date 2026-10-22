(lec02-tldr)=
# TLDR

**Lecture 2 in one sentence:** estimate planar image mappings from trustworthy matches, resample them correctly, and recognize when distortion or 3D depth requires another model.

## The important things

1. **Convert quaternions consistently.** This chapter adds quaternion-to-matrix and matrix-to-quaternion formulas. The scalar extraction is $w=\tfrac12\sqrt{1+\operatorname{tr}R}$; near a half-turn, use a largest-component branch. See {ref}`lec02-quaternions`.
2. **SLERP interpolates orientations.** Align endpoint quaternion signs, then interpolate along the unit sphere. For nearly identical orientations, normalized linear interpolation avoids an unstable denominator.
3. **A plane can be rectified with four nondegenerate matches.** A homography supplies the mapping; the destination rectangle's aspect ratio needs known geometry for metric accuracy. Raised objects and hidden floor cannot be reconstructed by a floor warp. See {ref}`lec02-homographies`.
4. **Cross-ratio survives perspective.** For four ordered collinear coordinates, $\operatorname{CR}(a,b;c,d)=(c-a)(d-b)/((c-b)(d-a))$. Ordinary spacings may change while this value stays fixed.
5. **Inverse warping fills the output grid.** For each destination pixel, use $H^{-1}$ to locate its source sample. Bilinear interpolation blends four neighbors with weights summing to one; strong shrinking also needs antialiasing. See {ref}`lec02-warping`.
6. **DLT estimates the mapping; normalization stabilizes it.** Each homography match contributes two rows to a $2n\times9$ system. The smallest right singular vector supplies the matrix entries. Normalize each image independently, then recover $H=(T')^{-1}\widetilde H T$. See {ref}`lec02-estimation`.
7. **RANSAC rejects inconsistent matches.** Sample → fit → score → repeat → refit. Under its sampling assumptions, use $N=\lceil\log(1-p)/\log(1-w^s)\rceil$, where $w$ is the inlier fraction, $s$ the sample size, and $p$ the desired sampling success probability. Consensus is not proof of a correct model.
8. **Distortion and depth variation require different tools.** Radial correction straightens lens-bent edges. The fundamental matrix constrains correspondence by $\ell'=Fx$ and $x'^TFx=0$; it has rank two and seven DOF. Rectification aligns corresponding epipolar lines with matching rows. See {ref}`lec02-two-view`.

## Short quiz

These original questions test the additions in this chapter. Foundation quiz solutions are in {ref}`lec01-quiz-practice`.

Each question has its own complete worked answer below. Open it after trying the problem; all answers are visible in print.

(lec02-tldr-q1)=
### Question 1

````{original-question} Original practice question
For a proper rotation with trace zero, what scalar quaternion component does the trace branch give?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Insert the trace
**Why:** This branch extracts the nonnegative quaternion scalar from a proper rotation.

$$
w=\frac12\sqrt{1+\operatorname{tr}R}=\frac12\sqrt{1+0}=\frac12.
$$
````

````{solution-step} 2 — State the sign convention
**Why:** A quaternion and its negative encode the same rotation.

The trace branch chooses $w=+1/2$; negating the entire quaternion gives an equivalent representation.
````

`````

(lec02-tldr-q2)=
### Question 2

````{original-question} Original practice question
Before SLERP, what should you do if the endpoint quaternions have a negative dot product?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Inspect the quaternion dot product
**Why:** Opposite quaternion signs can describe equivalent rotations.

If $q_0^Tq_1<0$, replace one endpoint by its negative: $q_1\leftarrow-q_1$.
````

````{solution-step} 2 — Check the resulting path
**Why:** Sign alignment avoids taking the unnecessarily long interpolation arc.

$$
q_0^T(-q_1)=-q_0^Tq_1>0.
$$

 SLERP then uses sign-aligned endpoints for a shortest rotation path; handle nearly equal endpoints with a stable interpolation branch.
````

`````

(lec02-tldr-q3)=
### Question 3

````{original-question} Original practice question
What is $\operatorname{CR}(0,1;2,3)$? Should a projective warp of the line change it?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Substitute all four coordinates
**Why:** The ordering fixes which cross-ratio is being evaluated.

$$
\operatorname{CR}(0,1;2,3)=\frac{(2-0)(3-1)}{(2-1)(3-0)}=\frac{2\cdot2}{1\cdot3}=\frac43.
$$
````

````{solution-step} 2 — Apply projective invariance
**Why:** A valid projectivity preserves this ordered collinear ratio.

The warped points have the same cross-ratio $4/3$, even when their ordinary distances change. Keep their order and handle ideal coordinates homogeneously if needed.
````

`````

(lec02-tldr-q4)=
### Question 4

````{original-question} Original practice question
How many nondegenerate matches and how many DLT rows are needed for a minimal homography estimate?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Count the constraints
**Why:** Each homography correspondence supplies two independent linear rows.

A homography has nine entries up to one common nonzero scale, leaving eight degrees of freedom. Four pairs give $2(4)=8$ equations.
````

````{solution-step} 2 — State the system and its rank
**Why:** A unique homogeneous solution needs a one-dimensional nullspace.

$$
A\in\mathbb R^{8\times9},\qquad \operatorname{rank}A=8,\qquad Ah=0.
$$

 Four nondegenerate matches are minimal; degenerate arrangements need additional usable information.
````

`````

(lec02-tldr-q5)=
### Question 5

````{original-question} Original practice question
A source-to-destination warp translates content by $(6,-2)$ pixels. Where does destination pixel $(10,10)$ sample?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Invert the translation
**Why:** An output pixel must look backward to its source location.

$$
H^{-1}=\begin{pmatrix}1&0&-6\\0&1&2\\0&0&1\end{pmatrix}.
$$
````

````{solution-step} 2 — Multiply the output pixel
**Why:** The inverse warp identifies which source pixel to sample.

$$
H^{-1}\begin{pmatrix}10\\10\\1\end{pmatrix}=\begin{pmatrix}10-6\\10+2\\1\end{pmatrix}=\begin{pmatrix}4\\12\\1\end{pmatrix}.
$$

 Sample source $(4,12)$.
````

`````

(lec02-tldr-q6)=
### Question 6

````{original-question} Original practice question
Four neighboring intensities are $0,20,40,60$. What is their bilinear value at the center of the square?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Find the four weights
**Why:** The center is halfway along both axes of the square.

Each bilinear weight is $(1/2)(1/2)=1/4$. The weights sum to one.
````

````{solution-step} 2 — Take the weighted sum
**Why:** Bilinear interpolation combines all four neighboring values.

$$
I=\frac14(0)+\frac14(20)+\frac14(40)+\frac14(60)=\frac{120}{4}=30.
$$
````

`````

(lec02-tldr-q7)=
### Question 7

````{original-question} Original practice question
For $p=0.99$, $w=0.8$, $s=4$, is the standard RANSAC budget 8 or 9 trials? Does it guarantee the correct model?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Compute one clean-sample probability
**Why:** The standard model treats the four sampled inlier statuses as independent.

$$
q=w^s=0.8^4=0.4096.
$$
````

````{solution-step} 2 — Round the trial budget upward
**Why:** A fractional number of trials must be rounded up to meet the target probability.

$$
N=\left\lceil\frac{\ln(1-0.99)}{\ln(1-0.4096)}\right\rceil=\lceil8.7392\ldots\rceil=9.
$$
````

````{solution-step} 3 — Interpret the guarantee correctly
**Why:** Sampling success alone cannot certify the final model.

The calculation concerns at least one clean sample under the stated assumptions. Degeneracy, an unsuitable threshold or ambiguous image content can still spoil the estimated model.
````

`````

(lec02-tldr-q8)=
### Question 8

````{original-question} Original practice question
If $Fx=(0,-1,4)^T$, what must a matching ordinary point $(u',v')$ satisfy? Is $u'$ determined?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Test point-line incidence
**Why:** The three supplied numbers are line coefficients.

$$
\begin{pmatrix}u'&v'&1\end{pmatrix}\begin{pmatrix}0\\-1\\4\end{pmatrix}=0u'-v'+4=0.
$$
````

````{solution-step} 2 — Read the free coordinate
**Why:** A line imposes one equation on two ordinary coordinates.

Thus $v'=4$, while $u'$ is not determined. Image evidence must select the actual match along the line.
````

`````
