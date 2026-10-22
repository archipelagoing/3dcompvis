(lec01-frames)=
# Reference frames and two worked quiz problems

A camera pose answers a question only after its coordinate frames are named. “The translation is $(2,0,0)$” is incomplete: from which frame to which other frame? This section makes the direction explicit, then uses it to solve the lecture's most relevant quiz problems.

**Lecture source:** `wk1_2_cs532s26_IntroToGeometry.pdf`, PDF pages 101–103, printed slides 102–104; supporting plane/rotation material on PDF pages 82–89.

## Rigid motion is rotation plus translation

A **{term}`rigid transformation <Rigid transformation>`** preserves distances and angles. With column vectors, rotate a position into the target axes, then add the source origin's position expressed in the target frame.

````{formula-box} Formula — rigid coordinate transform and inverse
```{math}
:label: eq-lec01-rigid3
\begin{aligned}
p_B&=R_{B\leftarrow A}p_A+t_{B\leftarrow A},\\
T_{B\leftarrow A}&=\begin{pmatrix}R&t\\0^T&1\end{pmatrix},\qquad
T_{A\leftarrow B}=\begin{pmatrix}R^T&-R^Tt\\0^T&1\end{pmatrix}.
\end{aligned}
```

$p_A,p_B,t$ are $3\times1$ and use one length unit; $R$ is a proper $3\times3$ rotation; $T$ is $4\times4$. The inverse follows by subtracting $t$ from $p_B$ and multiplying by $R^T$.

**Conditions:** exact rigid transform. The inverse translation is $-R^Tt$, not generally $-t$. Directions and normals under a rigid transform rotate without translation; positions translate as well.
````

```{application} How to use it — move a coordinate description
1. Label the source and target frames on the matrix.
2. Rotate the source-frame position and add the translation in target coordinates.
3. To reverse, apply the inverse with rotated negative translation.
4. Check that a source-frame origin maps to $t$ and that forward/inverse composition is identity.

See {ref}`Example 1.10 <ex-lec01-relative-pose>`.
```

````{formula-box} Formula — compose compatible frame transforms
```{math}
:label: eq-lec01-compose
T_{C\leftarrow A}=T_{C\leftarrow B}T_{B\leftarrow A},\qquad
R_{CA}=R_{CB}R_{BA},\quad t_{CA}=R_{CB}t_{BA}+t_{CB}.
```

All $T$ matrices are $4\times4$; all $R$ blocks are $3\times3$ and translations $3\times1$. Intermediate frame $B$ matches between adjacent factors. The subscripts without arrows abbreviate the same target/source ordering.

**Conditions:** frames, time, object convention, and length units must agree. A product of numerically compatible matrices can still be geometrically meaningless if the frame path does not connect.
````

```{application} How to use it — follow the frame path
1. Write the desired coordinate journey, for example $A\to B\to C$.
2. Place the first operation on the right.
3. Invert any supplied transform whose direction opposes the journey.
4. Multiply and test the result on a known point.

See {ref}`Example 1.10 <ex-lec01-relative-pose>`.
```

## Quiz: recover camera pose through a shared object

**Assigned source:** Fall 2025 Quiz 1, questions 3–4, `cs532f25_quiz_1_solution.pdf`, PDF page 2. Its printed title is “RANSAC and Two-view Geometry.” The probability questions 1–2 belong beside RANSAC in Lecture 3; the geometry questions belong here according to `quizByLec.md`.

Each static camera estimates the object's pose in its own coordinates. Assume both estimates describe the same rigid object frame at the same instant and in the same physical units.

```{figure} ../../images/lecture01/shared-object.*
:name: fig-lec01-shared-object
:width: 85%
:alt: A coordinate-transform path goes from camera two through the object frame to camera one.

Follow the transform directions through the shared object. This is a frame graph, not a drawing of physical camera positions. Original diagram for Fall 2025 Quiz 1, question 3.
```

(ex-lec01-relative-pose)=
````{worked-example} Worked example 1.10 — Fall 2025 Quiz 1, question 3
**Question:** can a simultaneous pair of object-pose estimates determine the relative camera pose?

**Answer:** yes, under the shared-frame, time, and scale assumptions above.

1. The supplied maps are $T_{C_1\leftarrow O}$ and $T_{C_2\leftarrow O}$.
2. To express a camera-2 point in camera 1, first go from $C_2$ back to $O$ by inverting the second map.
3. Then go from $O$ to $C_1$ with the first map.

```{math}
:label: eq-lec01-relative-pose
T_{C_1\leftarrow C_2}
=T_{C_1\leftarrow O}\bigl(T_{C_2\leftarrow O}\bigr)^{-1}.
```

Writing each supplied pose as $(R_i,t_i)$ gives $R_{12}=R_1R_2^T$ and $t_{12}=t_1-R_1R_2^Tt_2$. These are the composition and inverse rules above, not new assumptions.

**Numerical illustration added here:** take $R_1=R_2=I$, $t_1=(1,1,4)^T$, and $t_2=(-1,1,4)^T$. Then $R_{12}=I$ and $t_{12}=(2,0,0)^T$. The object origin in camera 2 is $t_2$; transforming it gives $t_2+t_{12}=t_1$, which checks the direction.

If each pose estimate has an independent unknown scale, or uses a different ambiguous object orientation, this simple metric composition is not justified.
````

The boxed general composition formula is the canonical rule; the displayed quiz equation is its concrete specialization. Its $4\times4$ inputs and output have the same frame/unit conditions. Use the graph as the algorithm: invert the camera-2 object pose, multiply on the left by the camera-1 object pose, and verify on the object origin.

(ex-lec01-object-plane)=
```{worked-example} Worked example 1.11 — Fall 2025 Quiz 1, question 4
**Question:** can we estimate the plane through the object and both cameras?

Interpret “the object” as the origin of its estimated object frame, and choose camera 1 as the working coordinate frame.

1. Its center is $C_1=(0,0,0)^T$.
2. Camera 2's center is $C_2=t_{12}$. This works because the origin of frame $C_2$ maps to the translation column of $T_{C_1\leftarrow C_2}$.
3. The object origin is $O=t_1$.
4. Form $n=(O-C_1)\times(C_2-C_1)$, then $d=-n^TC_1=0$.

For the numerical illustration above, $n=(1,1,4)\times(2,0,0)=(0,8,-2)\sim(0,4,-1)$. The plane is $4y-z=0$. It contains both camera centers and the object origin, since each gives zero on substitution.

**Qualification to the supplied solution:** this gives a unique plane only if the three positions are noncollinear. If the object origin lies on the camera baseline, the cross product is zero and there is no unique plane. An extended object is not necessarily wholly contained in this plane.
```

## Quiz: tetrahedron face normals and a rotated object

**Assigned source:** Fall 2017 Quiz 9, problem 2(a–b), `cs532_f17_quiz9.pdf`, PDF page 2. This is supplementary practice for Lecture 1; it is not a high-probability exam prediction. Its depth-map problem 1 is previewed in the camera section and retained for deeper treatment in Lectures 3–4.

```{figure} ../../images/lecture01/tetrahedron.*
:name: fig-lec01-tetrahedron
:width: 70%
:alt: Tetrahedron with vertices 1,1,0; 1,2,0; 1,1,1; and 2,1,0.

The quiz tetrahedron. Coordinates are shown relative to the corner $v_1$ for drawing convenience; vertex labels give the actual quiz coordinates. Original schematic, not a metric perspective rendering.
```

(ex-lec01-tetrahedron)=
```{worked-example} Worked example 1.12 — Fall 2017 Quiz 9, problem 2(a)
The vertices are $v_1=(1,1,0)$, $v_2=(1,2,0)$, $v_3=(1,1,1)$, and $v_4=(2,1,0)$.

We choose **outward unit normals**. The problem does not specify orientation or normalization; declare them rather than silently mixing signed answers.

1. For face $123$, $(v_2-v_1)\times(v_3-v_1)=(0,1,0)\times(0,0,1)=(1,0,0)$. This points toward the opposite vertex $v_4$, so flip it: $n_{123}=(-1,0,0)$.
2. Face $124$ lies on $z=0$, with the interior at positive $z$. Its outward normal is $(0,0,-1)$.
3. Face $134$ lies on $y=1$, with the interior at larger $y$. Its outward normal is $(0,-1,0)$.
4. For face $234$, use $v_3-v_2=(0,-1,1)$ and $v_4-v_2=(1,-1,0)$. Their cross product is $(1,1,1)$. The opposite vertex lies on its negative side, so it already points outward. Normalize to $(1,1,1)/\sqrt3$.

A general orientation check is $n^T(v_{\rm opposite}-v_{\rm face})<0$ for an outward normal. Each normal must also have zero dot product with its face's two edge directions.
```

(ex-lec01-rotated-normals)=
```{worked-example} Worked example 1.13 — Fall 2017 Quiz 9, problem 2(b)
Rotate the object actively by $+90^\circ$ about the global $z$ axis. Because this is a rigid rotation, normals rotate with $R_z$ and do not translate.

The coordinate rule is $(x,y,z)\mapsto(-y,x,z)$. Applying it to every vertex gives $(-1,1,0)$, $(-2,1,0)$, $(-1,1,1)$, and $(-1,2,0)$.

| Face | Original outward unit normal | Rotated outward unit normal |
| --- | --- | --- |
| 123 | $(-1,0,0)$ | $(0,-1,0)$ |
| 124 | $(0,0,-1)$ | $(0,0,-1)$ |
| 134 | $(0,-1,0)$ | $(1,0,0)$ |
| 234 | $(1,1,1)/\sqrt3$ | $(-1,1,1)/\sqrt3$ |

**Check:** recomputing each cross product from the rotated vertices gives the same oriented normal after normalization. Unit lengths and outward orientation are preserved. For a general affine deformation, use an inverse transpose for normals instead; multiplying by the forward matrix is special to rigid rotations (and needs normalization under uniform scale).
```

## Where rigid transformations sit in the 3D hierarchy

The last geometry slide, PDF page 103, extends the 2D hierarchy to 3D. The homogeneous forms in {eq}`eq-lec01-hierarchy` extend by making $R,A$ $3\times3$ and $t,v$ $3\times1$.

| Family | 3D continuous DOF | Important preserved properties |
| --- | --- | --- |
| Proper rigid/Euclidean | 6 | Distances, angles, volume |
| Similarity | 7 | Angles and ratios of lengths |
| Affine | 12 | Parallelism, collinear ratios, volume ratios |
| Projective | 15 | Incidence and tangency where defined |

A rigid motion has three rotation and three translation parameters. Adding uniform scale gives seven. An affine map has nine linear and three translation parameters. A projectivity has sixteen entries minus one common scale. Its matrix must be invertible. Projective notions such as the absolute conic, named in the hierarchy figures, motivate metric invariants but are developed with reconstruction upgrades in Lecture 6.

```{understanding-check} Check 1.6 — why not add translation to a normal?
A plane is moved three meters sideways without rotation. Does its normal acquire that translation?
```

```{admonition} Solution
:class: dropdown
No. A normal describes orientation, not position. The plane's offset changes, while its direction remains fixed. The homogeneous plane coefficients change through the inverse transpose, which accounts for the offset correctly.
```

```{index} rigid transformation
```

```{index} reference frame
```

```{index} transform composition
```

```{index} normal; outward orientation
```
