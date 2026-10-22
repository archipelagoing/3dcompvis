```{raw} latex
\clearpage
```

(lec04-tldr)=
# TLDR

**Lecture 4 in one sentence:** estimate valid two-view geometry, choose a camera pose that sees the scene, and turn reliable stereo matches into depths with honest error estimates.

## The important things

1. **Keep points, lines, and scalars distinct.** A pixel defines a ray; that ray and the baseline define a plane whose intersection with the other image is a line. Compute that line with $Fx$, then test a candidate using $x'^TFx=0$. The assigned quizzes practice symbolic expansion and third-view prediction. Two lines in a third image can locate a point, unless their intersection is degenerate. See [quiz practice](epipolar-practice.md).
2. **Check rank before trusting “F.”** Fall 2025 Quiz 2 supplies a rank-three matrix. Its bilinear equation can be solved, but it is not valid pinhole-camera geometry. A noisy estimate requires a rank-two correction and pixel-space residual checks. See [estimation](estimation.md).
3. **Calibration supplies an essential matrix.** $E=K'^TFK=[t]_\times R$ has equal nonzero singular values and one zero. It recovers translation direction, not metric scale. Numerical conditioning transforms and camera calibration are different operations. See [essential geometry](essential.md).
4. **Test all four poses.** Two rotations and two translation signs produce four candidates. Positive reconstructed depths in both cameras select the visible configuration for suitable nondegenerate data. Translation $t$ is not the second camera center.
5. **Disparity is inverse depth.** In the specified rectified convention, $Z=fb/d$. Use focal length and disparity in pixels, baseline and depth in one length unit. Account for unequal principal-point columns. See [stereo](stereo.md).
6. **A one-pixel depth error is not symmetric.** Underestimating disparity pushes the point farther by more than an equal overestimate pulls it nearer. Use the exact error when the disparity error is a substantial fraction of disparity. Small disparities are especially fragile: local error magnitude is approximately $Z^2|\delta|/(fb)$. At fixed cameras and small disparity error, doubling depth roughly quadruples absolute error.
7. **Appearance chooses among geometric candidates.** Dense stereo generates hypotheses, evaluates costs, aggregates support, and selects or rejects. Minimize SAD/SSD; maximize NCC. Flat patches, repetitions, and occlusions can defeat a low-cost match. See [matching](matching.md).
8. **Support has assumptions.** A constant-disparity window favors fronto-parallel surfaces; large windows can mix depths. Shifted, elongated, weighted, or oriented-plane support can help. Rank retains a count; Census retains the ordered relative-intensity pattern. None removes ambiguity automatically.

```{raw} latex
\newpage
```

## Short quiz

These original questions test this chapter's additions.

Each question has its own complete worked answer below. Open it after trying the problem; all answers are visible in print.

(lec04-tldr-q1)=
### Question 1

````{original-question} Original practice question
For $x_A=(0,1,1)^T$, $x_B=(1,0,1)^T$, expand $x_B^TFx_A$ in matrix entries.
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Multiply the point into F
**Why:** The zero first coordinate selects columns two and three.

$$
\begin{aligned}Fx_A&=\begin{pmatrix}f_{11}&f_{12}&f_{13}\\f_{21}&f_{22}&f_{23}\\f_{31}&f_{32}&f_{33}\end{pmatrix}\begin{pmatrix}0\\1\\1\end{pmatrix}\\&=\begin{pmatrix}f_{12}+f_{13}\\f_{22}+f_{23}\\f_{32}+f_{33}\end{pmatrix}.\end{aligned}
$$
````

````{solution-step} 2 — Dot with the second point
**Why:** Its transpose selects the first and third output entries.

$$
\begin{pmatrix}1&0&1\end{pmatrix}\begin{pmatrix}f_{12}+f_{13}\\f_{22}+f_{23}\\f_{32}+f_{33}\end{pmatrix}=f_{12}+f_{13}+f_{32}+f_{33}=0.
$$
````

`````

(lec04-tldr-q2)=
### Question 2

````{original-question} Original practice question
Two predicted lines in image C are proportional. Does their cross product give a unique finite correspondence?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Write proportional line vectors
**Why:** Nonzero scaling represents the same homogeneous line.

Let $\ell_2=k\ell_1$ with $k\ne0$. Then $\ell_1\times\ell_2=k(\ell_1\times\ell_1)=0$.
````

````{solution-step} 2 — Interpret the zero result
**Why:** The zero homogeneous vector cannot represent a unique image point.

No unique finite correspondence is determined: the two constraints describe the same line.
````

`````

(lec04-tldr-q3)=
### Question 3

````{original-question} Original practice question
A noisy matrix has singular values $(4,2,0.2)$. What singular values do rank-two F correction and essential-form correction use?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Apply the rank-two F rule
**Why:** Only the smallest singular value must be zero.

$$
\Sigma_F=\begin{pmatrix}4&0&0\\0&2&0\\0&0&0\end{pmatrix}.
$$
````

````{solution-step} 2 — Apply the essential-matrix rule
**Why:** The first two singular values must also agree.

$$
a=(4+2)/2=3,\qquad\Sigma_E=\begin{pmatrix}3&0&0\\0&3&0\\0&0&0\end{pmatrix}.
$$

 Thus F uses $(4,2,0)$ and E uses $(3,3,0)$.
````

`````

(lec04-tldr-q4)=
### Question 4

````{original-question} Original practice question
A candidate pose reconstructs a point with depths $+5$ and $-5$ in the two cameras. Is that point a valid visible correspondence under that pose?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Check the first camera
**Why:** A visible point must have positive camera-frame depth.

The first depth $+5>0$ passes the first camera's test.
````

````{solution-step} 2 — Check the second camera
**Why:** Cheirality requires positive depth in both observing cameras.

The second depth $-5<0$ fails. Reject this point/pose combination as a valid visible correspondence.
````

`````

(lec04-tldr-q5)=
### Question 5

````{original-question} Original practice question
Rectified cameras have $b=0.2\,\mathrm m$, $f=600$ pixels, $d=30$ pixels. What is the depth? If measured disparity becomes 31, is the point reconstructed nearer or farther?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Compute the true depth
**Why:** Baseline and depth both use meters; focal length and disparity both use pixels.

$$
fb=600(0.2)=120\,\mathrm{m\,px},\qquad Z=120/30=4\,\mathrm m.
$$
````

````{solution-step} 2 — Compute the perturbed depth and sign
**Why:** A larger disparity should place the estimate nearer.

$$
\widehat Z=\frac{120}{31}\,\mathrm m,\qquad\Delta Z=\frac{120}{31}-4=\frac{120-124}{31}=-\frac4{31}\,\mathrm m\approx-0.1290\,\mathrm m.
$$

 The estimate is nearer.
````

`````

(lec04-tldr-q6)=
### Question 6

````{original-question} Original practice question
For that setup, which disparity interval corresponds to depths from 2 to 6 meters?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Evaluate the far limit
**Why:** Inverse depth makes the far endpoint the smaller disparity.

$$
d_{min}=\frac{fb}{Z_{max}}=\frac{120}{6}=20\,\mathrm{pixels}.
$$
````

````{solution-step} 2 — Evaluate the near limit
**Why:** The closer endpoint has the larger disparity.

$$
d_{max}=\frac{120}{2}=60\,\mathrm{pixels},\qquad d\in[20,60].
$$
````

`````

(lec04-tldr-q7)=
### Question 7

````{original-question} Original practice question
Which direction do you optimize SAD and NCC? Can a constant-intensity patch supply a defined zero-mean NCC score?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Identify what each score rewards
**Why:** Difference costs reward small disagreement; correlation rewards similar centered patterns.

Minimize SAD. Maximize zero-mean NCC, or equivalently minimize a consistently defined negative correlation cost.
````

````{solution-step} 2 — Check the NCC denominator
**Why:** A flat patch has no centered contrast to normalize.

For constant $I_i=c$, every $I_i-\bar I=0$, so $\sqrt{\sum_i(I_i-\bar I)^2}=0$. The NCC denominator vanishes; the normalized score is undefined.
````

`````

(lec04-tldr-q8)=
### Question 8

````{original-question} Original practice question
With center intensity 10 and ordered neighbors $(8,12,7,11)$, what are the Census string and rank under the strict darker-than-center convention?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Compare each neighbor with the center
**Why:** The strict darker-than-center convention assigns one to values below 10.

$$
\begin{pmatrix}8<10\\12<10\\7<10\\11<10\end{pmatrix}\quad\Rightarrow\quad\begin{pmatrix}1\\0\\1\\0\end{pmatrix}.
$$
````

````{solution-step} 2 — Read the string and count its ones
**Why:** Census retains order; rank retains only the count.

The Census string is $1010$. The rank is $1+0+1+0=2$.
````

`````
