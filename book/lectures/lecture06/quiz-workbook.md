(lec06-quiz-workbook)=
# Original quiz questions and worked solutions

**Read the problem in black. Follow the numbered red steps. Work through the blue mathematics.** Every step explains why it is needed. Matrix calculations show the inputs and intermediate results; written-reasoning questions explain the decision instead of inventing numerical data.

**Source:** the supplied lecture-organized quiz booklet. Full problems follow its wording and givens, with typography normalized; the historical PDF filenames appear below. Source-key corrections and added numerical companions are marked.

**Retests have their own questions and full solutions.** Problems labeled **Original practice** are the booklet’s seven supplemental examples, separate from the 18 historical quizzes. Colored steps remain numbered and readable in grayscale.

## Jump to a quiz

- {ref}`Fall 2025 Quiz 5 — SfM reconstruction upgrades <quiz-source-12>`
- {ref}`Fall 2025 Quiz 6 — Large-scale Structure from Motion <quiz-source-16>`
- {ref}`A5. Linear triangulation with two projection matrices (L6, slides 48–52) <quiz-source-a5>`
- {ref}`A6. Gauss–Newton and reprojection error (L6, slides 46 and 62–70) <quiz-source-a6>`
- {ref}`A7. Affine structure-from-motion factorization (L6, slides 25–37) <quiz-source-a7>`

---

(quiz-source-12)=
## Fall 2025 Quiz 5 — SfM reconstruction upgrades

**Historical source:** `3dcvMid/quizzesf25sol/cs532f25_quiz_5_solution-1.pdf`.

(quiz-12-q1)=
### Question 1, Scenario A

````{original-question}
You photograph an office facade with parallel horizontal bands and parallel pedestrian crossing lines on the road. Is this geometry sufficient to upgrade an entire-scene projective reconstruction? To what type? What extra information is needed?
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — State what each reconstruction preserves
**Why:** The target upgrade determines which geometric constraints are needed.

Recall reconstruction hierarchy: projective transformations preserve incidence; affine preserves parallelism; similarity preserves angles and length ratios; Euclidean/metric reconstruction preserves true lengths when scale is fixed.
````

````{solution-step} 2 — Identify the supplied ideal points
**Why:** Each parallel-line family contributes one direction at infinity.

Each known family of 3D parallel lines gives a vanishing/ideal point in projective reconstruction. Horizontal facade bands provide one direction; road crossing lines provide a second.
````

````{solution-step} 3 — Count the plane-at-infinity constraints
**Why:** Two points leave a family of possible planes.

To identify the plane at infinity $\pi_\infty$ (a 3D plane in projective space), three independent noncollinear ideal points are generally needed. Two ideal points alone do not specify this plane.
````

````{solution-step} 4 — Decide whether an affine upgrade is determined
**Why:** A third independent ideal point is generally needed.

Therefore the two supplied families are $\boxed{\text{insufficient for a unique entire-scene affine upgrade}}$ under the simple count used by the quiz. A third independent family, such as vertical facade edges, may provide the missing ideal point; with suitable calibrated correspondences it constrains the affine plane.
````

````{solution-step} 5 — Separate metric constraints and scale
**Why:** Parallelism alone does not recover angles or absolute lengths.

To reach metric/similarity reconstruction, also require enough Euclidean information, such as camera calibration, orthogonality/angular or absolute-conic constraints with adequate geometry. One known physical length then fixes absolute scale.
````


(quiz-12-q2)=
### Question 1, Scenario B

````{original-question}
You film a planar kitchen floor tiled with regular square tiles. Can this geometry upgrade the reconstruction, and what else is required for metric scale?
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Identify the square-grid constraints
**Why:** Parallel directions, a right angle and equal lengths constrain the observed plane.

A square tile grid contains two line directions with known 3D parallelism, and their intersection angle is $90^\circ$. Equal-length squares also supply metric relations *within the floor plane*.
````

````{solution-step} 2 — State the identifiable upgrade
**Why:** Plane rectification is weaker than upgrading arbitrary off-plane structure.

The square grid directly permits a *metric rectification of the floor plane up to scale*. An *entire-scene* *similarity reconstruction (metric up to scale)* additionally requires sufficient camera-calibration and nondegenerate 3D constraints; diverse views of a single plane alone are not a general guarantee.
````

````{solution-step} 3 — Recover scale when a length is known
**Why:** The ratio of real to reconstructed tile size fixes units.

If tile side length $L$ is given (e.g. 30 cm), compare reconstructed tile dimension $\hat L$ with $L$ and scale all translations/points by $s=L/\hat L$ to fix absolute units.
````

````{solution-step} 4 — State the full-scene limitation
**Why:** A planar grid alone does not determine general 3D metric geometry.

Scope qualification: the known square grid alone, viewed only as a single plane without adequate camera/model constraints, does not in general uniquely determine full 3D scene metric geometry. State the extra assumption of sufficient viewpoints/calibration constraints when claiming an *entire-scene* upgrade.
````


(quiz-12-q3)=
### Question 2

````{original-question}
An image sequence has weak overlap: A overlaps B, B overlaps C, but A and C never share points, and so on. Is a single global factorization or a sequential SfM approach better?
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Inspect the visibility pattern
**Why:** Neighboring-only tracks leave many entries missing.

Form the tracking/measurement matrix mentally: many 3D features occur in only neighboring frames, leaving missing entries outside a narrow image-track visibility band.
````

````{solution-step} 2 — Check complete-data factorization's assumptions
**Why:** Ordinary dense SVD expects a suitable filled measurement matrix.

Classical complete-data factorization $D\approx MS$ presumes adequate common visibility. With widespread missing observations, naive dense SVD cannot be applied directly and estimates can become poorly conditioned.
````

````{solution-step} 3 — Choose incremental reconstruction
**Why:** It can grow using successive overlapping views.

Choose $\boxed{\text{sequential / incremental SfM}}$: start with a strongly overlapping initial pair; estimate two-view geometry and poses, triangulate their tracks, add the next overlapping image via pose estimation, then triangulate new points.
````

````{solution-step} 4 — Refine and verify the result
**Why:** Bundle adjustment uses the visible measurements across the growing model.

Periodically refine all visible cameras and points with bundle adjustment; robust matching handles outliers. This respects the chain-like visibility structure.
````

**Source check / assumptions:** The original answer key describes a similarity upgrade. The rigorous distinction is between rectifying the observed tile plane and uniquely upgrading arbitrary off-plane 3D structure; the latter needs extra camera/scene constraints.


(quiz-source-16)=
## Fall 2025 Quiz 6 — Large-scale Structure from Motion

**Historical source:** `3dcvMid/quizzesf25sol/cs532f25_quiz_6_solution.pdf`.

(quiz-16-q1)=
### Question 1

````{original-question}
Given about 500,000 weakly overlapping photographs of Manhattan, choose incremental, global, hierarchical or hybrid SfM and defend your choice.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Read the dataset constraints
**Why:** Scale, weak overlap and repetition determine the practical bottlenecks.

Read the constraints: huge dataset, weak overlap, large repetitive urban textures (windows/facades), and significant computational burden from repeatedly refining poses and points.
````

````{solution-step} 2 — Compare the candidate pipelines
**Why:** Each approach handles computation and bad pairwise matches differently.

Incremental SfM grows a reconstruction camera by camera; it gives good local control but updating an enormous model can become expensive. Global SfM estimates camera motions jointly but bad pairwise matches in repetitive facades can contaminate the solution.
````

````{solution-step} 3 — Choose a hierarchical strategy
**Why:** Connected clusters make a huge reconstruction more manageable.

Choose $\boxed{\text{hierarchical SfM}}$ (a hierarchical–hybrid strategy is also defensible). Build an image-overlap graph and partition it into moderately sized, sufficiently connected image clusters.
````

````{solution-step} 4 — Reconstruct and refine locally
**Why:** Verified tracks are needed before neighboring pieces can be merged.

Run robust local two-view matching/geometric verification, initialize and triangulate points within each cluster, and perform local bundle adjustment.
````

````{solution-step} 5 — Merge overlapping reconstructions
**Why:** Shared cameras or points provide alignment constraints.

Merge neighboring cluster reconstructions using common tracks/cameras and an appropriate similarity/alignment transformation; reject inconsistent alignments. Perform regional/global adjustment once the merged model is stable.
````

````{solution-step} 6 — Defend the tradeoff
**Why:** The choice follows from the dataset rather than a universal complexity claim.

State why this choice matches the question: computation is localized; false repetitive-feature matches are easier to reject; partial overlaps need not be tracked in a single fully dense global factorization.
````

**Source check / assumptions:** The uploaded key uses an $O(N^3)$ assertion about pure incremental BA. That is not a universal complexity for sparse bundle adjustment, so the defensible argument is high computational cost that depends on graph structure, implementation and solver.


(quiz-16-q2)=
### Question 2

````{original-question}
The images are crowd-sourced and contaminated by “WTF” watermarks/text/frames that may produce false geometric matches. Suggest one simple modification to the RANSAC geometric verification step.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Inspect the consensus beyond its size
**Why:** Repeated overlays can create a large false match set.

Run RANSAC for each candidate image pair, estimating a valid geometric model and collecting its consensus inliers. A high inlier count *alone* may be deceptive when static overlays match each other.
````

````{solution-step} 2 — Measure border concentration
**Why:** Frames and watermarks often produce suspicious edge-localized inliers.

Measure the spatial distribution of inliers: compute the proportion near thin image-border strips, as watermark/frames often occur along borders.
````

````{solution-step} 3 — Check displacement consistency
**Why:** Overlay matches may behave like one common image translation.

For those border inliers, calculate pixel-coordinate displacements $\delta_i=x_i'-x_i$ after dehomogenization (and accounting for image size/crop if needed). Check whether most are approximately the same 2D translation with little parallax or 3D structure.
````

````{solution-step} 4 — Reject or downweight suspicious models
**Why:** The combined evidence can identify a false consensus.

If both conditions hold—large border concentration and near-translation consistency—*reject or downweight the model/image pair*, despite its inlier count. Optionally mask border strips and rerun robust estimation.
````

````{solution-step} 5 — State the heuristic's limitation
**Why:** Genuine scene geometry can also produce nearly translational matches.

To avoid false rejection of genuine pure translations, apply this rule as a *heuristic* together with spatial-coverage and scene-consistency checks, not as an infallible theorem.
````


(quiz-source-a5)=
## A5. Linear triangulation with two projection matrices (L6, slides 48–52)

**Original practice from the supplied booklet; not a historical quiz question.**

(quiz-a5-q1)=
### Illustrative problem

````{original-question}
Rectified cameras have $f=800$ px and baseline $b=0.2$ m. Let 

$$
P_L=\begin{bmatrix}800&0&0&0\\0&800&0&0\\0&0&1&0\end{bmatrix}
$$

 and 

$$
P_R=\begin{bmatrix}800&0&0&-160\\0&800&0&0\\0&0&1&0\end{bmatrix}
$$

. Observed pixels are $(260,120)$ and $(220,120)$. Reconstruct $X=(X,Y,Z)$.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Write two constraints per camera
**Why:** The projected point must lie on each observed viewing ray.

For each point $(u,v)$ in a camera with matrix rows $p_1^T,p_2^T,p_3^T$, the two homogeneous equations are $(up_3^T-p_1^T)\widetilde X=0$ and $(vp_3^T-p_2^T)\widetilde X=0$, with $\widetilde X=(X,Y,Z,1)^T$.
````

````{solution-step} 2 — Stack the complete homogeneous system
**Why:** Both image observations constrain the same four-component point.

Stack two equations from each actual camera:

$$
\begin{pmatrix}-800&0&260&0\\0&-800&120&0\\-800&0&220&160\\0&-800&120&0\end{pmatrix}
\begin{pmatrix}X\\Y\\Z\\W\end{pmatrix}=\begin{pmatrix}0\\0\\0\\0\end{pmatrix}.
$$

The matrix is $4\times4$ and the point is $4\times1$. For a finite point choose $W=1$ after finding a nonzero homogeneous solution.
````

````{solution-step} 3 — Read the first camera's equations
**Why:** They express lateral coordinates in terms of depth.

Row 1 gives $X=(260/800)Z$ and row 2 gives $Y=(120/800)Z$. Row 3 gives $-800X+220Z+160=0$.
````

````{solution-step} 4 — Substitute into the second camera
**Why:** The baseline resolves the remaining depth ambiguity.

Substitute $X$: $-260Z+220Z+160=0\Rightarrow Z=4$ m. Then $X=260(4)/800=1.3$ m, $Y=120(4)/800=0.6$ m.
````

````{solution-step} 5 — Reproject the answer
**Why:** Both original observations should be recovered.

Answer $\boxed{(X,Y,Z)=(1.3,0.6,4)\ \mathrm m}$. Check by projecting into each camera: $(800X/Z,800Y/Z)=(260,120)$; $(800(X-0.2)/Z,800Y/Z)=(220,120)$.
````

````{solution-step} 6 — Explain the noisy SVD solution
**Why:** Noisy constraints require a best-fit homogeneous null vector.

With noisy measurements the four rays/equations are inconsistent. Use SVD $A=U\Sigma V^T$; take the last right singular vector as homogeneous $\widetilde X$, then divide by its fourth coordinate. Refine if needed by minimizing *reprojection* error rather than algebraic residual.
````

````{solution-step} 7 — Verify the full nullspace product
**Why:** Every row should vanish for the exact supplied measurements.

Explicit nullspace check for the answer:

$$
A\begin{pmatrix}1.3\\0.6\\4\\1\end{pmatrix}
=\begin{pmatrix}-800(1.3)+260(4)\\-800(0.6)+120(4)\\-800(1.3)+220(4)+160\\-800(0.6)+120(4)\end{pmatrix}
=\begin{pmatrix}0\\0\\0\\0\end{pmatrix}.
$$

An SVD may return this column divided by $\sqrt{19.05}$, with either sign. Divide its first three entries by its fourth to recover $(1.3,0.6,4)$; do not interpret a unit homogeneous vector as ordinary coordinates.
````


(quiz-source-a6)=
## A6. Gauss–Newton and reprojection error (L6, slides 46 and 62–70)

**Original practice from the supplied booklet; not a historical quiz question.**

(quiz-a6-q1)=
### Illustrative problem

````{original-question}
For calibrated rectified stereo with $u_L=260$, $bf=160$ pixel-meters, and an observed right pixel $u_R^{obs}=219$, refine an initial depth $Z_0=4$ m by one Gauss–Newton iteration.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Define prediction and residual
**Why:** Optimization needs an explicit error whose sign is fixed.

Predicted right pixel from stereo geometry is $\widehat u_R(Z)=260-160/Z$. Define signed residual $r(Z)=\widehat u_R(Z)-219=41-160/Z$. Minimize $E(Z)=r(Z)^2$.
````

````{solution-step} 2 — Evaluate the initial error
**Why:** This gives the starting point for improvement.

Evaluate initial prediction: $\widehat u_R(4)=260-160/4=220$, hence $r(4)=1$ pixel and $E(4)=1$ squared pixel.
````

````{solution-step} 3 — Differentiate the residual
**Why:** The Jacobian predicts how the error responds to a depth change.

Differentiate: $J(Z)=dr/dZ=160/Z^2$, so $J(4)=160/16=10$ pixels/meter.
````

````{solution-step} 4 — Solve the normal equation
**Why:** Gauss–Newton chooses an increment that cancels the linearized residual.

Gauss–Newton normal equation is $(J^TJ)\Delta Z=-J^Tr$. In this one-variable case $10^2\Delta Z=-(10)(1)$, giving $\Delta Z=-0.1$ m.
````

````{solution-step} 5 — Update and re-evaluate
**Why:** The nonlinear residual must actually decrease.

Update $\boxed{Z_1=Z_0+\Delta Z=3.9\ \mathrm m}$. New pixel prediction is $260-160/3.9\approx218.97436$, residual $-0.02564$, error $E(Z_1)\approx0.000657$.
````

````{solution-step} 6 — Compare with the exact solution
**Why:** The small example clarifies the role of damping and multivariable extension.

The exact zero-residual solution is $Z^*=160/41\approx3.902439$ m. Full bundle adjustment extends this to many camera pose and 3D-point variables: $\min_\theta\sum\|x^{obs}-\pi(P(\theta)X(\theta))\|^2$. LM adds damping: $(J^TJ+\lambda I)\Delta\theta=-J^Tr$.
````

**Source check / assumptions:** This is a one-variable reprojection refinement, not full joint bundle adjustment. The purpose is to demonstrate a complete numerical optimization update before scaling to the sparse multivariable system.


(quiz-source-a7)=
## A7. Affine structure-from-motion factorization (L6, slides 25–37)

**Original practice from the supplied booklet; not a historical quiz question.**

(quiz-a7-q1)=
### Illustrative problem

````{original-question}
Four 3D points are $(0,0,0)$, $(2,0,0)$, $(0,2,0)$ and $(0,0,2)$. The first orthographic camera records $(X,Y)$ and the second records $(Y,Z)$. Build the centered observation matrix and explain its rank and SVD factorization.
````

**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.

````{solution-step} 1 — Center the first view
**Why:** Subtracting the image centroid removes its translation.

In view 1, image $x$ coordinates are $(0,2,0,0)$ with mean $0.5$, and $y$ coordinates are $(0,0,2,0)$ with mean $0.5$. Centered rows: $(-.5,1.5,-.5,-.5)$ and $(-.5,-.5,1.5,-.5)$.
````

````{solution-step} 2 — Center the second view
**Why:** Every view must use its own centroid.

In view 2, image coordinates are $(Y,Z)$. Their centered rows are $(-.5,-.5,1.5,-.5)$ and $(-.5,-.5,-.5,1.5)$.
````

````{solution-step} 3 — Stack all measured rows
**Why:** The centered matrix contains two rows per image.

Stack views to obtain the $2m\times n=4\times4$ matrix: 

$$
\boxed{D=\begin{bmatrix}-.5&1.5&-.5&-.5\\-.5&-.5&1.5&-.5\\-.5&-.5&1.5&-.5\\-.5&-.5&-.5&1.5\end{bmatrix}}.
$$
````

````{solution-step} 4 — Check rank three
**Why:** Only three independent shape-coordinate rows are needed.

Rows 2 and 3 are identical, so rank $\le3$. Rows 1,2,4 are linearly independent; therefore $\boxed{\operatorname{rank}(D)=3}$. This illustrates the centered affine/orthographic SfM rank-three condition.
````

````{solution-step} 5 — Split the SVD factors
**Why:** Three singular components produce motion and centered structure factors.

Perform SVD $D=U\Sigma V^T$, retain the top three singular terms, and form $\widetilde M=U_3\Sigma_3^{1/2}$, $\widetilde S=\Sigma_3^{1/2}V_3^T$. Then $D=\widetilde M\widetilde S$ in this noise-free example.
````

````{solution-step} 6 — Explain the affine ambiguity
**Why:** An invertible middle transformation leaves the measurements unchanged.

The factorization is not unique: for any invertible $Q\in\mathbb R^{3\times3}$, $(\widetilde M Q)(Q^{-1}\widetilde S)=D$. Metric constraints and camera-model assumptions are needed to upgrade from arbitrary affine coordinates. With missing feature observations, naive dense SVD also needs a missing-data strategy.
````

````{solution-step} 7 — Multiply an exact geometric factorization
**Why:** Full matrices show one concrete motion-and-shape pair.

An exact geometric factorization makes the matrix multiplication visible:

$$
M=\begin{pmatrix}1&0&0\\0&1&0\\0&1&0\\0&0&1\end{pmatrix},\quad
S=\begin{pmatrix}-.5&1.5&-.5&-.5\\-.5&-.5&1.5&-.5\\-.5&-.5&-.5&1.5\end{pmatrix}.
$$

Multiplying $MS$ selects row 1, row 2, row 2 again, then row 3 of $S$, reproducing every row of $D$. These are one valid camera/centered-shape pair; the balanced SVD factors generally look different but reproduce the same measurements.
````
