(lec02-quaternions)=
# Quaternions: convert without changing the rotation

Prerequisite: {eq}`eq-lec01-quaternion` defines the quaternion convention. This section adds conversion and interpolation.

**Source:** PDF pages 42–49. Page 48 uses the transpose/passive matrix relative to our convention. Page 49 omits a necessary $+1$ inside a square root. The formulas below use one consistent convention; see the {ref}`errata`.

## From a quaternion to a matrix

Write the scalar-first unit quaternion as $q=(w,x,y,z)$. Collecting the point-coordinate coefficients in Lecture 1's quaternion rotation gives the matrix below. Here $x,y,z$ name quaternion components.

````{formula-box} Formula — quaternion to active rotation matrix
```{math}
:label: eq-lec02-qmatrix
R(q)=\begin{pmatrix}
1-2(y^2+z^2)&2(xy-wz)&2(xz+wy)\\
2(xy+wz)&1-2(x^2+z^2)&2(yz-wx)\\
2(xz-wy)&2(yz+wx)&1-2(x^2+y^2)
\end{pmatrix}.
```

$q$ has four unitless entries; $R$ is $3\times3$. This form assumes **unit length**.
````

```{application} Turn an orientation into a matrix
1. Reject a zero quaternion; otherwise normalize it.
2. Substitute its scalar-first components.
3. Check $R^TR=I$, $\det R=1$, and a familiar vector.

Use Example 2.1 to check the signs.
```

## From a matrix back to a quaternion

Taking the trace gives $\operatorname{tr}R=4w^2-1$. That explains the square root and the missing $+1$ in the slide.

````{formula-box} Formula — matrix to quaternion, trace branch
```{math}
:label: eq-lec02-matrixq
\begin{aligned}
w&=\tfrac12\sqrt{1+\operatorname{tr}R},\\
(x,y,z)&=\frac{(R_{32}-R_{23},\ R_{13}-R_{31},\ R_{21}-R_{12})}{4w}.
\end{aligned}
```

Indices are one-based. $R$ must be a proper active rotation. This branch chooses $w\ge0$ and requires $w$ safely away from zero. Near a half-turn, division by $w$ is unstable.

Use the largest vector component instead. For example, when $x$ is largest,

$$
x=\tfrac12\sqrt{1+R_{11}-R_{22}-R_{33}},\quad
(w,y,z)=\frac{(R_{32}-R_{23},\ R_{12}+R_{21},\ R_{13}+R_{31})}{4x}.
$$

The $y$ and $z$ branches follow by cyclic permutation. Normalize the result; the overall sign is arbitrary.
````

```{application} Recover an orientation safely
1. Validate the matrix as a proper rotation.
2. Use the trace branch away from a half-turn; near a half-turn, use the largest vector-component branch.
3. Normalize and rebuild $R(q)$; compare matrices rather than quaternion signs.

See Example 2.1. Clamp small rounding errors only after validating the input.
```

(ex-lec02-conversions)=
```{worked-example} Worked example 2.1 — cycle the axes, then test a half-turn
**Source:** original numerical companions to PDF pages 48–49.

For $120^\circ$ about $a=(1,1,1)^T/\sqrt3$, the quaternion is $q=(1/2,1/2,1/2,1/2)$. Substitution gives $R=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}$. It cycles the coordinate axes: $e_x\to e_y\to e_z\to e_x$.

The trace is zero. Recover $w=1/2$ and $x=y=z=1/(4w)=1/2$. Omitting $+1$ would give $w=0$ and make the remaining divisions fail. This tests a different rotation from Lecture 1's quarter-turn.

For $R=\operatorname{diag}(1,-1,-1)$, the trace branch gives $w=0$, so do not divide by it. The largest-component branch gives $x=1$, $w=y=z=0$: a $180^\circ$ turn about $x$.
```

## Interpolation

The slides mention smooth interpolation. **SLERP** (spherical linear interpolation) follows the unit-quaternion sphere instead of independently changing Euler angles:

````{formula-box} Formula — interpolate two orientations
```{math}
:label: eq-lec02-slerp
q(t)=\frac{\sin((1-t)\Omega)}{\sin\Omega}q_a+
\frac{\sin(t\Omega)}{\sin\Omega}q_b,
\qquad \cos\Omega=q_a^Tq_b,\quad 0\le t\le1.
```

This is an explanatory companion to PDF page 45, not a printed formula. Both endpoints are unit 4-vectors. If their dot product is negative, negate one endpoint first to select a shortest rotation path. Constant change in $t$ gives constant angular speed. For nearly equal endpoints, use normalized linear interpolation to avoid a small $\sin\Omega$ denominator.
````

```{application} Find an in-between orientation
1. Normalize endpoints, align signs, and clamp their computed dot product to $[-1,1]$.
2. Calculate $\Omega$ and the weights, or use the near-equal fallback.
3. Normalize and check the endpoints at $t=0,1$.

Between identity $(1,0,0,0)$ and a $90^\circ$ $z$ rotation, $t=1/2$ gives $(\cos22.5^\circ,0,0,\sin22.5^\circ)$: a $45^\circ$ rotation.
```

```{understanding-check} Check 2.1 — do opposite quaternions cancel?
What happens if you average $q$ and $-q$ directly?
```

```{admonition} Answer
:class: dropdown
You get the zero vector, which cannot represent an orientation. Align signs first; both endpoints describe the same rotation.
```

```{index} SLERP
```
