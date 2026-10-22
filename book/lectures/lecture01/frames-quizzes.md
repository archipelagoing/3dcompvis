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

**Worked example 1.10 — Fall 2025 Quiz 1, question 3.** {ref}`Read the original problem and every worked step <quiz-17-q3>`.

```{math}
:label: eq-lec01-relative-pose
T_{C_1\leftarrow C_2}=T_{C_1\leftarrow O}\bigl(T_{C_2\leftarrow O}\bigr)^{-1}.
```

The boxed general composition formula is the canonical rule; the displayed quiz equation is its concrete specialization. Its $4\times4$ inputs and output have the same frame/unit conditions. Use the graph as the algorithm: invert the camera-2 object pose, multiply on the left by the camera-1 object pose, and verify on the object origin.

**Worked example 1.11 — Fall 2025 Quiz 1, question 4.** {ref}`Read the original problem and every worked step <quiz-17-q4>`.

## Quiz: tetrahedron face normals and a rotated object

**Assigned source:** Fall 2017 Quiz 9, problem 2(a–b), `cs532_f17_quiz9.pdf`, PDF page 2. This is supplementary practice for Lecture 1; it is not a high-probability exam prediction. Its depth-map problem 1 is previewed in the camera section and retained for deeper treatment in Lectures 3–4.

```{figure} ../../images/lecture01/tetrahedron.*
:name: fig-lec01-tetrahedron
:width: 70%
:alt: Tetrahedron with vertices 1,1,0; 1,2,0; 1,1,1; and 2,1,0.

The quiz tetrahedron. Coordinates are shown relative to the corner $v_1$ for drawing convenience; vertex labels give the actual quiz coordinates. Original schematic, not a metric perspective rendering.
```

**Worked example 1.12 — Fall 2017 Quiz 9, problem 2(a).** {ref}`Read the original problem and every worked step <quiz-18-q2>`.

**Worked example 1.13 — Fall 2017 Quiz 9, problem 2(b).** {ref}`Read the original problem and every worked step <quiz-18-q3>`.

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
