(lec01-rotations)=
# Rotations: several descriptions of the same motion

A 3D orientation can be stored as a matrix, an axis and angle, three ordered angles, or a quaternion. These representations are not interchangeable lists of numbers. Ask **what rotates, about which axes, and in which order?** before using any of them.

**Lecture source:** `wk1_2_cs532s26_IntroToGeometry.pdf`, PDF pages 88–100, printed slides 89–101.

## Rotation matrices preserve the dot product

We use active right-handed rotations of column vectors. Each elementary rotation keeps its named axis fixed and performs a 2D rotation in the perpendicular plane.

````{formula-box} Formula — elementary 3D rotations
```{math}
:label: eq-lec01-rotation3
\begin{aligned}
R_x(\theta)&=\begin{pmatrix}1&0&0\\0&c&-s\\0&s&c\end{pmatrix},\quad
R_y(\theta)=\begin{pmatrix}c&0&s\\0&1&0\\-s&0&c\end{pmatrix},\\
R_z(\theta)&=\begin{pmatrix}c&-s&0\\s&c&0\\0&0&1\end{pmatrix},\qquad
c=\cos\theta,\quad s=\sin\theta.
\end{aligned}
```

Each matrix is unitless and $3\times3$; the point it multiplies is $3\times1$. Angles follow the right-hand rule in a right-handed Cartesian frame.

**Conditions:** exact rotations about axes through the origin. A displaced axis needs translations as well. A passive change of coordinates uses the inverse. Specify degrees or radians explicitly.
````

```{application} How to use it — rotate around a named axis
1. Name the axis and state whether points or coordinates are rotating.
2. Substitute sine/cosine in consistent angle units.
3. Multiply by the point.
4. Check the fixed coordinate and preserved length.

See {ref}`Example 1.8 <ex-lec01-order>` and the tetrahedron quiz in {ref}`lec01-frames`.
```

````{formula-box} Formula — validate and invert a rotation
```{math}
:label: eq-lec01-orthogonal
R^TR=I,\qquad \det R=+1,\qquad R^{-1}=R^T.
```

The columns of a proper rotation are orthonormal basis vectors. Dot products are preserved because $(Ra)^T(Rb)=a^T(R^TR)b=a^Tb$; therefore lengths and angles are preserved. Nine entries with six independent orthonormality constraints leave three continuous DOF.

**Conditions:** a proper rotation, not an arbitrary matrix. An orthogonal matrix with determinant $-1$ includes a reflection. Floating-point checks need tolerances; transposing a noisy nonrotation is not generally its inverse.
````

```{application} How to use it — check a claimed rotation
1. Compare $R^TR$ with identity and $\det R$ with $+1$.
2. Use $R^T$ as the inverse only when those conditions hold.
3. Rotate a test vector forward and backward and compare with the original.

See {ref}`Example 1.8 <ex-lec01-order>`.
```

The slide example on PDF page 89 sends $(1,0,1)^T$ to $(0,1,1)^T$ with a positive quarter-turn about $z$. The unchanged last coordinate and equal lengths give two independent sanity checks.

## Composition: order is part of the answer

```{figure} ../../images/lecture01/rotation-order.*
:name: fig-lec01-order
:width: 100%
:alt: Applying z then x rotations gives a different final vector from applying x then z rotations.

The same two rotations in different orders give different results. Original numerical diagram developing PDF pages 93–100.
```

(ex-lec01-order)=
```{worked-example} Worked example 1.8 — prove that rotation order matters
**Source:** original numerical expansion of the compositional-rotation slides, PDF pages 93–100.

Start with $v=(1,0,0)^T$.

1. Apply $R_z(90^\circ)$: $v$ becomes $(0,1,0)^T$.
2. Apply $R_x(90^\circ)$ next: it becomes $(0,0,1)^T$.
3. Reverse the order: the first $x$ rotation leaves $v$ unchanged, then the $z$ rotation gives $(0,1,0)^T$.

Thus $R_xR_z\ne R_zR_x$. The rightmost matrix in each product acts first on the column vector.
```

## Body axes versus fixed axes

An **{term}`intrinsic rotation <Intrinsic rotation>`** sequence uses axes attached to the moving body. An **{term}`extrinsic rotation <Extrinsic rotation>`** sequence uses fixed reference axes. Euler terminology varies: some sources reserve “Euler angles” for a repeated first/third axis, while others also include three-distinct-axis sequences. Write the axes and matrix product explicitly.

The lecture's body-axis sequence uses $x$, then the new $y$, then the new $z$ (PDF 95–98). The fixed-axis sequence uses premultiplication (PDF 99–100). Equal angle values in these two sequences do not generally give equal orientations.

````{formula-box} Formula — ordered-angle composition
```{math}
:label: eq-lec01-ordered-angles
R_{\mathrm{body}\,xyz}=R_x(a)R_y(b)R_z(c),\qquad
R_{\mathrm{fixed}\,xyz}=R_z(c)R_y(b)R_x(a).
```

Angles $a,b,c$ name successive $x,y,z$ rotations. For an orientation matrix mapping body coordinates to world coordinates, a body-axis increment postmultiplies it; a world-axis increment premultiplies it. All factors are $3\times3$.

**Conditions:** the sequence and frame interpretation are essential. At $b=\pm90^\circ$ these three-angle parameterizations become singular: two angle directions lose independent effect, called **{term}`gimbal lock <Gimbal lock>`**. The physical orientation remains valid; its angle description becomes ambiguous.
````

```{application} How to use it — assemble an orientation
1. Specify body versus fixed axes and the full sequence.
2. Associate each angle with its named axis.
3. Multiply the elementary matrices in the stated order.
4. Test a basis vector instead of trusting roll/pitch/yaw names alone.

See {ref}`Example 1.8 <ex-lec01-order>`.
```

For reference, multiplying the body-$xyz$ factors gives

$$
\begin{pmatrix}
c_bc_c&-c_bs_c&s_b\\
s_as_bc_c+c_as_c&-s_as_bs_c+c_ac_c&-s_ac_b\\
-c_as_bc_c+s_as_c&c_as_bs_c+s_ac_c&c_ac_b
\end{pmatrix},
$$

with $c_a=\cos a$, $s_a=\sin a$, and similarly for $b,c$. This is an expansion of the boxed product, not a different rule. Recover it by multiplying two factors first and checking row–column dot products. Roll/pitch/yaw labels depend on axis convention; the lecture's fixed-axis figure uses its own assignment. An explicit product avoids that ambiguity.

## Axis–angle: turn about one direction

An **axis–angle representation** uses a unit axis $a$ and a turn angle $\theta$. Components along the axis stay fixed. Components perpendicular to it undergo the familiar planar rotation.

````{formula-box} Formula — extract axis and angle
```{math}
:label: eq-lec01-axis-angle
\theta=\arccos\!\left(\frac{\operatorname{tr}(R)-1}{2}\right),\qquad
 a=\frac{1}{2\sin\theta}\begin{pmatrix}R_{32}-R_{23}\\R_{13}-R_{31}\\R_{21}-R_{12}\end{pmatrix}.
```

$R$ is a proper $3\times3$ rotation and $\theta\in[0,\pi]$ is its principal angle. $a$ is a unit $3\times1$ direction. The trace is the diagonal sum: one unchanged axial component contributes one, while the perpendicular rotation contributes $2\cos\theta$.

**Conditions:** the axis expression requires $\sin\theta\ne0$. At zero angle the axis is arbitrary. At $\pi$, recover the axis with a stable method, such as a unit eigenvector satisfying $Ra=a$. After validating $R$, clamp small numerical arccos overshoots to $[-1,1]$.
````

```{application} How to use it — recover a geometric rotation
1. Validate $R$, calculate its trace, and recover the angle.
2. Handle near-zero and near-$\pi$ cases separately.
3. Otherwise compute and normalize the axis.
4. Check $Ra=a$ and reconstruct a test rotation.

See {ref}`Example 1.9 <ex-lec01-quaternion>`.
```

An original derivation companion makes this representation computational. Split $p$ into $p_\parallel=a(a^Tp)$ and $p_\perp=p-p_\parallel$. Keep the first part, rotate the second by sine/cosine, and use $a\times p$ as its quarter-turn direction. Collecting terms yields **Rodrigues' formula**:

````{formula-box} Formula — build a rotation from axis and angle
```{math}
:label: eq-lec01-rodrigues
R=I\cos\theta+(1-\cos\theta)aa^T+\sin\theta[a]_\times,
\qquad [a]_\times p=a\times p.
```

Here $[a]_\times=\begin{pmatrix}0&-a_3&a_2\\a_3&0&-a_1\\-a_2&a_1&0\end{pmatrix}$. Every matrix is $3\times3$ and unitless.

**Conditions:** $\|a\|=1$, active right-handed rotation, and consistent angle units. This exact formula is an explanatory supplement to PDF page 91; it is not claimed to be printed on that slide.
````

```{application} How to use it — construct a rotation matrix
1. Normalize the axis and evaluate sine/cosine.
2. Form the outer product $aa^T$ and cross-product matrix.
3. Add the three terms.
4. Check the axis stays fixed and the result is a proper rotation.

See {ref}`Example 1.9 <ex-lec01-quaternion>`.
```

## Quaternions: four entries for a three-DOF rotation

A **{term}`quaternion <Quaternion>`** is a scalar–vector pair $q=(w,v)$ with a special multiplication rule. We use scalar-first Hamilton multiplication and active rotations. Unit length removes one DOF from four entries. The pair $q,-q$ represents the same rotation; this is a discrete ambiguity.

````{formula-box} Formula — unit quaternion and active point rotation
```{math}
:label: eq-lec01-quaternion
\begin{aligned}
q&=\left(\cos\frac\theta2,\;a\sin\frac\theta2\right),\qquad P=(0,p),\\
(w_1,v_1)(w_2,v_2)&=(w_1w_2-v_1^Tv_2,\;w_1v_2+w_2v_1+v_1\times v_2),\\
q^{-1}&=(w,-v)\quad(\|q\|=1),\qquad P'=qPq^{-1}.
\end{aligned}
```

$a,p,v$ are $3\times1$; $a$ is unit length. The vector part of pure quaternion $P'$ is the rotated point. Unit quaternion entries are dimensionless; point coordinates retain their length unit.

**Conditions:** exact under the stated convention. For a nonunit quaternion the inverse is $(w,-v)/(w^2+v^Tv)$, not just its conjugate. PDF page 92 prints $q^{-1}Pq$: that gives the inverse/passive rotation relative to our active convention. Do not mix sandwich orders.
````

```{application} How to use it — rotate a point with a quaternion
1. Build or normalize the scalar-first quaternion.
2. Embed the point as $(0,p)$.
3. Apply Hamilton multiplication twice in the stated order.
4. Extract the vector part; check zero scalar part and preserved vector length.

See {ref}`Example 1.9 <ex-lec01-quaternion>`.
```

(ex-lec01-quaternion)=
```{worked-example} Worked example 1.9 — a quarter-turn in three representations
**Source:** original numerical companion to PDF pages 88–92.

For $90^\circ$ about $a=(0,0,1)^T$, use $R_z(90^\circ)$ and $q=(\sqrt2/2,0,0,\sqrt2/2)$.

1. The matrix trace is one: $\theta=\arccos(0)=90^\circ$.
2. The skew-entry formula returns $a=(0,0,1)$.
3. With $P=(0,1,0,0)$, the first Hamilton product is $qP=(0,\sqrt2/2,\sqrt2/2,0)$.
4. Multiplying by $q^{-1}$ gives $P'=(0,0,1,0)$, so the rotated point is $(0,1,0)^T$.
5. Rodrigues' formula and the elementary matrix agree. The opposite sandwich $q^{-1}Pq$ instead gives $(0,-1,0)^T$.
```

```{understanding-check} Check 1.5 — is negative identity a 3D rotation?
The matrix $-I_3$ preserves lengths. Is it a proper rotation?
```

```{admonition} Solution
:class: dropdown
No: its determinant is $-1$. It is orthogonal but reverses orientation. Proper rotations require both orthogonality and determinant $+1$.
```

```{index} rotation matrix
```

```{index} axis–angle
```

```{index} quaternion
```

```{index} gimbal lock
```

```{index} intrinsic rotation
```

```{index} extrinsic rotation
```
