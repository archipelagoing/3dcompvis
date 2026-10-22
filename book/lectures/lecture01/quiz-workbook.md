(lec01-quiz-workbook)=
# Original quiz questions and worked solutions

**Read the problem in black. Follow the numbered red steps. Work through the blue mathematics.** Every step explains why it is needed. Matrix calculations show the inputs and intermediate results; written-reasoning questions explain the decision instead of inventing numerical data.

**Source:** the supplied lecture-organized quiz booklet. Full problems follow its wording and givens, with typography normalized; the historical PDF filenames appear below. Source-key corrections and added numerical companions are marked.

**Retests have their own questions and full solutions.** Problems labeled **Original practice** are the booklet’s seven supplemental examples, separate from the 18 historical quizzes. Colored steps remain numbered and readable in grayscale.

## Jump to a quiz

- {ref}`Fall 2025 Quiz 1 — Probability and rigid camera poses <quiz-source-17>`
- {ref}`Fall 2017 Quiz 9 — Depth maps and tetrahedron normals <quiz-source-18>`

---

(quiz-source-17)=
## Fall 2025 Quiz 1 — Probability and rigid camera poses

**Historical source:** `3dcvMid/quizzesf25sol/cs532f25_quiz_1_solution.pdf`.

(ex-lec03-probability)=
(quiz-17-q1)=
### Question 1

````{original-question}
A parlay succeeds only if all three independent fair coin flips succeed. What is the chance of winning one parlay?
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Identify independent events
**Why:** Independent outcomes let us multiply their probabilities.

Each fair flip succeeds with probability $1/2$. The three flip outcomes are independent.
````

````{solution-step} 2 — Multiply the three chances
**Why:** A parlay wins only when every flip wins.

Multiply probabilities for the joint event: $P(\text{all 3})=(1/2)^3=1/8$.
````

````{solution-step} 3 — Interpret the probability
**Why:** A fraction and a percentage describe the same chance.

$\boxed{P(\text{win})=1/8=12.5\%}$. This is the same product rule used for all-inlier RANSAC samples.
````


(quiz-17-q2)=
### Question 2

````{original-question}
You attempt one three-coin-flip parlay each day for seven independent days. What is the probability of winning at least one?
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Find one day's failure chance
**Why:** Counting no wins is easier than counting every possible pattern of wins.

One parlay win probability is $q=1/8$. Its loss probability is $1-q=7/8$.
````

````{solution-step} 2 — Multiply seven failures
**Why:** The daily attempts are assumed independent.

All seven attempts fail with probability $P(0\text{ wins})=(7/8)^7$.
````

````{solution-step} 3 — Take the complement
**Why:** At least one win and no wins are complementary events.

Use the complement of no wins: 

$$
P(\ge1\text{ win})=1-(7/8)^7=1-823543/2097152.
$$
````

````{solution-step} 4 — Convert to a percentage
**Why:** The result should be a probability between zero and one.

Therefore $\boxed{P(\ge1\text{ win})\approx0.607304\approx60.73\%}$.
````


(ex-lec01-relative-pose)=
(quiz-17-q3)=
### Question 3

````{original-question}
Two static cameras concurrently estimate the 3D rigid pose of the same object, as $[R_1,t_1]$ and $[R_2,t_2]$ in their own camera frames. Can one recover the relative camera pose? Explain and derive a transformation.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Define the coordinate maps
**Why:** Matrix order is meaningful only after we know what each map does.

Define the direction before multiplying. For $i=1,2$, the object-to-camera pose is

$$
T_i=\begin{pmatrix}R_i&t_i\\0&1\end{pmatrix},\qquad X_{C_i}=T_iX_O.
$$

Here $R_i$ is $3\times3$, $t_i$ is $3\times1$, and $T_i$ is $4\times4$. The same physical object frame, time and length scale must be used in both estimates.
````

````{solution-step} 2 — Invert camera 2's object pose
**Why:** We must return to the shared object frame first.

Undo the second camera's map to return to object coordinates:

$$
X_O=T_2^{-1}X_{C_2},\qquad T_2^{-1}=\begin{pmatrix}R_2^T&-R_2^Tt_2\\0&1\end{pmatrix}.
$$

A rotation's inverse is its transpose, and its translation must be undone in the rotated frame.
````

````{solution-step} 3 — Compose the frame path
**Why:** The object frame connects the two camera frames.

Follow the frame path camera 2 → object → camera 1:

$$
X_{C_1}=T_1(T_2^{-1}X_{C_2})=(T_1T_2^{-1})X_{C_2}.
$$

The rightmost matrix acts first; reversing the product changes the mapping direction.
````

````{solution-step} 4 — Multiply the block matrices
**Why:** This exposes the recovered rotation and translation separately.

Multiply the complete block matrices:

$$
\begin{aligned}
T_{C_1\leftarrow C_2}
&=\begin{pmatrix}R_1&t_1\\0&1\end{pmatrix}
\begin{pmatrix}R_2^T&-R_2^Tt_2\\0&1\end{pmatrix}\\
&=\begin{pmatrix}R_1R_2^T&t_1-R_1R_2^Tt_2\\0&1\end{pmatrix}.
\end{aligned}
$$

Thus $R_{12}=R_1R_2^T$ and $t_{12}=t_1-R_1R_2^Tt_2$.
````

````{solution-step} 5 — Insert a numerical example
**Why:** Full matrices make the abstract composition concrete.

Original numerical companion, not extra quiz givens: let $R_1=R_2=I$, $t_1=(1,1,4)^T$, $t_2=(-1,1,4)^T$. Then

$$
T_1=\begin{pmatrix}1&0&0&1\\0&1&0&1\\0&0&1&4\\0&0&0&1\end{pmatrix},\quad
T_2^{-1}=\begin{pmatrix}1&0&0&1\\0&1&0&-1\\0&0&1&-4\\0&0&0&1\end{pmatrix}.
$$

Their product is

$$
T_{12}=\begin{pmatrix}1&0&0&2\\0&1&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix}.
$$
````

````{solution-step} 6 — Check the object origin
**Why:** A known point tests both the matrix order and translation sign.

Check the direction on the observed object origin:

$$
\begin{pmatrix}1&0&0&2\\0&1&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix}
\begin{pmatrix}-1\\1\\4\\1\end{pmatrix}
=\begin{pmatrix}-1+2\\1\\4\\1\end{pmatrix}
=\begin{pmatrix}1\\1\\4\\1\end{pmatrix}.
$$

This is exactly camera 1's observation $t_1$. Independent unknown pose scales or inconsistent object-frame orientations prevent this metric recovery.
````

**Source check / assumptions:** The uploaded key's superscript/subscript arrows are inconsistent in places. The formula above is unambiguous because its mapping direction is defined explicitly. If the poses are only known up to unknown scale, relative metric translation is not determined absolutely.


(ex-lec01-object-plane)=
(quiz-17-q4)=
### Question 4

````{original-question}
Can one determine the 3D plane passing through both camera centers and the tracked object's center? Derive it.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Choose one working frame
**Why:** Points can share a plane equation only when their coordinates use the same frame.

Use camera-1 coordinates as the world frame: $C_1=(0,0,0)^T$. The object-frame origin is observed at $O=t_1$.
````

````{solution-step} 2 — Locate camera 2
**Why:** Its origin maps to the translation column of the relative camera pose.

Find camera-2 center $C_2$ as the translation part of the transform $^{C_1}T_{C_2}$ from Question 3.
````

````{solution-step} 3 — Cross two in-plane vectors
**Why:** The cross product is perpendicular to both directions.

Two vectors lying in the plane are $a=O-C_1$ and $b=C_2-C_1$. Take the cross product to find a plane normal: $\boxed{n=a\times b}$.
````

````{solution-step} 4 — Write the plane equation
**Why:** Every displacement inside the plane is perpendicular to its normal.

The plane equation is $n^T(X-C_1)=0$ or $n^TX+d=0$ with $d=-n^TC_1$. Because $C_1=0$, $\boxed{n^TX=0}$.
````

````{solution-step} 5 — Check for collinearity
**Why:** Three collinear points do not determine a unique plane.

Require $n\ne0$, i.e. the three points are noncollinear. If cameras and object center lie on one line, infinitely many planes contain them. Draw a triangle joining $C_1,C_2,O$ with a perpendicular arrow $n$.
````

````{solution-step} 6 — Expand and verify a numerical plane
**Why:** Substitution checks that all three required points actually lie on the answer.

Original numerical companion: the preceding question gave $C_1=(0,0,0)^T$, $C_2=(2,0,0)^T$, $O=(1,1,4)^T$. Expand the cross product:

$$
n=\begin{pmatrix}1\\1\\4\end{pmatrix}\times\begin{pmatrix}2\\0\\0\end{pmatrix}
=\begin{pmatrix}1(0)-4(0)\\4(2)-1(0)\\1(0)-1(2)\end{pmatrix}
=\begin{pmatrix}0\\8\\-2\end{pmatrix}\sim\begin{pmatrix}0\\4\\-1\end{pmatrix}.
$$

The plane is $4Y-Z=0$. Substitution gives $0$ for both camera centers and $4(1)-4=0$ for the object origin. An extended object need not lie entirely on this plane.
````

```{figure} ../../images/quizzes/camera-plane.*
:width: 70%
:alt: The two camera centers and object origin determine a plane when noncollinear. Schematic from the supplied quiz booklet.

The two camera centers and object origin determine a plane when noncollinear. Schematic from the supplied quiz booklet.
```


(quiz-source-18)=
## Fall 2017 Quiz 9 — Depth maps and tetrahedron normals

**Historical source:** `3dcvMid/olderquizzes/cs532_f17_quiz9.pdf`.

(ex-lec01-depth)=
(quiz-18-q1)=
### Problem 1

````{original-question}
Explain how to convert two depth maps into a single 3D point cloud in a common reference frame. What information is required? Make a sketch.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Collect calibration and poses
**Why:** Depth alone does not identify a point's coordinates in a shared world frame.

For camera $i\in\{1,2\}$ obtain intrinsic matrix $K_i$, per-pixel depth $Z_i(u,v)$, and a known camera-to-world rigid transform 

$$
^{W}T_{C_i}=\begin{bmatrix}R_i&t_i\\0&1\end{bmatrix}
$$

. First correct lens distortion if depth is reported in distorted coordinates.
````

````{solution-step} 2 — Backproject each depth pixel
**Why:** Intrinsics turn a pixel into a viewing ray; axial depth sets its scale.

For pixel $p_i=(u,v,1)^T$, compute normalized camera ray $r_i=K_i^{-1}p_i$, whose last component is 1 under standard intrinsics. If depth means camera-axis $Z$, backproject: $\boxed{X_{C_i}=Z_i(u,v)\,K_i^{-1}p_i}$.
````

````{solution-step} 3 — Expand the camera coordinates
**Why:** This makes the pixel offsets and focal-length divisions explicit.

For standard intrinsics with zero skew this becomes $X_{C_i}=((u-c_x)Z/f_x,(v-c_y)Z/f_y,Z)^T$. Skip missing, zero, invalid, or occluded depth pixels.
````

````{solution-step} 4 — Transform both clouds into one frame
**Why:** Coordinates from different cameras cannot be merged directly.

Map every 3D point into the *same* world frame: $\boxed{X_W=R_iX_{C_i}+t_i}$. Combine both transformed sets; optional voxel fusion/outlier removal prevents duplicates or inconsistent observations.
````

````{solution-step} 5 — Check the meaning of depth
**Why:** Range along a ray and depth along the optical axis require different scaling.

If depth means *Euclidean range along ray*, use $X_{C_i}=\rho_i r_i/\|r_i\|$, not $Z_i r_i$. The question needs a depth convention, the two sets of intrinsics, and the relative/world poses.
````

````{solution-step} 6 — Multiply a complete numerical example
**Why:** Both camera observations should land on the same world point.

Original numerical companion: use

$$
K=\begin{pmatrix}500&0&250\\0&500&250\\0&0&1\end{pmatrix},\quad
K^{-1}=\begin{pmatrix}1/500&0&-1/2\\0&1/500&-1/2\\0&0&1\end{pmatrix}.
$$

Both axial depths are $10$. Backproject each measurement explicitly:

$$
X_{C_1}=10K^{-1}\begin{pmatrix}300\\250\\1\end{pmatrix}
=10\begin{pmatrix}300/500-1/2\\250/500-1/2\\1\end{pmatrix}
=\begin{pmatrix}1\\0\\10\end{pmatrix},
$$

$$
X_{C_2}=10K^{-1}\begin{pmatrix}200\\250\\1\end{pmatrix}
=10\begin{pmatrix}200/500-1/2\\250/500-1/2\\1\end{pmatrix}
=\begin{pmatrix}-1\\0\\10\end{pmatrix}.
$$

Camera 2 is at world $(2,0,0)$ with identity orientation. Its camera-to-world map gives

$$
\begin{pmatrix}1&0&0&2\\0&1&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix}
\begin{pmatrix}-1\\0\\10\\1\end{pmatrix}
=\begin{pmatrix}1\\0\\10\\1\end{pmatrix}.
$$

The two observations now represent the same world point.
````

```{figure} ../../images/lecture01/depth-rays.*
:width: 70%
:alt: Two camera rays meet at the same point after both depth maps are transformed into one frame.

Two camera rays meet at the same point after both depth maps are transformed into one frame.
```


(ex-lec01-tetrahedron)=
(quiz-18-q2)=
### Problem 2(a)

````{original-question}
A tetrahedron has vertices $v_1=(1,1,0)$, $v_2=(1,2,0)$, $v_3=(1,1,1)$, $v_4=(2,1,0)$. Find one *outward* surface normal per face, and sketch the result.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Choose faces and an orientation rule
**Why:** A cross product gives two possible normal directions depending on edge order.

Use the four faces 123, 124, 134 and 234. For each face take two edge vectors and cross them. Choose outward unit normals for a consistent answer; the opposite vertex lies on the inward side. A candidate $n$ is outward when $n^T(v_{opposite}-v_{face})<0$.
````

````{solution-step} 2 — Compute face 123
**Why:** The opposite vertex tells us whether to flip the candidate normal.

Face 123: subtract the vertices and expand:

$$
a=v_2-v_1=\begin{pmatrix}0\\1\\0\end{pmatrix},\quad b=v_3-v_1=\begin{pmatrix}0\\0\\1\end{pmatrix},
$$

$$
a\times b=\begin{pmatrix}1(1)-0(0)\\0(0)-0(1)\\0(0)-1(0)\end{pmatrix}
=\begin{pmatrix}1\\0\\0\end{pmatrix}.
$$

The opposite vertex is toward $+X$, so this candidate points inward. Flip it: $n_{123}=(-1,0,0)^T$.
````

````{solution-step} 3 — Compute face 124
**Why:** The cross product must point away from the tetrahedron's interior.

Face 124 uses $a=(0,1,0)^T$ and $b=v_4-v_1=(1,0,0)^T$:

$$
a\times b=\begin{pmatrix}1(0)-0(0)\\0(1)-0(0)\\0(0)-1(1)\end{pmatrix}
=\begin{pmatrix}0\\0\\-1\end{pmatrix}.
$$

It points away from the opposite vertex above $Z=0$, so $n_{124}=(0,0,-1)^T$.
````

````{solution-step} 4 — Compute face 134
**Why:** A candidate pointing toward the opposite vertex is inward.

Face 134 uses $a=(0,0,1)^T$, $b=(1,0,0)^T$:

$$
a\times b=\begin{pmatrix}0(0)-1(0)\\1(1)-0(0)\\0(0)-0(1)\end{pmatrix}
=\begin{pmatrix}0\\1\\0\end{pmatrix}.
$$

The opposite vertex lies toward $+Y$, so flip this inward candidate: $n_{134}=(0,-1,0)^T$.
````

````{solution-step} 5 — Compute face 234
**Why:** The slanted face also needs normalization to unit length.

Face 234 uses $a=v_3-v_2=(0,-1,1)^T$, $b=v_4-v_2=(1,-1,0)^T$:

$$
a\times b=\begin{pmatrix}(-1)(0)-1(-1)\\1(1)-0(0)\\0(-1)-(-1)(1)\end{pmatrix}
=\begin{pmatrix}1\\1\\1\end{pmatrix}.
$$

Its dot product with $v_1-v_2=(0,-1,0)^T$ is $-1$, so it already points outward. Divide by $\sqrt{1+1+1}=\sqrt3$: $n_{234}=(1,1,1)^T/\sqrt3$.
````

````{solution-step} 6 — Collect and check all normals
**Why:** Unit length, perpendicularity and outward direction are separate checks.

The four answers are

$$
n_{123}=\begin{pmatrix}-1\\0\\0\end{pmatrix},\quad n_{124}=\begin{pmatrix}0\\0\\-1\end{pmatrix},\quad
n_{134}=\begin{pmatrix}0\\-1\\0\end{pmatrix},\quad n_{234}=\frac1{\sqrt3}\begin{pmatrix}1\\1\\1\end{pmatrix}.
$$

Each has unit length and zero dot product with both edges of its own face. Draw arrows outward from the four face interiors.
````

```{figure} ../../images/lecture01/tetrahedron.*
:width: 70%
:alt: The tetrahedron from the problem, with all four given vertices.

The tetrahedron from the problem, with all four given vertices.
```


(ex-lec01-rotated-normals)=
(quiz-18-q3)=
### Problem 2(b)

````{original-question}
Rotate the complete tetrahedron by $+90^\circ$ about the global $Z$ axis. Find the modified face normals.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Build the rotation matrix
**Why:** The active right-handed convention fixes the signs.

For an *active*, right-handed $+90^\circ$ rotation, 

$$
R_z(90^\circ)=\begin{bmatrix}\cos90^\circ&-\sin90^\circ&0\\\sin90^\circ&\cos90^\circ&0\\0&0&1\end{bmatrix}=\begin{bmatrix}0&-1&0\\1&0&0\\0&0&1\end{bmatrix}.
$$
````

````{solution-step} 2 — Apply the normal transformation rule
**Why:** A rigid rotation rotates a normal without adding translation.

Pure rigid rotations rotate normals by the same matrix: $n'_{ijk}=R_zn_{ijk}$. (General nonrigid affine transforms use an inverse-transpose rule instead.)
````

````{solution-step} 3 — Multiply the three axis normals
**Why:** Writing every matrix-vector product exposes the changed directions.

Multiply the rotation by each axis-aligned normal:

$$
\begin{aligned}
n'_{123}&=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}\begin{pmatrix}-1\\0\\0\end{pmatrix}
=\begin{pmatrix}0\\-1\\0\end{pmatrix},\\
n'_{124}&=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}\begin{pmatrix}0\\0\\-1\end{pmatrix}
=\begin{pmatrix}0\\0\\-1\end{pmatrix},\\
n'_{134}&=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}\begin{pmatrix}0\\-1\\0\end{pmatrix}
=\begin{pmatrix}1\\0\\0\end{pmatrix}.
\end{aligned}
$$
````

````{solution-step} 4 — Multiply the slanted normal
**Why:** Its normalization must be preserved too.

For the slanted face, retain the normalization:

$$
n'_{234}=\frac1{\sqrt3}\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}
\begin{pmatrix}1\\1\\1\end{pmatrix}
=\frac1{\sqrt3}\begin{pmatrix}0(1)-1(1)+0(1)\\1(1)+0(1)+0(1)\\0(1)+0(1)+1(1)\end{pmatrix}
=\frac1{\sqrt3}\begin{pmatrix}-1\\1\\1\end{pmatrix}.
$$
````

````{solution-step} 5 — Check geometric consistency
**Why:** A rotation preserves lengths and perpendicularity.

Check the rotation rather than adding translation: $R_z^TR_z=I$ preserves unit lengths and dot products. Rotating the vertices and recomputing their outward normals gives these same answers. Under a general nonrigid affine transform, normals instead use an inverse transpose.
````
