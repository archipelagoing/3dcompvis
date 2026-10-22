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

1. A centered pinhole image is 800 pixels wide with 90° horizontal FOV. What is $f_x$? Does that alone determine $f_y$?
2. If $f_x=400$ pixels and pixel pitch is $0.004\,\mathrm{mm/pixel}$, where is the principal point on the positive virtual image plane in camera-frame millimeters?
3. For a scene vector $(3,2,30)^T$ and $f=3$, what is its image-plane 3D intersection? What is the cross product of the two vectors?
4. A ray is $P=Z(0.5,0,1)^T$ and the known plane is $X+Z=12$. Find $Z$ and $P$.
5. What happens if a ray has $\gamma=0$ for a plane with $D\ne0$?
6. For Example 3.5's matrix, where does source point $(0.5,0.5)$ go? Is it the destination vertex average?
7. If one independent attempt succeeds with probability $1/4$, what is the chance of at least one success in three attempts?
8. A regular pentagon gives several equally supported alignments. Will increasing RANSAC's trial count identify the intended alignment? Name evidence that could.

## Answers

```{admonition} Show answers and short explanations
:class: dropdown

1. **400 pixels.** Use $800/(2\tan45^\circ)$. Vertical focal length needs an additional pixel-shape or calibration assumption.
2. **$(0,0,1.6)\,\mathrm{mm}$.** Multiply $400$ by $0.004$; pixel principal-point coordinates are a different description.
3. **$(0.3,0.2,3)^T$; zero cross product.** The intersection is one tenth of the scene vector.
4. **$Z=8$, $P=(4,0,8)^T$.** Substitute into the plane: $0.5Z+Z=12$. The depth is positive.
5. **No finite intersection.** The ray is parallel to a plane that does not contain the camera center.
6. **$(4/3,2/3)$.** Divide $(2,1,3/2)^T$ by its last coordinate. It differs from the vertex average $(1,3/4)$.
7. **$1-(3/4)^3=37/64\approx57.81\%$.** Subtract the probability of three failures from one.
8. **No.** A distinctive visible mark, a labeled corner, or other asymmetric scene evidence can distinguish models that have identical corner support.
```
