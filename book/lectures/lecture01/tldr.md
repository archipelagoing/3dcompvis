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

1. **Depth:** why can one image pixel correspond to many 3D points?
2. **Coordinates:** what ordinary point does $(6,9,3)^T$ represent? Can you similarly normalize $(1,0,0)^T$?
3. **Intersection:** find the homogeneous intersection of $x=2$ and $y=3$, using line vectors $(1,0,-2)^T$ and $(0,1,-3)^T$.
4. **Pivot:** rotate $(3,1)$ by $+90^\circ$ about $(2,1)$ in Cartesian axes with $y$ upward. Where does it land?
5. **Plane:** find a normal and plane equation through $(0,0,0)$, $(1,0,0)$, and $(0,1,0)$. When would the three-point method fail?
6. **Rotation:** a matrix satisfies $R^TR=I$ but has determinant $-1$. Is it a proper rotation?
7. **Frames:** two object-to-camera poses have identity rotations and translations $t_1=(1,1,4)^T$, $t_2=(-1,1,4)^T$. What is the translation from camera 2 to camera 1?
8. **Camera:** use zero skew, $f_x=f_y=100$ pixels, and principal point $(0,0)$. Project camera-coordinate point $(2,1,5)^T$. Then move the camera one unit forward without rotating it while the point stays fixed. What is the new pixel?

## Answers

```{admonition} Show answers and short explanations
:class: dropdown

1. **A pixel identifies a ray, not a depth.** Different positive depths along that ray produce the same image point.
2. **$(2,3)$.** Divide the first two entries by three. $(1,0,0)^T$ is an ideal point; dividing by its last coordinate is invalid.
3. **$(2,3,1)^T$.** The cross product gives this vector. Substitution into both line equations gives zero.
4. **$(2,2)$.** The offset from the pivot is $(1,0)$. Rotate it to $(0,1)$, then add the pivot back.
5. **$n=(0,0,1)^T$, so $z=0$.** Cross the two edge vectors. Its negative is equally valid for the unoriented plane. Collinear or repeated inputs cannot determine a unique plane.
6. **No.** It is orthogonal but includes a reflection. A proper rotation needs determinant $+1$.
7. **$(2,0,0)^T$.** With both rotations equal to identity, the relative translation is $t_1-t_2$. Check: camera 2's object coordinates plus this translation equal camera 1's.
8. **Initially $(40,20)$ pixels; afterward $(50,25)$.** First compute $(100\cdot2/5,100\cdot1/5)$. Moving the camera forward reduces depth from five to four, so the image moves away from the principal point.
```
