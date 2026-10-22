(lec06-optimization)=
# Bundle adjustment: move the model until the pixels agree

**A reconstructed point should project back to the pixel where you measured it.** Bundle adjustment changes cameras and points together to reduce those discrepancies. “Bundle” refers to the bundle of viewing rays.

**Source:** PDF pages 46 and 56–72. Fully worked numerical companions: {ref}`a Gauss–Newton reprojection update <quiz-a6-q1>` and {ref}`long-sequence reconstruction <quiz-16-q1>`.

## Define exactly what is being minimized

````{formula-box} Formula — weighted reprojection least squares
```{math}
:label: eq-lec06-ba
\begin{aligned}
r_{ij}(\theta)&=\pi(K_i[R_i\mid t_i]X_j)-x_{ij},\\
E(\theta)&=\tfrac12\sum_{(i,j)\in\mathcal O}r_{ij}^TW_{ij}r_{ij}.
\end{aligned}
```

$\theta$ collects the camera parameters and finite 3D point coordinates; intrinsics may be fixed or estimated as appropriate. $\mathcal O$ contains actual observations only. Each residual is $2\times1$, in pixels, and $W_{ij}$ is a symmetric positive definite $2\times2$ information matrix (often inverse covariance). The source sometimes uses observed-minus-predicted residuals; we consistently use predicted-minus-observed. Changing both residual and Jacobian signs leaves the least-squares update unchanged.
````

```{application} Prepare a meaningful objective
1. Choose which parameters are unknown and which are fixed.
2. Fix the gauge: for calibrated monocular SfM, fixing the first pose and one nonzero baseline/length removes the usual seven freedoms.
3. Stack only valid observed residuals with consistent units and uncertainty weights.
4. Remove gross outliers or use an appropriate robust loss. Ordinary squared error gives large residuals strong influence.
5. Compare actual objective values after every proposed update.
```

## The Jacobian says how a parameter moves a pixel

For zero skew, let camera coordinates be $q=(x_c,y_c,z_c)^T$ and let

$$u=f_xx_c/z_c+c_x,\qquad v=f_yy_c/z_c+c_y.$$

Differentiate one coordinate at a time. For example, $\partial u/\partial x_c=f_x/z_c$ and $\partial u/\partial z_c=-f_xx_c/z_c^2$.

````{formula-box} Formula — projection and pose Jacobian blocks
```{math}
:label: eq-lec06-jacobian
\begin{aligned}
B&=\begin{pmatrix}f_x/z_c&0&-f_xx_c/z_c^2\\0&f_y/z_c&-f_yy_c/z_c^2\end{pmatrix},\\
J_{point}&=BR_i,\qquad
J_{pose}=B\begin{pmatrix}-[q]_\times&I\end{pmatrix}.
\end{aligned}
```

$B$ is $2\times3$, $J_{point}$ is $2\times3$, and $J_{pose}$ is $2\times6$. Here the local pose increment is ordered $(\delta\omega,\delta t)$ and acts on camera coordinates as $q'\approx q+\delta\omega\times q+\delta t$ (a left local rigid-motion increment). A different pose convention changes the block; do not copy it into a different parameterization without checking. Depth must be nonzero. Intrinsics derivatives require extra columns if intrinsics are optimized.
````

```{application} Build a Jacobian row pair
1. Transform the point into the camera frame and compute $B$.
2. Multiply by $R_i$ for world-point derivatives.
3. Use the stated local pose convention for camera derivatives.
4. Insert these blocks into the columns for that camera and that point; unrelated columns are zero.
5. Compare with small finite differences before trusting a new implementation.
```

## Four update rules, one local picture

Linearize $r(\theta+\delta)\approx r+J\delta$. The derivative of $\tfrac12r^TWr$ is $g=J^TWr$. Setting the derivative of the quadratic approximation to zero gives the Gauss–Newton equation.

````{formula-box} Formula — gradient, Newton, Gauss–Newton, and damping
```{math}
:label: eq-lec06-updates
\begin{aligned}
g&=J^TWr,\qquad
H_{exact}=J^TWJ+\sum_k(Wr)_k\nabla^2r_k,\\
\delta_{GD}&=-\eta g,\qquad H_{exact}\delta_N=-g,\\
(J^TWJ)\delta_{GN}&=-g,\\
(J^TWJ+\lambda D)\delta_{LM}&=-g.
\end{aligned}
```

$W$ is held constant in this expression; $D$ is a positive diagonal scaling matrix and $\lambda\ge0$. Gradient descent needs a suitable step size $\eta$. Newton uses the full Hessian. Gauss–Newton drops the residual second-derivative term, often useful near a good fit. Levenberg–Marquardt damps the solve; damping alone does not guarantee an accepted step. Large $\lambda$ gives a scaled gradient-like direction. Parameter scaling matters because meters and radians have different meanings.
````

```{application} Run an iteration
1. Evaluate residuals, weights, Jacobian, and current cost.
2. Solve the damped normal system; do not explicitly invert it.
3. Apply the camera increment with its proper rotation parameterization.
4. Recompute the **actual** cost and verify valid depths.
5. Accept an improving step; otherwise increase damping or reduce the step. Stop using cost, gradient, and step-size criteria.
```

(ex-lec06-gn)=
`````{worked-example} Worked example 6.2 — a full two-variable point update
```{original-question} Original practice question
Fixed rectified cameras have $f=800$ pixels and baseline $b=0.2$ m. Their measured horizontal coordinates are $u_L=260$ and $u_R=219$. Refine the horizontal point block $(X,Z)$ from $(1.3,4)$ m using one Gauss–Newton step. This block example holds the cameras fixed; it is not a complete joint camera-and-point solve.
```

````{solution-step} 1 — Evaluate the residual and Jacobian
**Why:** The update must describe the present prediction error and its local sensitivity.

$$r=\begin{pmatrix}800X/Z-260\\800(X-0.2)/Z-219\end{pmatrix}_{(1.3,4)}=\begin{pmatrix}0\\1\end{pmatrix},$$
$$J=\begin{pmatrix}800/Z&-800X/Z^2\\800/Z&-800(X-0.2)/Z^2\end{pmatrix}=\begin{pmatrix}200&-65\\200&-55\end{pmatrix}.$$
````

````{solution-step} 2 — Write and solve the complete normal system
**Why:** Both parameters affect both observations; solve their coupled equations together.

$$J^TJ=\begin{pmatrix}80000&-24000\\-24000&7250\end{pmatrix},\quad J^Tr=\begin{pmatrix}200\\-55\end{pmatrix},$$
$$\begin{pmatrix}80000&-24000\\-24000&7250\end{pmatrix}\begin{pmatrix}\delta_X\\\delta_Z\end{pmatrix}=\begin{pmatrix}-200\\55\end{pmatrix}.$$

Equivalently, $200\delta_X-65\delta_Z=0$ and $200\delta_X-55\delta_Z=-1$. Subtracting gives $10\delta_Z=-1$, hence

$$\delta=\begin{pmatrix}-0.0325\\-0.1\end{pmatrix},\qquad
\begin{pmatrix}X_{new}\\Z_{new}\end{pmatrix}=\begin{pmatrix}1.2675\\3.9\end{pmatrix}.$$
````

````{solution-step} 3 — Reproject and compare actual costs
**Why:** A linearized improvement must be verified in the original nonlinear model.

$$u_L^{new}=\frac{800(1.2675)}{3.9}=260,\qquad
u_R^{new}=\frac{800(1.2675-0.2)}{3.9}\approx218.974359.$$
$$E_{old}=\tfrac12(0^2+1^2)=0.5,\qquad
E_{new}\approx\tfrac12(0^2+(-0.025641)^2)=0.00032873.$$

Both depths are positive and the cost falls. The exact horizontal solution is $Z=160/(260-219)\approx3.902439$ m and $X=260Z/800\approx1.268293$ m. One nonlinear iteration gets close; it need not finish exactly.
````
`````

## See a point update in real 3D

`````{interactive-demo} refinement
The cameras stay fixed. The point is constrained to the left measured ray, with $X=260Z/800$ and $Y=120Z/800$. Rotate the scene to see that moving along this ray changes the right projection. Adjust the initial depth or right measurement, then take a Gauss–Newton/LM step.

**Static equivalent:** $u_R(Z)=260-160/Z$, $r(Z)=u_R(Z)-219$, and $J=160/Z^2$. At $Z=4$, $u_R=220$, $r=1$, and $J=10$. An undamped step gives $\delta_Z=-r/J=-0.1$ m. At $Z=3.9$, $r\approx-0.025641$; the next update moves back toward $3.902439$ m. The left projection remains $(260,120)$ throughout.

For this one-parameter subset, damping solves $(J^2+\lambda)\delta_Z=-Jr$. The interactive checks positive depth and actual cost, reducing the step if necessary. The measured right pixel defines another ray; the moving point's projection approaches it. This is a visual model of a point refinement, while full bundle adjustment also updates camera parameters.

```{figure} ../../images/lecture06/refinement-rays.*
:name: fig-lec06-refinement
:width: 85%
:alt: A point moves along the fixed left viewing ray to reduce its right-image reprojection error.

Original diagram. Camera centers and the left ray stay fixed; the point's right ray changes as depth is refined.
```
`````

## Why large reconstructions can still be solved

Each image residual depends on **one camera and one point**, not every unknown. That creates sparse Jacobian blocks.

````{formula-box} Formula — eliminate point updates with the Schur complement
```{math}
:label: eq-lec06-schur
\begin{pmatrix}U&V\\V^T&W_p\end{pmatrix}
\begin{pmatrix}\delta_c\\\delta_p\end{pmatrix}
=-\begin{pmatrix}g_c\\g_p\end{pmatrix},
```
```{math}
\begin{aligned}
(U-VW_p^{-1}V^T)\delta_c&=-g_c+VW_p^{-1}g_p,\\
W_p\delta_p&=-g_p-V^T\delta_c.
\end{aligned}
```

$U$ is the camera block, $W_p$ the point block, and $V$ their coupling in the (possibly damped) normal system. $W_p$ is block diagonal for independent point parameters. Inverse notation expresses elimination; implementations solve the small blocks. Gauge fixing and sufficient observations are needed for nonsingular systems. Here $W_p$ is not the observation-weight matrix $W$ above.
````

```{application} Solve a sparse bundle system
1. Assemble blocks only where observations connect a camera and a point.
2. Eliminate each independent point block to form the reduced camera system.
3. Solve for camera updates, then back-substitute for point updates.
4. Use appropriate ordering, scaling, and preconditioning; inspect connectivity and degeneracy.
```

The source ends with software examples. The important transferable ideas are the residual definition, a consistent Jacobian, gauge fixing, sparse structure, and checking actual improvement. A large parameter count alone does not tell you whether a reconstruction is well constrained.

```{index} Bundle adjustment
```
```{index} Gauss–Newton
```
```{index} Levenberg–Marquardt
```
```{index} Schur complement
```
