(lec06-factorization)=
# Factorization: split one matrix into cameras and shape

**Put the tracks in a table. A low-rank split separates motion from shape.** This works particularly cleanly for an affine camera, which has no division by depth.

**Source:** PDF pages 20–38. Full numerical booklet problem: {ref}`rank-three factorization <quiz-a7-q1>`.

## Center first

````{formula-box} Formula — affine measurements and centering
```{math}
:label: eq-lec06-affine
\begin{aligned}
x_{ij}&=A_iX_j+b_i,\\
\bar x_i&=\frac1n\sum_jx_{ij}=A_i\bar X+b_i,\\
x_{ij}-\bar x_i&=A_i(X_j-\bar X).
\end{aligned}
```

$x_{ij},b_i$ are $2\times1$, $A_i$ is $2\times3$, and $X_j$ is Euclidean $3\times1$. Here the same complete set of $n$ points is visible in every view. Orthographic and weak-perspective cameras are special affine models. Centering removes image translation and chooses the shape centroid as the origin.
````

```{application} Build the centered measurement matrix
1. For each image, compute the mean horizontal and vertical coordinates of the same tracked points.
2. Subtract these means from that image's measurements.
3. Stack two rows per image into $D\in\mathbb R^{2m\times n}$.
4. Do not enter zero for a missing observation; zero is a valid centered coordinate. Basic SVD here assumes complete tracks.
```

```{raw} latex
\Needspace{18\baselineskip}
```

````{formula-box} Formula — rank-three affine factorization
```{math}
:label: eq-lec06-factorization
\begin{aligned}
D&=MS,\\
M&=\begin{pmatrix}A_1\\\vdots\\A_m\end{pmatrix}\in\mathbb R^{2m\times3},\\
S=\begin{pmatrix}X_1-\bar X&\cdots&X_n-\bar X\end{pmatrix}\in\mathbb R^{3\times n},\\
\operatorname{rank}D&\le3,\\
D&=U\Sigma V^T\approx U_3\Sigma_3V_3^T,\\
\widetilde M&=U_3\Sigma_3^{1/2},\qquad
\widetilde S=\Sigma_3^{1/2}V_3^T.
\end{aligned}
```

With noise, retaining the three largest singular values gives the best rank-at-most-three approximation in Frobenius norm. A generic nondegenerate scene can have rank three; a planar/degenerate configuration can have lower rank. Do not force a nonexistent third dimension from noise.
````

```{application} Recover affine motion and shape
1. Center the complete tracks and compute their SVD.
2. Inspect singular values: do three dimensions plausibly explain the data?
3. Form the balanced factors above. Their product reproduces the truncated measurements.
4. Restore each image mean when predicting original coordinates.
5. Treat the factors as affine estimates until additional metric constraints are enforced.
```

For any invertible $3\times3$ matrix $C$, $(\widetilde MC)(C^{-1}\widetilde S)$ gives the same $D$. This is the remaining affine ambiguity after centering.

## Turn an orthographic factorization into metric shape

For calibrated, unit-scale orthographic rows $a_i,b_i$, require unit lengths and perpendicularity. If weak perspective has a different unknown scale in each image, the unit-length constraints must be changed; do not apply this model blindly.

````{formula-box} Formula — orthographic metric upgrade
```{math}
:label: eq-lec06-metric
\begin{aligned}
M&=\widetilde MC,\quad S=C^{-1}\widetilde S,\quad L=CC^T,\\
\widetilde a_iL\widetilde a_i^T&=1,\quad
\widetilde b_iL\widetilde b_i^T=1,\quad
\widetilde a_iL\widetilde b_i^T=0.
\end{aligned}
```

$L$ is symmetric with six unknown entries. Each row pair gives three equations linear in those entries. A valid invertible upgrade requires a positive definite $L$ and sufficient independent constraints. Factor it as $CC^T$, for example with Cholesky. Noisy estimates may need constrained fitting; an indefinite result is not a usable Euclidean metric.
````

```{application} Solve the metric upgrade
1. Write $L=\left(\begin{smallmatrix}l_{11}&l_{12}&l_{13}\\l_{12}&l_{22}&l_{23}\\l_{13}&l_{23}&l_{33}\end{smallmatrix}\right)$.
2. Expand the three constraints per view; solve for its six distinct entries.
3. Check definiteness and constraint residuals.
4. Recover $C$ and update **both** factors. Verify $MS=\widetilde M\widetilde S$.
```

(ex-lec06-upgrade)=
`````{worked-example} Worked example 6.1 — remove unequal axis scaling
```{original-question} Original practice question
Three orthographic views give the estimated motion rows below. Find a diagonal metric upgrade and display the corrected motion matrix.

$$\widetilde M=\begin{pmatrix}2&0&0\\0&1&0\\0&1&0\\0&0&1/2\\2&0&0\\0&0&1/2\end{pmatrix}.$$
```

````{solution-step} 1 — Expand all independent constraints
**Why:** Unit rows set axis scales; perpendicular rows set the cross terms.

$$4l_{11}=1,\quad l_{22}=1,\quad \tfrac14l_{33}=1,$$
$$2l_{12}=0,\quad \tfrac12l_{23}=0,\quad l_{13}=0.$$

The first camera supplies the $xy$ orthogonality constraint, the second $yz$, and the third $xz$. Thus

$$L=\begin{pmatrix}1/4&0&0\\0&1&0\\0&0&4\end{pmatrix}.$$
````

````{solution-step} 2 — Factor the metric
**Why:** Multiplying motion by this factor must make its rows unit length.

$$C=\begin{pmatrix}1/2&0&0\\0&1&0\\0&0&2\end{pmatrix},\qquad CC^T=L.$$
````

````{solution-step} 3 — Correct motion and compensate shape
**Why:** Correcting only motion would change the predicted measurements.

$$M=\widetilde MC=\begin{pmatrix}1&0&0\\0&1&0\\0&1&0\\0&0&1\\1&0&0\\0&0&1\end{pmatrix},$$
$$S=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1/2\end{pmatrix}\widetilde S,\qquad
MS=\widetilde MCC^{-1}\widetilde S=D.$$

Each camera's two rows are perpendicular unit vectors. A common rotation/reflection of the recovered coordinate system remains possible.
````
`````

```{figure} ../../images/lecture06/factorization-house.*
:name: fig-lec06-factorization-house
:width: 95%
:alt: Frames from the lecture house-model sequence and its factorization reconstruction.

The house-model sequence and result, PDF page 38, credited in the deck to Tomasi and Kanade. The matrix method reconstructs structure from tracks; the pictures alone are not the measurement matrix.
```

```{index} Affine factorization
```
```{index} Metric upgrade
```
