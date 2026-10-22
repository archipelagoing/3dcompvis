(lec01-tldr)=
# TLDR

**Lecture 1 in one sentence:** images lose depth, so reconstructing a scene requires geometry, coordinate frames, and careful use of multiple measurements.

## The big picture

The reconstruction pipeline is **match features → estimate cameras and 3D points → estimate dense depth → build a representation**. A convincing picture is not proof of correct geometry: lighting, occlusion, repeated patterns, and noise can mislead us.

## The rules worth remembering

1. **Homogeneous coordinates ignore overall scale.** $(2,4,2)^T$ and $(1,2,1)^T$ represent the same point. Divide by the last coordinate to get ordinary coordinates only when it is nonzero. A zero last coordinate means an ideal point; the all-zero vector is invalid. A scene direction can project to a finite image vanishing point. See {ref}`lec01-projective`.

2. **Dot products test incidence; cross products construct geometry.** A point lies on a line when $\ell^Tx=0$. Join two distinct image points with $x\times y$; intersect two distinct image lines with $\ell_1\times\ell_2$. Parallel lines meet at an ideal point. See {eq}`eq-lec01-cross`.

3. **Choose the transformation you actually need.** Rigid motion preserves distances and angles; similarity adds uniform scale; affine maps preserve parallelism; projective maps preserve incidence but can change parallelism. Points transform with $H$; line and plane coefficients use its inverse transpose. To rotate about a pivot, **subtract the pivot → rotate → add it back**. See {ref}`lec01-transformations`.

4. **Three noncollinear points determine a plane.** Use $n=(B-A)\times(D-A)$ and $d=-n^TA$ in $n^Tp+d=0$ for a point $p$. Collinear points give no unique plane. A unit normal gives orientation; its sign depends on your chosen inward/outward convention. Under a rigid rotation, normals rotate without translation. See {ref}`lec01-planes`.

5. **A rotation is more than a square matrix.** A proper rotation satisfies $R^TR=I$ and $\det R=+1$, so $R^{-1}=R^T$. Rotation order matters. Matrices, ordered angles, axis–angle, and unit quaternions describe rotations, but their conventions must agree. Here active quaternion rotation is $qPq^{-1}$. See {ref}`lec01-rotations`.

6. **Label every coordinate frame.** For $p_B=Rp_A+t$, undo the motion with $p_A=R^T(p_B-t)$. In a matrix product the rightmost transform acts first. To go from camera 2 through a shared object to camera 1, use $T_{C_1\leftarrow O}(T_{C_2\leftarrow O})^{-1}$. See {ref}`lec01-frames`.

7. **Projection divides by depth.** In camera coordinates, normalized image coordinates are $(X_c/Z_c,Y_c/Z_c)$. Intrinsics convert these to pixels; extrinsics convert world coordinates to camera coordinates. Together, $x\sim K[R\mid t]X_w$. Require positive depth for a point in front, then check image bounds separately. See {ref}`lec01-cameras`.

8. **Camera motion changes the point's camera coordinates.** Moving the camera forward by $\Delta$ changes a stationary point's depth to $Z_c-\Delta$. Off-axis points move farther from the principal point while they remain in front. Moving the object farther away does the opposite. Backprojection needs calibration and a specified depth convention: axial depth and distance along the ray are different. See {ref}`Example 1.15 <ex-lec01-camera-motion>`.

**Also recognize:** a nullspace solves homogeneous incidence equations; a finite Plücker line stores direction $d$ and moment $p\times d$. The [formula checklist](review.md) links to these less frequently used constructions and their conditions.

**Before calculating:** name the frames, check units, choose the formula, and test whether the answer makes geometric sense.

## Short quiz

Try these without looking at the answers. These are original practice questions based on Lecture 1; the assigned course quizzes are worked through in {ref}`lec01-frames`.

Each question has its own complete worked answer below. Open it after trying the problem; all answers are visible in print.

(lec01-tldr-q1)=
### Question 1

````{original-question} Original practice question
**Depth:** why can one image pixel correspond to many 3D points?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Write a camera ray
**Why:** A pixel fixes a direction but leaves its distance unknown.

For a calibrated pixel $p=(u,v,1)^T$, let $r=K^{-1}p$. Points on its ray have $X_C=Zr$ when $r_3=1$ and depth is axial.
````

````{solution-step} 2 — Check two depths
**Why:** Perspective division cancels the common ray scale.

For normalized direction $r=(a,b,1)^T$, both points $(a,b,1)^T$ and $(2a,2b,2)^T$ project to $(a,b)$. Thus one pixel can represent many positive depths.
````

`````

(lec01-tldr-q2)=
### Question 2

````{original-question} Original practice question
**Coordinates:** what ordinary point does $(6,9,3)^T$ represent? Can you similarly normalize $(1,0,0)^T$?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Normalize the finite point
**Why:** Ordinary coordinates are ratios to the final homogeneous coordinate.

$$
\begin{pmatrix}6\\9\\3\end{pmatrix}/3=\begin{pmatrix}2\\3\\1\end{pmatrix},\qquad (u,v)=(2,3).
$$
````

````{solution-step} 2 — Check the other denominator
**Why:** A zero final coordinate cannot be divided out.

The nonzero vector $(1,0,0)^T$ is an ideal point. It has no finite ordinary coordinate pair.
````

`````

(lec01-tldr-q3)=
### Question 3

````{original-question} Original practice question
**Intersection:** find the homogeneous intersection of $x=2$ and $y=3$, using line vectors $(1,0,-2)^T$ and $(0,1,-3)^T$.
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Expand the line cross product
**Why:** The cross product intersects two homogeneous image lines.

$$
\begin{pmatrix}1\\0\\-2\end{pmatrix}\times\begin{pmatrix}0\\1\\-3\end{pmatrix}=\begin{pmatrix}0(-3)-(-2)(1)\\(-2)(0)-1(-3)\\1(1)-0(0)\end{pmatrix}=\begin{pmatrix}2\\3\\1\end{pmatrix}.
$$
````

````{solution-step} 2 — Verify both incidences
**Why:** The answer must lie on both original lines.

$$
\begin{pmatrix}1&0&-2\end{pmatrix}\begin{pmatrix}2\\3\\1\end{pmatrix}=2-2=0,\qquad \begin{pmatrix}0&1&-3\end{pmatrix}\begin{pmatrix}2\\3\\1\end{pmatrix}=3-3=0.
$$

 The ordinary intersection is $(2,3)$.
````

`````

(lec01-tldr-q4)=
### Question 4

````{original-question} Original practice question
**Pivot:** rotate $(3,1)$ by $+90^\circ$ about $(2,1)$ in Cartesian axes with $y$ upward. Where does it land?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Rotate the offset
**Why:** Rotating about a pivot requires coordinates relative to that pivot.

$$
p-c=\begin{pmatrix}3\\1\end{pmatrix}-\begin{pmatrix}2\\1\end{pmatrix}=\begin{pmatrix}1\\0\end{pmatrix},\qquad R(p-c)=\begin{pmatrix}0&-1\\1&0\end{pmatrix}\begin{pmatrix}1\\0\end{pmatrix}=\begin{pmatrix}0\\1\end{pmatrix}.
$$
````

````{solution-step} 2 — Add the pivot back
**Why:** The final answer must use the original coordinate frame.

$$
p'=\begin{pmatrix}2\\1\end{pmatrix}+\begin{pmatrix}0\\1\end{pmatrix}=\begin{pmatrix}2\\2\end{pmatrix}.
$$
````

`````

(lec01-tldr-q5)=
### Question 5

````{original-question} Original practice question
**Plane:** find a normal and plane equation through $(0,0,0)$, $(1,0,0)$, and $(0,1,0)$. When would the three-point method fail?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Cross the two edges
**Why:** Their cross product is perpendicular to the desired plane.

$$
n=\begin{pmatrix}1\\0\\0\end{pmatrix}\times\begin{pmatrix}0\\1\\0\end{pmatrix}=\begin{pmatrix}0\\0\\1\end{pmatrix}.
$$
````

````{solution-step} 2 — Set the plane offset and check uniqueness
**Why:** The given origin lies on the plane, fixing its offset to zero.

$$
d=-n^T\begin{pmatrix}0\\0\\0\end{pmatrix}=0,\qquad n^T\begin{pmatrix}X\\Y\\Z\end{pmatrix}+d=Z=0.
$$

 Collinear or repeated inputs give a zero edge cross product and no unique plane. Negating the normal describes this same unoriented plane.
````

`````

(lec01-tldr-q6)=
### Question 6

````{original-question} Original practice question
**Rotation:** a matrix satisfies $R^TR=I$ but has determinant $-1$. Is it a proper rotation?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Check orthogonality
**Why:** The first condition preserves lengths and angles.

$R^TR=I$ makes $R$ orthogonal. Orthogonal matrices can have determinant $+1$ or $-1$.
````

````{solution-step} 2 — Check orientation
**Why:** A proper rotation must preserve handedness too.

The supplied $\det R=-1$ fails the condition $\det R=+1$. Therefore this is not a proper rotation; it includes an orientation reversal.
````

`````

(lec01-tldr-q7)=
### Question 7

````{original-question} Original practice question
**Frames:** two object-to-camera poses have identity rotations and translations $t_1=(1,1,4)^T$, $t_2=(-1,1,4)^T$. What is the translation from camera 2 to camera 1?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Subtract the translations
**Why:** Both rotations are identity, so the general relative-pose formula simplifies.

$$
t_{12}=t_1-t_2=\begin{pmatrix}1\\1\\4\end{pmatrix}-\begin{pmatrix}-1\\1\\4\end{pmatrix}=\begin{pmatrix}2\\0\\0\end{pmatrix}.
$$
````

````{solution-step} 2 — Test the observed origin
**Why:** The translation should map camera 2's object coordinates into camera 1's.

$$
\begin{pmatrix}-1\\1\\4\end{pmatrix}+\begin{pmatrix}2\\0\\0\end{pmatrix}=\begin{pmatrix}1\\1\\4\end{pmatrix}=t_1.
$$
````

`````

(lec01-tldr-q8)=
### Question 8

````{original-question} Original practice question
**Camera:** use zero skew, $f_x=f_y=100$ pixels, and principal point $(0,0)$. Project camera-coordinate point $(2,1,5)^T$. Then move the camera one unit forward without rotating it while the point stays fixed. What is the new pixel?
````

`````{worked-solution} Show the fully worked answer

````{solution-step} 1 — Project the initial point
**Why:** Intrinsics multiply the camera point before division by depth.

$$
q=\begin{pmatrix}100&0&0\\0&100&0\\0&0&1\end{pmatrix}\begin{pmatrix}2\\1\\5\end{pmatrix}=\begin{pmatrix}200\\100\\5\end{pmatrix},\qquad (u,v)=(200/5,100/5)=(40,20).
$$
````

````{solution-step} 2 — Update camera coordinates and reproject
**Why:** A forward camera motion reduces a stationary point's camera depth.

$$
X_C'=\begin{pmatrix}2\\1\\5\end{pmatrix}-\begin{pmatrix}0\\0\\1\end{pmatrix}=\begin{pmatrix}2\\1\\4\end{pmatrix},\quad q'=\begin{pmatrix}100&0&0\\0&100&0\\0&0&1\end{pmatrix}\begin{pmatrix}2\\1\\4\end{pmatrix}=\begin{pmatrix}200\\100\\4\end{pmatrix}.
$$

 Divide by four: the new pixel is $(50,25)$.
````

`````
