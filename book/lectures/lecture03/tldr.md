```{raw} latex
\clearpage
```

(lec03-tldr)=
# TLDR

**Lecture 3 in one sentence:** use camera geometry to solve concrete calibration and depth problems, then distinguish a probable clean sample from an identifiable correct model.

## The important things

1. **FOV determines horizontal focal length only after stating the model.** A centered 640-pixel-wide, 90° pinhole view gives $f_x=320$ pixels. Square pixels, zero skew, and a centered principal point supply the remaining assumptions for the quiz's $K$. See [calibration](calibration.md).
2. **Pixel focal length is not physical focal length.** Multiply by physical pixel pitch to change units. The principal point is $(c_x,c_y)$ in pixels but $(0,0,f_{\rm phys})$ on the positive virtual image plane.
3. **A scaled Euclidean 3D vector stays on the same camera ray.** The image-plane intersection is one tenth of the scene vector when $f=Z/10$. Its cross product with that vector is zero. See [the ray quiz](ray-plane.md).
4. **A known plane can supply missing depth.** Use {eq}`eq-lec03-ray-plane`, then check plane incidence, reprojection, and positive depth. A parallel ray may have no intersection or lie entirely in the plane.
5. **Projective mappings do not preserve coordinate averages.** The fitted trapezoid's mapped center differs from the average of its corners. The [normalized DLT walkthrough](homography-practice.md) shows all the numerical stages.
6. **Count the complement when attempts repeat.** The coin quiz gives $1/8$ per attempt and $1-(7/8)^7\approx60.73\%$ across seven independent attempts. See [probability](probability-ransac.md).
7. **State the sampler before quoting a RANSAC budget.** The pentagon has 25 candidate pairs and five correct pairs for one alignment. The standard independent-status approximation gives 2,876 trials for 99%; exact finite-pool rules give different counts.
8. **Symmetry is missing information.** An unlabeled regular pentagon permits ten corner alignments without orientation constraints. More trials cannot select the intended one; extra asymmetric evidence can.

```{raw} latex
\newpage
```

## Short quiz

These original questions test this chapter's applications.

Each question has its own complete worked answer below. Open it after trying the problem; all answers are visible in print.

(lec03-tldr-q1)=
### Question 1

````{original-question} Original practice question
A centered pinhole image is 800 pixels wide with 90° horizontal FOV. What is $f_x$? Does that alone determine $f_y$?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Use the half-angle triangle
**Why:** A centered 90-degree horizontal field gives a 45-degree half angle.

$$
f_x=\frac{800/2}{\tan45^\circ}=\frac{400}{1}=400\,\mathrm{pixels}.
$$
````

````{solution-step} 2 — Identify the missing parameter
**Why:** A horizontal angular measurement constrains horizontal focal length only.

It does not determine $f_y$ without a pixel-shape or other calibration assumption.
````

`````

(lec03-tldr-q2)=
### Question 2

````{original-question} Original practice question
If $f_x=400$ pixels and pixel pitch is $0.004\,\mathrm{mm/pixel}$, where is the principal point on the positive virtual image plane in camera-frame millimeters?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Convert pixel focal length to millimeters
**Why:** Pixel pitch supplies the missing physical length per pixel.

$$
f_{phys}=(400\,\mathrm{px})(0.004\,\mathrm{mm/px})=1.6\,\mathrm{mm}.
$$
````

````{solution-step} 2 — Locate the principal point
**Why:** It is on the camera optical axis at the virtual image plane.

Its camera-frame position is $(0,0,1.6)^T\,\mathrm{mm}$. This is different from its image-array pixel coordinate.
````

`````

(lec03-tldr-q3)=
### Question 3

````{original-question} Original practice question
For a scene vector $(3,2,30)^T$ and $f=3$, what is its image-plane 3D intersection? What is the cross product of the two vectors?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Scale onto the image plane
**Why:** The ray's third coordinate must become the focal depth.

$$
a=\frac{f}{Z}\begin{pmatrix}3\\2\\30\end{pmatrix}=\frac3{30}\begin{pmatrix}3\\2\\30\end{pmatrix}=\begin{pmatrix}0.3\\0.2\\3\end{pmatrix}.
$$
````

````{solution-step} 2 — Expand the cross product
**Why:** Parallel 3D ray vectors must have zero cross product.

$$
\begin{pmatrix}3\\2\\30\end{pmatrix}\times\begin{pmatrix}.3\\.2\\3\end{pmatrix}=\begin{pmatrix}2(3)-30(.2)\\30(.3)-3(3)\\3(.2)-2(.3)\end{pmatrix}=\begin{pmatrix}0\\0\\0\end{pmatrix}.
$$
````

`````

(lec03-tldr-q4)=
### Question 4

````{original-question} Original practice question
A ray is $P=Z(0.5,0,1)^T$ and the known plane is $X+Z=12$. Find $Z$ and $P$.
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Substitute the ray into the plane
**Why:** At the intersection both descriptions must hold.

$$
X+Z=0.5Z+Z=12\quad\Rightarrow\quad1.5Z=12\quad\Rightarrow\quad Z=8.
$$
````

````{solution-step} 2 — Recover and check the point
**Why:** The recovered depth scales the complete ray direction.

$$
P=8\begin{pmatrix}.5\\0\\1\end{pmatrix}=\begin{pmatrix}4\\0\\8\end{pmatrix}.
$$

 It has positive depth and gives $4+8=12$ in the plane equation.
````

`````

(lec03-tldr-q5)=
### Question 5

````{original-question} Original practice question
What happens if a ray has $\gamma=0$ for a plane with $D\ne0$?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Write the reduced intersection equation
**Why:** Substitution always produces the scalar equation gamma times depth plus D equals zero.

$$
\gamma Z+D=0.
$$

 With $\gamma=0$ this reduces to $D=0$.
````

````{solution-step} 2 — Check the stated nonzero offset
**Why:** The supplied D contradicts that required equality.

Since $D\ne0$, there is no finite solution. The viewing ray is parallel to a plane that does not contain the camera center.
````

`````

(lec03-tldr-q6)=
### Question 6

````{original-question} Original practice question
For Example 3.5's matrix, where does source point $(0.5,0.5)$ go? Is it the destination vertex average?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Multiply the supplied example matrix
**Why:** Projective coordinates must be transformed before averaging or division.

$$
\begin{pmatrix}4&0&0\\0&2&0\\1&0&1\end{pmatrix}\begin{pmatrix}.5\\.5\\1\end{pmatrix}=\begin{pmatrix}2\\1\\1.5\end{pmatrix}.
$$
````

````{solution-step} 2 — Normalize and compare
**Why:** A projective map does not generally preserve ordinary coordinate averages.

$$
 (u,v)=\left(\frac2{1.5},\frac1{1.5}\right)=\left(\frac43,\frac23\right).
$$

 This differs from the destination vertex average $(1,3/4)$.
````

`````

(lec03-tldr-q7)=
### Question 7

````{original-question} Original practice question
If one independent attempt succeeds with probability $1/4$, what is the chance of at least one success in three attempts?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Count three failures
**Why:** Independent failures are easier to count than all success patterns.

$$
P(\text{no success})=(1-1/4)^3=(3/4)^3=27/64.
$$
````

````{solution-step} 2 — Take the complement
**Why:** At least one success is the complement of no successes.

$$
P(\text{at least one})=1-27/64=37/64=0.578125\approx57.81\%.
$$
````

`````

(lec03-tldr-q8)=
### Question 8

````{original-question} Original practice question
A regular pentagon gives several equally supported alignments. Will increasing RANSAC's trial count identify the intended alignment? Name evidence that could.
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Identify the ambiguity
**Why:** Several models have the same corner evidence.

Increasing the number of samples does not change that evidence, so it cannot identify the intended alignment.
````

````{solution-step} 2 — Supply asymmetric evidence
**Why:** The competing alignments must make different predictions about something observable.

A distinctive visible mark, labeled corner or other asymmetric scene cue can distinguish them. More identical unlabeled corners do not remove this symmetry.
````

`````
