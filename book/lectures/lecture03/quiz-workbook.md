(lec03-quiz-workbook)=
# Original quiz questions and worked solutions

**Read the problem in black. Follow the numbered red steps. Work through the blue mathematics.** Every step explains why it is needed. Matrix calculations show the inputs and intermediate results; written-reasoning questions explain the decision instead of inventing numerical data.

**Source:** the supplied lecture-organized quiz booklet. Full problems follow its wording and givens, with typography normalized; the historical PDF filenames appear below. Source-key corrections and added numerical companions are marked.

**Retests have their own questions and full solutions.** Problems labeled **Original practice** are the booklet’s seven supplemental examples, separate from the 18 historical quizzes. Colored steps remain numbered and readable in grayscale.

## Jump to a quiz

- {ref}`Spring 2019 Quiz 3 — Pentagon, homography, RANSAC <quiz-source-7>`
- {ref}`Spring 2019 Quiz 2 — FOV, calibration, homogeneous scaling <quiz-source-10>`
- {ref}`Spring 2020 Quiz 3 — Duplicate camera model <quiz-source-11>`
- {ref}`Spring 2020 Quiz 2 — Pinhole ray and cross product <quiz-source-14>`
- {ref}`Older Quiz 9 — Pinhole ray intersects a 3D plane <quiz-source-15>`
- {ref}`A1. Homography, DLT and SVD (L3, slides 34–45) <quiz-source-a1>`

---

(quiz-source-7)=
## Spring 2019 Quiz 3 — Pentagon, homography, RANSAC

**Historical source:** `3dcvMid/olderquizzes/cs532s19-quiz3.pdf`.

(ex-lec03-pentagon)=
(ex-lec03-symmetry)=
(quiz-7-q1)=
### Problem 1(a–d)

````{original-question}
Two images show only the same *irregular five-sided polygon*, related by an unknown homography. All five corners are detected in each image. You create every possible putative corner correspondence. (a) How many? (b) What inlier rate? (c) How many RANSAC iterations are needed to reliably estimate the homography? (d) What changes for a regular/equilateral pentagon?
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Count all candidate pairs
**Why:** Every corner in the first image can pair with every corner in the second.

There are 5 features in image A and 5 in image B. Exhaustive matching forms all ordered cross-image pairs, so $\boxed{5\times5=25}$ putative correspondences.
````

````{solution-step} 2 — Count the true inliers
**Why:** The inlier ratio is measured relative to one intended corner assignment.

Assume one unique correct correspondence for each of the 5 image-A corners. Then 5 of the 25 pairs are inliers, so $\boxed{w=5/25=0.2}$ and outlier rate $e=0.8$.
````

````{solution-step} 3 — Set up the RANSAC probability
**Why:** A homography needs four nondegenerate correspondences in one clean sample.

The minimal homography solver requires $s=4$ nondegenerate correspondences. The usual RANSAC independent-sample approximation sets 

$$
1-(1-w^s)^N\ge p\quad\Rightarrow\quad N\ge\frac{\ln(1-p)}{\ln(1-w^s)}.
$$
````

````{solution-step} 4 — Insert a confidence level
**Why:** The question needs a chosen confidence before a numerical trial count exists.

For the *illustrative* common confidence $p=0.99$, $w^4=0.2^4=0.0016$, hence 

$$
\boxed{N_{\mathrm{approx}}=\left\lceil\frac{\ln(0.01)}{\ln(0.9984)}\right\rceil=2876}.
$$

 The quiz does not specify a confidence; the general formula is the source-supported answer. Sampling all putative matches independently also ignores the one-to-one matching constraint, so these iteration counts describe a simplified model.
````

````{solution-step} 5 — Check the finite sampling model
**Why:** Drawing distinct pairs from a small pool changes the clean-sample probability.

Because there are only 25 candidate pairs and each RANSAC *sample selects 4 distinct pairs*, the exact probability of four inliers in a uniform draw without replacement is smaller: 

$$
q_{\mathrm{exact}}=\frac{\binom54}{\binom{25}4}=\frac5{12650}\approx0.00039526.
$$

 If *each trial samples afresh* and we desire $p=0.99$, 

$$
\boxed{N_{\mathrm{finite}}=\left\lceil\frac{\ln(.01)}{\ln(1-5/12650)}\right\rceil=11649}.
$$

 This is an optional exact finite-population refinement; the standard lecture approximation uses $w^s$.
````

````{solution-step} 6 — Explain the regular-pentagon ambiguity
**Why:** More trials cannot distinguish equally supported symmetries.

For a regular pentagon, rotational/reflection symmetry makes the corner identities ambiguous: several match permutations may fit geometrically similar configurations. Without texture/orientation/other cues, a unique physical correspondence is less secure. Explain that good geometric fits need not identify the *intended* corner labeling.
For a genuinely regular pentagon, each of its five corners can serve as the first aligned corner. Each choice permits a clockwise or counterclockwise ordering, giving $5\times2=10$ equally supported alignments: five rotations and five reflections. If an external orientation constraint excludes reflections, five remain. The $20\%$ inlier rate refers to one selected alignment, not a union of different models. Equal side lengths alone do not imply these symmetries; the answer assumes a regular pentagon with equal angles too.
````

**Source check / assumptions:** The irregular-pentagon problem still requires nondegenerate 4-tuples (e.g. no three source points collinear). The exact without-replacement refinement above does not imply that *every* four-inlier subset yields a uniquely acceptable model under all degeneracies.


(quiz-source-10)=
## Spring 2019 Quiz 2 — FOV, calibration, homogeneous scaling

**Historical source:** `3dcvMid/olderquizzes/cs532s19_quiz2-2.pdf`.

(ex-lec03-calibration)=
(quiz-10-q1)=
### Problem 1

````{original-question}
A digital camera has image resolution $640\times480$ pixels and horizontal field of view $90^\circ$. Determine the focal length in pixels and draw a sketch.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Draw the half-angle triangle
**Why:** The symmetric horizontal field of view splits into two equal angles.

Take a horizontal cross-section through the optical axis. The full horizontal FOV is $90^\circ$, so each edge ray is $45^\circ$ from the optical axis. The image half-width is $W/2=320$ pixels.
````

````{solution-step} 2 — Rearrange the tangent relation
**Why:** Similar triangles connect pixel half-width and focal length.

In the pinhole triangle, $\tan(\theta/2)=(W/2)/f_x$. Rearrange: $f_x=(W/2)/\tan(\theta/2)$.
````

````{solution-step} 3 — Substitute the camera's numbers
**Why:** The requested focal length is in pixels.

Substitute $W=640$, $\theta=90^\circ$: 

$$
\boxed{f_x=\frac{320}{\tan45^\circ}=320\ \mathrm{px}}.
$$
````

```{figure} ../../images/lecture03/fov.*
:width: 70%
:alt: The half-width and half field of view determine pixel focal length.

The half-width and half field of view determine pixel focal length.
```


(quiz-10-q2)=
### Problem 2

````{original-question}
Write the intrinsic calibration matrix $K$ for the camera.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Write the intrinsic matrix
**Why:** Its entries separate focal lengths, skew and principal point.

Use standard intrinsic form 

$$
K=\begin{bmatrix}f_x&s&c_x\\0&f_y&c_y\\0&0&1\end{bmatrix}
$$

.
````

````{solution-step} 2 — State the missing assumptions
**Why:** Horizontal field of view alone does not determine every entry.

The horizontal FOV determines $f_x=320$ px only. To fill the other terms, *assume* square pixels ($f_y=f_x$), zero skew ($s=0$), and centered principal point ($(c_x,c_y)=(320,240)$).
````

````{solution-step} 3 — Fill in all matrix entries
**Why:** Only the stated extra assumptions justify a numerical K.

Under those common assumptions, 

$$
\boxed{K=\begin{bmatrix}320&0&320\\0&320&240\\0&0&1\end{bmatrix}}.
$$

 Without them, $f_y,s,c_x,c_y$ cannot all be inferred from the given horizontal FOV alone.
````


(ex-lec03-principal)=
(quiz-10-q3)=
### Problem 3(a–b)

````{original-question}
In $x=K[R\mid t]X$, give dimensions of every matrix/vector. If the right-hand side is multiplied by 2 to obtain $x'=2K[R\mid t]X$, how are $x'$ and $x$ related?
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — List matrix dimensions
**Why:** Adjacent matrix dimensions must agree in the projection product.

$K:3\times3$, $R:3\times3$, $t:3\times1$, $[R\mid t]:3\times4$, $X:4\times1$, $x:3\times1$; total projection matrix $P=K[R\mid t]$ is $3\times4$.
````

````{solution-step} 2 — Apply the common scale
**Why:** Homogeneous coordinates permit a nonzero common multiplier.

Homogeneous images are defined up to nonzero scale: $x'=(2q_1,2q_2,2q_3)^T$ vs $x=(q_1,q_2,q_3)^T$.
````

````{solution-step} 3 — Divide out that scale
**Why:** Ordinary image coordinates depend on ratios, so the location stays fixed.

Dehomogenize: $u'=2q_1/(2q_3)=q_1/q_3=u$ and $v'=2q_2/(2q_3)=v$. So $\boxed{x'\sim x}$: identical physical image points.
````


(quiz-10-q4)=
### Problem 4

````{original-question}
What are the 3D coordinates of the image principal point in the camera coordinate system?
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Locate the optical-axis intersection
**Why:** That intersection defines the principal point geometrically.

The principal point is the intersection of the camera optical axis with the image plane. In a virtual plane $z=f_{\mathrm{physical}}$, the optical axis is $X=Y=0$.
````

````{solution-step} 2 — Give its camera-frame position
**Why:** The virtual image plane is at physical focal depth.

Therefore its camera-frame position is $\boxed{(0,0,f_{\mathrm{physical}})}$. If the image-plane coordinate units are *chosen as pixel-equivalent units*, one may write $(0,0,320)$ using the computed focal length in pixels.
````

````{solution-step} 3 — Separate physical and pixel coordinates
**Why:** Pixel focal length does not reveal millimeters without pixel pitch.

Distinguish this 3D position from the image-array pixel coordinates $\boxed{(c_x,c_y)=(320,240)}$ under the centered-principal-point assumption. Physical $f$ in meters/mm is not determined by pixel focal length alone without pixel pitch.
````


(quiz-source-11)=
## Spring 2020 Quiz 3 — Duplicate camera model

**Historical source:** `3dcvMid/olderquizzes/cs532s20_quiz3.pdf`.

**Header note:** the supplied PDF contains mixed/overprinted year labels. The filename and separate retest entry are retained.

(quiz-11-q1)=
### Problem 1

````{original-question}
A camera is $640$ pixels wide by $480$ tall with horizontal FOV $90^\circ$. Find pixel focal length and sketch the rays.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Split the field of view
**Why:** The centered optical axis produces two 45-degree half angles.

Half-angle is $90^\circ/2=45^\circ$, and half-width is $640/2=320$ pixels. Draw the camera center, optical axis and the rays to the two horizontal ends of the image plane.
````

````{solution-step} 2 — Write the tangent equation
**Why:** The opposite side is the 320-pixel half-width.

$\tan45^\circ=(320\,\mathrm{px})/f_x$.
````

````{solution-step} 3 — Solve the focal length
**Why:** The tangent of 45 degrees is one.

Since $\tan45^\circ=1$, $\boxed{f_x=320\,\mathrm{px}}$. The half-angle/FOV diagram on the preceding quiz applies.
````

```{figure} ../../images/lecture03/fov.*
:width: 70%
:alt: The same half-angle construction applies to this separate retest.

The same half-angle construction applies to this separate retest.
```


(quiz-11-q2)=
### Problem 2

````{original-question}
Write the camera intrinsic matrix $K$.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Write the general matrix
**Why:** This shows which intrinsic parameters remain unknown.

Use 

$$
K=\begin{bmatrix}f_x&s&c_x\\0&f_y&c_y\\0&0&1\end{bmatrix}
$$

. The supplied FOV fixes only $f_x$.
````

````{solution-step} 2 — Declare the calibration assumptions
**Why:** Centering, square pixels and zero skew are additional information.

Explicitly assume square pixels $f_y=f_x=320$, zero skew $s=0$, and principal point at $(320,240)$.
````

````{solution-step} 3 — Substitute every entry
**Why:** The assumptions now determine a full numerical matrix.

Then 

$$
\boxed{K=\begin{bmatrix}320&0&320\\0&320&240\\0&0&1\end{bmatrix}}
$$

.
````


(quiz-11-q3)=
### Problem 3(a–b)

````{original-question}
Give dimensions in $x=K[R\mid t]X$ and explain what doubling the full homogeneous right-hand side changes.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Check every matrix shape
**Why:** The product maps four world entries to three image entries.

Identify $K\in\mathbb R^{3\times3}$, $R\in\mathbb R^{3\times3}$, $t\in\mathbb R^{3\times1}$, $[R\mid t]\in\mathbb R^{3\times4}$, $X\in\mathbb R^{4\times1}$, $x\in\mathbb R^{3\times1}$.
````

````{solution-step} 2 — Double the homogeneous column
**Why:** The question rescales all three components together.

For projected $x=(a,b,c)^T$, the doubled homogeneous vector $x'=2x=(2a,2b,2c)^T$.
````

````{solution-step} 3 — Dehomogenize both columns
**Why:** The common multiplier cancels from both ratios.

The dehomogenized coordinates are the same: $(a/c,b/c)=(2a/2c,2b/2c)$. Answer: $\boxed{\text{no image location change}}$.
````


(quiz-11-q4)=
### Problem 4

````{original-question}
Find the 3D coordinates of the principal point in the camera reference frame.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Write the optical-axis ray
**Why:** Its two lateral camera coordinates are zero.

Set the optical-axis ray to $\{(0,0,Z):Z>0\}$; intersect with virtual image plane $z=f_{\mathrm{physical}}$.
````

````{solution-step} 2 — Intersect with the virtual image plane
**Why:** The plane fixes the third coordinate to the focal length.

The point is $\boxed{(0,0,f_{\mathrm{physical}})}$ in camera length units; in pixel-normalized plane units $f=320$ gives the coordinate triple $(0,0,320)$.
````

````{solution-step} 3 — Distinguish the pixel-array answer
**Why:** Camera-frame positions and pixel indices are different quantities.

If the question instead asks for image-array pixel coordinates, use $(c_x,c_y)=(320,240)$ under the stated centering assumption.
````


(quiz-source-14)=
## Spring 2020 Quiz 2 — Pinhole ray and cross product

**Historical source:** `3dcvMid/olderquizzes/cs532s20_quiz2.pdf`.

(ex-lec03-ray)=
(quiz-14-q1)=
### Problem 1

````{original-question}
Let $A=(X,Y,Z)$ be a camera-frame 3D point. Its viewing ray passes through image point $a$ on the image plane. Given $f=Z/10$, determine the 3D camera-frame coordinates of $a$; sketch.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Use the common viewing ray
**Why:** A pinhole camera center, image-plane point and scene point are collinear.

For a virtual pinhole image plane at $z=f$, the 3D point and pixel lie on the same ray from the origin. Similar triangles give $x_a/f=X/Z$ and $y_a/f=Y/Z$.
````

````{solution-step} 2 — Write all three coordinates
**Why:** The image point lies on the plane with third coordinate f.

Thus $a=(fX/Z,fY/Z,f)$.
````

````{solution-step} 3 — Substitute the supplied focal length
**Why:** The common scale becomes one tenth.

Substitute $f=Z/10$, assuming $Z\ne0$: 

$$
\boxed{a=(X/10,Y/10,Z/10)=A/10}.
$$
````

````{solution-step} 4 — Sketch the geometry
**Why:** The drawing should show the same ray through both points.

Draw origin $O$, the point $A$, the intermediate image plane $z=f$, and $a$ on the segment of ray $OA$ (for $Z>0$ and $f=Z/10$). The vectors $Oa$ and $OA$ point in the same direction.
````

```{figure} ../../images/lecture01/pinhole.*
:width: 70%
:alt: Pinhole viewing-ray sketch, shown as a side view. In this quiz the image-plane point is one tenth of the scene vector; the schematic is not drawn to that scale.

Pinhole viewing-ray sketch, shown as a side view. In this quiz the image-plane point is one tenth of the scene vector; the schematic is not drawn to that scale.
```


(quiz-14-q2)=
### Problem 2

````{original-question}
Develop the expression for $A\times a$.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Insert the two vectors
**Why:** The preceding part fixes every coordinate of the image-plane point.

Set $A=(X,Y,Z)^T$ and $a=(X/10,Y/10,Z/10)^T$.
````

````{solution-step} 2 — Set up the cross product
**Why:** Its determinant representation organizes the three component calculations.

Use the cross-product determinant: 

$$
A\times a=\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\X&Y&Z\\X/10&Y/10&Z/10\end{vmatrix}.
$$
````

````{solution-step} 3 — Expand each component
**Why:** Equal scalar products cancel pairwise.

Expand components: $(YZ/10-ZY/10,\ ZX/10-XZ/10,\ XY/10-YX/10)$.
````

````{solution-step} 4 — Interpret the zero vector
**Why:** Parallel Euclidean 3D directions have zero cross product.

Every component is zero, so $\boxed{A\times a=(0,0,0)^T}$. Geometrically, collinear vectors have zero cross product.
````


(quiz-source-15)=
## Older Quiz 9 — Pinhole ray intersects a 3D plane

**Historical source:** `3dcvMid/olderquizzes/cs532f15_quiz9.pdf`.

**Header note:** this filename contains “2015”; the PDF is printed Spring 2019.

(quiz-15-q1)=
### Problem 1

````{original-question}
A 3D plane has homogeneous parameters $\pi=(A,B,C,D)^T$, i.e. $AX+BY+CZ+D=0$. A pinhole camera has center at the 3D origin, orientation $I$, focal length $f$, and observes pixel image-plane coordinates $(x',y')$. Find the 3D depth of the intersection of the viewing ray with the plane. Draw a sketch.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Parameterize the viewing ray
**Why:** Every candidate 3D point must lie along that ray.

The ray begins at camera origin and passes through $(x',y',f)$ on the virtual image plane. Its parametric form is $r(\lambda)=\lambda(x',y',f)=(\lambda x',\lambda y',\lambda f)$.
````

````{solution-step} 2 — Express X and Y using depth
**Why:** Pinhole ratios reduce the unknown point to one unknown Z.

Using pinhole geometry, $x'/f=X/Z$, $y'/f=Y/Z$, hence $X=(x'/f)Z$ and $Y=(y'/f)Z$.
````

````{solution-step} 3 — Substitute into the plane
**Why:** The requested intersection must satisfy the plane equation.

Substitute into plane equation: 

$$
A\frac{x'Z}{f}+B\frac{y'Z}{f}+CZ+D=0.
$$
````

````{solution-step} 4 — Collect the depth terms
**Why:** Factoring Z isolates the quantity we want.

Factor out $Z$: $Z(Ax'/f+By'/f+C)=-D$.
````

````{solution-step} 5 — Solve the axial depth
**Why:** Division is valid only when the ray-plane denominator is nonzero.

Solve the optical-axis depth: 

$$
\boxed{Z=-\frac{Df}{Ax'+By'+Cf}}.
$$
````

````{solution-step} 6 — Recover the full point
**Why:** Once depth is known the ray determines both lateral coordinates.

Recover the complete intersection point, if requested: 

$$
\boxed{X=\frac{x'Z}{f},\quad Y=\frac{y'Z}{f},\quad Z=-\frac{Df}{Ax'+By'+Cf}}.
$$

 Equivalently $\lambda=-D/(Ax'+By'+Cf)$ and $r(\lambda)$ gives all three coordinates.
````

````{solution-step} 7 — Check exceptional cases
**Why:** Parallel, contained and behind-camera cases need different interpretations.

Check exceptions: if $Ax'+By'+Cf=0$ and $D\ne0$, the viewing ray is parallel to the plane (no finite intersection). If both equal zero, the entire ray lies in the plane (no unique depth). A visible front-of-camera intersection normally requires $Z>0$.
````

**Source check / assumptions:** The formula gives $Z$ (depth along optical axis), not necessarily Euclidean camera-to-point range $\sqrt{X^2+Y^2+Z^2}$.

```{figure} ../../images/lecture03/ray-plane.*
:width: 70%
:alt: A ray–plane illustration. Its numerical labels belong to the separate Example 3.4 companion in the teaching section.

A ray–plane illustration. Its numerical labels belong to the separate Example 3.4 companion in the teaching section.
```


(quiz-source-a1)=
## A1. Homography, DLT and SVD (L3, slides 34–45)

**Original practice from the supplied booklet; not a historical quiz question.**

(quiz-a1-q1)=
### Illustrative problem

````{original-question}
Find the homography mapping $(0,0)\mapsto(0,0)$, $(1,0)\mapsto(1/2,0)$, $(0,1)\mapsto(0,1)$, $(1,1)\mapsto(1/2,1/2)$. Explain where SVD would enter for noisy pairs.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Write the projective mapping
**Why:** Homogeneous scaling makes the image coordinates ratios.

Write the unknown homography $H=[h_{ij}]$, with $h_{33}=1$ for this convenient example. Use $u=(h_{11}x+h_{12}y+h_{13})/(h_{31}x+h_{32}y+1)$ and $v=(h_{21}x+h_{22}y+h_{23})/(h_{31}x+h_{32}y+1)$.
````

````{solution-step} 2 — Use the origin match
**Why:** It isolates the translation-like numerator entries.

The origin maps to itself, so at $(x,y)=(0,0)$: $h_{13}=h_{23}=0$.
````

````{solution-step} 3 — Use the horizontal match
**Why:** Its nonzero input coordinate constrains one denominator term.

At $(1,0)\to(1/2,0)$: $h_{11}/(h_{31}+1)=1/2$ and $h_{21}/(h_{31}+1)=0$. Therefore $2h_{11}=h_{31}+1$ and $h_{21}=0$.
````

````{solution-step} 4 — Use the vertical match
**Why:** This constrains the remaining numerator and denominator entries.

At $(0,1)\to(0,1)$: $h_{12}/(h_{32}+1)=0$ and $h_{22}/(h_{32}+1)=1$. Thus $h_{12}=0$ and $h_{22}=h_{32}+1$.
````

````{solution-step} 5 — Use the final corner
**Why:** Combining previous constraints determines the projective denominator.

At $(1,1)\to(1/2,1/2)$: $h_{11}/(h_{31}+h_{32}+1)=1/2$ and $h_{22}/(h_{31}+h_{32}+1)=1/2$. Compare with step 3 to get $h_{32}=0$, hence $h_{22}=1$. Then $h_{31}+1=2$, so $h_{31}=h_{11}=1$.
````

````{solution-step} 6 — Assemble and project a check point
**Why:** A held-out point tests the resulting matrix.

Assemble and verify: 

$$
\boxed{H=\begin{bmatrix}1&0&0\\0&1&0\\1&0&1\end{bmatrix}}.
$$

 For $(x,y)=(2,1)$, $H(2,1,1)^T=(2,1,3)^T$, so the new image coordinates are $(2/3,1/3)$.
````

````{solution-step} 7 — Build the general DLT equations
**Why:** Each correspondence supplies two linear constraints on nine homogeneous entries.

In general, each match $(x,y)\to(u,v)$ yields two rows of $Ah=0$: 

$$
A_i=\begin{bmatrix}x&y&1&0&0&0&-ux&-uy&-u\\0&0&0&x&y&1&-vx&-vy&-v\end{bmatrix}.
$$

 With more than four noisy pairs, choose the *last right singular vector* of $A=U\Sigma V^T$ (smallest singular value) and reshape it to $H$. Coordinate normalization before DLT improves conditioning: $H=T'^{-1}\widetilde HT$.
````

````{solution-step} 8 — Show the complete numerical system
**Why:** The actual eight rows expose the nullspace that SVD must recover.

For these four actual matches, the full $8\times9$ homogeneous DLT system is $Ah=0$, where

$$
A=\begin{pmatrix}
0&0&1&0&0&0&0&0&0\\0&0&0&0&0&1&0&0&0\\
1&0&1&0&0&0&-1/2&0&-1/2\\0&0&0&1&0&1&0&0&0\\
0&1&1&0&0&0&0&0&0\\0&0&0&0&1&1&0&-1&-1\\
1&1&1&0&0&0&-1/2&-1/2&-1/2\\0&0&0&1&1&1&-1/2&-1/2&-1/2
\end{pmatrix},
$$

$$
h=\begin{pmatrix}h_{11}&h_{12}&h_{13}&h_{21}&h_{22}&h_{23}&h_{31}&h_{32}&h_{33}\end{pmatrix}^T.
$$

The solution $h=(1,0,0,0,1,0,1,0,1)^T$ makes each row zero. For four pairs, use a full right-singular basis: the null vector is the ninth right singular vector of this wide matrix, not the last vector of a reduced eight-vector basis.
````

**Source check / assumptions:** Fixing $h_{33}=1$ is only valid if the actual $h_{33}$ is nonzero; the homogeneous SVD formulation avoids relying on that choice.
