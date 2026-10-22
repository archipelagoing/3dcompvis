# 3D Computer Vision — The For Dummies Study Edition

**Six lectures. Plain English. The math you actually need.**

Start with the idea, use the formula, then check the example. The full textbook contains the original quiz questions and expanded matrix solutions; this edition gives you a fast route through the same core ideas. The examples below are original practice questions.

## Lecture 1 — Turn geometry into a language a computer can use

**The big idea:** a photograph tells you a direction toward an object. It usually does not tell you how far away the object is.

**Homogeneous coordinates** add one extra number so lines, intersections, and perspective can be handled with matrix multiplication. A normal image point (2,3) becomes (2,3,1). Multiplying all three numbers by the same nonzero number does not change the point.

$$ (2,3,1)^T \sim (4,6,2)^T. $$

**How to use it:** divide by the last coordinate to get an ordinary finite point. If the last coordinate is zero, the point is at infinity; do not divide by zero.

**Points and lines:** a line has coefficients l=(a,b,c). A point x=(u,v,1) is on it when au+bv+c=0. The cross product of two distinct points gives their joining line; the cross product of two distinct lines gives their intersection, up to scale.

$$ l^T x=0, \qquad l=x_1\times x_2, \qquad x=l_1\times l_2. $$

**Moving between coordinate frames:** rotate the coordinates, then translate. A rotation matrix changes direction while preserving lengths and angles. A translation changes the origin. Order matters.

$$ X_c=RX_w+t, \qquad T=\begin{pmatrix}R&t\\0^T&1\end{pmatrix}. $$

The camera center C and translation are related by t=-RC. They are not generally the same vector. To undo a rigid transform, use rotation R-transpose and translation -R-transpose times t.

**Other essentials:** a plane satisfies n-transpose X+d=0; a normal comes from the cross product of two independent directions in the plane. Rotation representations include matrices, axis-angle, and unit quaternions. They describe the same kind of motion using different parameters.

### Quick worked example — check a point

**Problem:** Is x=(2,3,1) on l=(1,1,-5)?

**Step 1 — Substitute.** A point belongs to a line only when the line equation gives zero.

$$ l^Tx=1(2)+1(3)-5(1)=0. $$

**Step 2 — Interpret.** Yes. Getting a nonzero result would mean the point is off the line.

**Remember:** homogeneous scale is a representation choice. Physical distance is a different issue.

## Lecture 2 — Align pictures and estimate transformations

**The big idea:** a homography can map points on one scene plane between two photographs. It also handles pure camera rotation under the pinhole model. It does not generally align an arbitrary 3D scene with parallax.

$$ x'\sim Hx. $$

**The recipe:** multiply the 3-by-3 matrix by the homogeneous point, then divide by the new last coordinate. Straight lines stay straight. Ordinary distances and angles generally do not stay the same.

**Why eight unknowns?** H has nine entries, but multiplying the entire matrix by a nonzero scale makes the same mapping. That leaves eight independent parameters.

**DLT estimation:** each matched point pair gives two linear equations. Four pairs are the minimal sample when they are in a suitable nondegenerate arrangement. Stack the equations into A, solve for its approximate nullspace with SVD, and reshape the result into H.

$$ Ah\approx0,\qquad A\in\mathbb R^{2n\times9}. $$

**SVD in everyday language:** it identifies directions of strong and weak action in a matrix. Here we want the direction that A sends closest to zero: the last right singular vector. Normalize image coordinates before fitting, then undo the normalization afterward.

**RANSAC:** many matches can be wrong. Repeatedly fit a model to a small random sample, count the matches it explains, then refine the best model using its inliers. A clean sample still needs nondegenerate geometry.

**Warping:** for each output pixel, look backward into the input image. Interpolate because the required position usually falls between pixels.

### Quick worked example — apply a homography

**Problem:** Map x=(2,1,1) using H with rows (1,0,0), (0,1,0), and (0.1,0,1).

**Step 1 — Multiply.** The third coordinate carries the perspective scaling.

$$ Hx=\begin{pmatrix}2\\1\\1.2\end{pmatrix}. $$

**Step 2 — Divide.** Return to ordinary image coordinates.

$$ (u',v')=(2/1.2,1/1.2)\approx(1.667,0.833). $$

**Remember:** point correspondences determine the model only when their configuration gives enough independent information.

## Lecture 3 — Turn camera measurements into useful numbers

**The big idea:** the camera first converts world coordinates into camera coordinates, then divides by depth, then converts the result into pixels.

$$ x\sim K[R\mid t]X, \qquad u=f_xX_c/Z_c+c_x, \qquad v=f_yY_c/Z_c+c_y. $$

**K is the camera's pixel conversion:** focal lengths are in pixels; the principal point (c_x,c_y) is the optical-axis location in the image. The common zero-skew K has rows (f_x,0,c_x), (0,f_y,c_y), and (0,0,1).

**Field of view:** a wider angle means a shorter focal length for the same image width.

$$ f_x=\frac{W/2}{\tan(\alpha/2)}. $$

**Ray-plane depth:** a pixel gives a ray X=C+lambda d. Substitute it into the known plane equation to solve for lambda. A ray parallel to the plane has zero denominator; it may have no unique intersection.

$$ \lambda=-\frac{n^TC+d_0}{n^Td}. $$

Here n is the plane normal, d_0 its offset, and d the ray direction. If d is not a unit vector, lambda is not automatically a distance in meters.

**RANSAC budget:** if the inlier fraction is w and the sample size is s, a sample is clean with probability w-to-the-s under the independent model. Choose enough trials N to reach target success probability p.

$$ N\ge\frac{\ln(1-p)}{\ln(1-w^s)}. $$

### Quick worked example — focal length and RANSAC

**Problem:** A 640-pixel-wide image has 90-degree horizontal field of view. Separately, estimate a 99% RANSAC budget for 50% inliers and four-point samples.

**Step 1 — Use the half-angle.** The formula uses half the field of view.

$$ f_x=320/\tan45^\circ=320\text{ pixels}. $$

**Step 2 — Round the budget upward.** A fraction of a trial cannot meet the target.

$$ N\ge\frac{\ln0.01}{\ln(1-0.5^4)}\approx71.36 \quad\Rightarrow\quad N=72. $$

**Remember:** keep pixel units separate from world units. State the assumptions behind every probability calculation.

## Lecture 4 — Find a match along a line, then recover depth

**The big idea:** knowing a point in one image restricts its match in the other image to an epipolar line. It does not usually determine a unique matching point.

$$ l'=Fx,\qquad x'^TFx=0,\qquad l=F^Tx'. $$

**Read the dimensions:** F is 3-by-3. F times a point gives three line coefficients. A point belongs to that line when their dot product is zero. F-transpose handles the reverse direction under this convention.

**The essential matrix E** expresses calibrated two-view geometry. It relates normalized camera coordinates and encodes relative rotation plus translation direction.

$$ E=K'^TFK,\qquad E=[t]_\times R. $$

A valid F has rank two. A valid E has two equal nonzero singular values and one zero singular value. Decomposing E gives candidate poses; positive-depth checks select a physically valid one when the data are suitable. Translation magnitude remains unknown without scale information.

**Rectified stereo:** corresponding points lie on matching image rows. Their horizontal difference is disparity d. Larger disparity means a nearer object.

$$ d=u_L-u_R,\qquad Z=\frac{fb}{d},\qquad \Delta Z\approx-\frac{fb}{d^2}\Delta d. $$

Here f is in pixels, b is the baseline in world units, and d is in pixels. Depth has the same world units as b. The error formula is a local approximation; exact errors can be asymmetric.

**Matching patches:** SAD/SSD compare intensities; NCC reduces sensitivity to affine brightness changes; Census compares local order. Occlusion and windows spanning different depths can still cause wrong matches.

### Quick worked example — epipolar line

**Problem:** F has rows (0,0,0), (0,0,-1), (0,1,0). For x=(2,3,1), find the matching line and test x'=(5,3,1).

**Step 1 — Multiply every row.** The result describes a line, not the matched point.

$$ Fx=\begin{pmatrix}0\\-1\\3\end{pmatrix},\qquad -v'+3=0. $$

**Step 2 — Test the proposed match.** Substitute its coordinates into that line.

$$ x'^TFx=5(0)+3(-1)+1(3)=0. $$

It satisfies the geometry. Appearance and other checks must still establish the actual correspondence.

### Quick worked example — depth and exact error

**Problem:** f=800 pixels, b=0.2 m, and d=40 pixels. What happens if the measured disparity becomes 41 or 39 pixels?

**Step 1 — Compute the original depth.** Multiply focal length by baseline, then divide by disparity.

$$ Z=800(0.2)/40=4\text{ m}. $$

**Step 2 — Recompute rather than guess the sign.** Larger disparity means smaller depth.

$$ Z_{41}=160/41\approx3.90244\text{ m},\qquad Z_{39}=160/39\approx4.10256\text{ m}. $$

The errors are about -9.76 cm and +10.26 cm. The derivative predicts about 10 cm in magnitude. Farther points are more sensitive to the same pixel error.

**Remember:** a zero epipolar residual is a geometric test, not proof of a correct match. Small disparity makes depth fragile.

## Lecture 5 — Find points you can actually track

**The big idea:** a patch must change when moved in either direction. A plain wall gives no clue. An edge gives one direction. A corner or textured patch can give both.

**The structure tensor M** adds up gradient information across the patch. A gradient measures how intensity changes horizontally and vertically.

$$ M=\sum_p w_p\begin{pmatrix}I_x^2&I_xI_y\\I_xI_y&I_y^2\end{pmatrix},\qquad E(u,v)\approx(u,v)M(u,v)^T. $$

**Eigenvalues** measure how strongly the patch constrains motion along two perpendicular directions. Both small means flat. One small means edge-like. Both sufficiently large means a useful feature. Two nonzero gradient components alone are not enough: they may describe one slanted edge.

**Harris** combines determinant and trace into a score. Thresholding removes weak scores. Non-maximum suppression keeps local peaks instead of a cluster around one feature. Shi–Tomasi directly tests the smaller eigenvalue.

$$ R_H=\det M-k(\operatorname{tr}M)^2,\qquad R_{ST}=\lambda_{min}(M). $$

**Lucas–Kanade tracking:** assume the patch keeps approximately the same brightness and shares a small displacement. Linearize intensity change, stack one equation per pixel, then solve for horizontal and vertical motion.

$$ I_xu+I_yv\approx-I_t,\qquad Ad\approx b,\qquad A^TAd=A^Tb. $$

With this convention b=-I_t. Iterate after warping. Pyramids make large motion smaller at coarse resolutions. An edge leaves motion along itself uncertain: the aperture problem. Reject poorly conditioned or inconsistent tracks.

**Exposure changes:** subtract a patch's mean and divide by its standard deviation to reduce positive gain/offset changes. Flat patches have little variance; normalization cannot create missing texture.

**Descriptors and matches:** BRIEF stores intensity comparisons as bits. ORB adds orientation and multiscale detection. BRISK uses long pairs for orientation and short pairs for descriptor bits. Hamming distance counts different bits. A nearest-neighbor ratio test rejects a best candidate that is barely better than second-best. Verify the surviving matches geometrically.

### Quick worked example — Harris and motion

**Problem:** M has diagonal entries 4 and 9 and zero off-diagonals. Use k=0.04. Separately, solve patch equations u=2, v=1, u+v=3.

**Step 1 — Compute the response.** Determinant is the product of eigenvalues; trace is their sum.

$$ R_H=4(9)-0.04(4+9)^2=29.24,\qquad R_{ST}=4. $$

**Step 2 — Solve and check the patch motion.** The third equation verifies the first two.

$$ d=(2,1)^T,\qquad u+v=2+1=3. $$

**Remember:** find a feature, track it, describe it, and verify its match are separate tasks.

## Lecture 6 — Build 3D structure, then improve it

**The big idea:** tracks across images let us estimate camera poses and scene points together. The result must project back onto the measured pixels.

**Reconstruction ambiguity:** photographs alone do not usually determine absolute size. Scaling all scene points and camera centers together preserves their projections. More general uncalibrated reconstructions can preserve images while distorting 3D geometry.

**Projective → affine → metric:** parallelism and the plane at infinity help establish affine geometry; enough independent metric/calibration constraints recover angles and relative lengths. A known length can set scale. One tiled plane does not automatically determine every off-plane 3D relationship.

**Affine factorization:** subtract each image's mean tracked position, stack coordinates into D, and split the centered matrix into motion M and shape S. In ideal affine data its rank is at most three. SVD supplies a low-rank fit. Missing observations are not zeros.

$$ D=MS,\qquad \operatorname{rank}(D)\le3. $$

An invertible change C in the motion factor can be canceled in shape: (MC)(C-inverse S)=MS. Extra metric constraints are needed to choose a Euclidean interpretation.

**Triangulation:** each pixel supplies a ray. With camera rows p1, p2, p3, an observation (u,v) supplies two linear equations. Stack them across views and use the last right singular vector of A.

$$ A_i=\begin{pmatrix}up_3^T-p_1^T\\vp_3^T-p_2^T\end{pmatrix},\qquad AX\approx0. $$

Divide by the fourth homogeneous coordinate if nonzero. Then check positive camera depth, reprojection error, and sufficient angle between rays. Nearly parallel rays give unstable depth. Linear algebraic error and geometric pixel error are different objectives.

**The practical pipeline:** initialize a reliable pair, reconstruct shared points, register another camera using known 3D points, triangulate new tracks, reject failures, and refine. Five-point relative pose uses two calibrated images; P3P estimates one calibrated camera from known 3D points. Both can produce multiple candidates.

**Bundle adjustment:** change cameras and 3D points to reduce image prediction errors. Fix the otherwise arbitrary coordinate frame and scale. A Jacobian tells you how a small parameter change moves a predicted pixel.

$$ r=\text{predicted pixel}-\text{measured pixel},\qquad E=\tfrac12\sum\|r\|^2. $$

$$ (J^TJ)\delta=-J^Tr,\qquad (J^TJ+\lambda D_s)\delta=-J^Tr. $$

The first update is Gauss–Newton; the second adds LM damping with a positive diagonal scale matrix D_s. Solve the system, update the model, then check the actual cost. Reject or reduce a step that makes the fit worse. Sparsity helps because each observation depends on only one camera and one point.

### Quick worked example — one improving depth update

**Problem:** fixed cameras give predicted right coordinate u_R(Z)=260-160/Z pixels. The measured coordinate is 219. Start at Z=4 m.

**Step 1 — Compute the error and sensitivity.** A positive residual means the prediction is too far right.

$$ r=260-160/4-219=1,\qquad J=160/4^2=10. $$

**Step 2 — Solve the scalar update.** Use the local slope to move against the error.

$$ \delta_Z=-r/J=-0.1\text{ m},\qquad Z_{new}=3.9\text{ m}. $$

**Step 3 — Check the real prediction.** A local approximation must improve the nonlinear problem.

$$ r(3.9)\approx-0.025641,\qquad E_{new}\approx0.00032873<0.5. $$

**Remember:** a solver returning numbers does not make a reconstruction correct. Check geometry, assumptions, and actual image error.

## Final TLDR — the whole course in six lines

- Lecture 1: represent points, lines, planes, rotations, and coordinate changes consistently.
- Lecture 2: estimate transformations from good matches; reject outliers and degenerate samples.
- Lecture 3: calibrate the pixel geometry; use explicit units and probability assumptions.
- Lecture 4: epipolar lines restrict matches; disparity gives depth and controls its sensitivity.
- Lecture 5: useful patches constrain both motion directions; tracking and matching need verification.
- Lecture 6: reconstruct cameras and points, state the remaining ambiguity, then minimize reprojection error.

## Two-minute self-check

**1. Why divide a homogeneous point by its last coordinate?** To recover ordinary finite coordinates; a zero last coordinate denotes an ideal point.

**2. What does Fx give?** The corresponding epipolar line coefficients in the second image, under the stated convention.

**3. What happens when disparity doubles?** For fixed focal length and baseline, depth halves.

**4. Why is an edge difficult to track?** Motion along the edge produces little local appearance change.

**5. Does rank three always hold in affine factorization?** No: rank is at most three; degenerate data can have lower rank.

**6. What must you check after an optimization step?** Valid geometry and a reduction in the actual objective, not just its linear approximation.
