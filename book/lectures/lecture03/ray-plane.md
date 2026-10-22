(lec03-ray-plane)=
# Find depth when the point lies on a known plane

One pixel supplies a ray, not a distance. A known plane supplies the missing condition: **keep moving along the ray until you reach the plane**.

**Sources:** lecture PDF pages 3–12; Spring 2020 Quiz 2, `cs532s20_quiz2.pdf`, P1–P2, PDF page 1; `cs532f15_quiz9.pdf`, P1, PDF page 1, printed **Spring 2019 Quiz 9** despite the filename.

## First, keep the two kinds of coordinates straight

(ex-lec03-ray)=
````{worked-example} Worked example 3.3 — two points on one viewing ray
**Adapted from:** Spring 2020 Quiz 2, P1–P2.

The camera center is the origin. A scene point is $A=(X,Y,Z)^T$ and the virtual image plane is at $f=Z/10$, with $Z>0$. Where does the ray meet that plane?

A point along the ray is $a=\lambda A$. Its third coordinate must be $f$, so

$$
\lambda Z=Z/10\quad\Rightarrow\quad\lambda=1/10,
\qquad a=(X/10,Y/10,Z/10)^T.
$$

For $A=(2,1,20)^T$ and $f=2$, the intersection is $a=(0.2,0.1,2)^T$. It is one tenth of the distance along the same ray.

The quiz also asks for $A\times a$. Since $a=A/10$,
$A\times a=(A\times A)/10=\mathbf0$.

**Why zero is correct:** here $A$ and $a$ are ordinary **Euclidean 3D vectors** from the camera center. A zero cross product confirms parallel directions. They are not two homogeneous 2D image points being joined into a line. Same three-entry shape, different meaning.
````

## Intersect the ray with a plane

```{index} Ray–plane intersection; Axial depth
```

Suppose the known plane is $AX+BY+CZ+D=0$. Here $A,B,C$ are plane coefficients, not the point named $A$ in the previous example. Work entirely in the **camera frame**.

The image coordinate $(x',y')$ lies on a virtual plane at focal length $f$. These three values use the same physical length unit. The ray direction with third component one is
$q=(x'/f,y'/f,1)^T$. If you start with a pixel $(u,v)$ instead, first obtain $q=K^{-1}(u,v,1)^T$ under the pinhole model; correct distortion before this step when necessary.

A scene point at axial depth $Z$ is $P=Zq$. Substitute its coordinates into the plane:

$$
A\frac{Zx'}f+B\frac{Zy'}f+CZ+D=0
\quad\Rightarrow\quad
Z\left(A\frac{x'}f+B\frac{y'}f+C\right)=-D.
$$

````{formula-box} Formula — depth from a ray and a plane
```{math}
:label: eq-lec03-ray-plane
\gamma=(A,B,C)\,q,\qquad
Z=-\frac{D}{\gamma}
 =-\frac{Df}{Ax'+By'+Cf},\qquad P=Zq.
```

Require $(A,B,C)\ne\mathbf0$ and $\gamma\ne0$. $Z$ is **axial depth**, not Euclidean range. For dimensionless normal coefficients and $D$ in meters, $Z$ is in meters. Rescaling the plane coefficients leaves the result unchanged.
````

```{application} Recover a 3D point on the known plane
1. **Input:** a calibrated image coordinate and plane coefficients in the camera frame.
2. Form $q$ with third component one. Compute $\gamma=(A,B,C)q$.
3. If $\gamma\ne0$, calculate $Z=-D/\gamma$ and $P=Zq$.
4. **Check:** substitute $P$ into the plane and reproject it. For a point visible in front of this camera, require $Z>0$.

Near-parallel rays amplify input errors. Judge this using the angle between the ray and plane, rather than an unnormalized denominator.
```

```{figure} ../../images/lecture03/ray-plane.*
:name: fig-lec03-ray-plane
:width: 85%
:alt: Camera ray from the origin crosses the virtual image plane at axial depth two and reaches the known scene plane X plus Z equals ten at the point X equals two, Z equals eight.

A side view of Example 3.4. The image-plane intersection fixes the ray; the scene-plane intersection fixes its depth. The $Y$ coordinate is suppressed only in the drawing.
```

(ex-lec03-plane)=
````{worked-example} Worked example 3.4 — put numbers into the depth answer
**Adapted from:** printed Spring 2019 Quiz 9, P1, whose requested symbolic answer is {eq}`eq-lec03-ray-plane`. The following numbers are an original companion.

**Given:** plane $X+Z=10$, $f=2$, $(x',y')=(0.5,0.25)$, all lengths in the same unit.

1. Plane coefficients: $(A,B,C,D)=(1,0,1,-10)$.
2. Ray: $q=(0.25,0.125,1)^T$.
3. Denominator: $\gamma=1(0.25)+0(0.125)+1=1.25$.
4. Depth: $Z=10/1.25=8$; point $P=(2,1,8)^T$.
5. Check the plane: $2+8=10$. Check projection: $(fX/Z,fY/Z)=(0.5,0.25)$.

The point is eight units forward along the optical axis. Its distance from the camera is $\sqrt{2^2+1^2+8^2}=\sqrt{69}$, a little larger.
````

## When there is no useful visible intersection

| Condition | Meaning | Action |
| --- | --- | --- |
| $\gamma=0$, $D\ne0$ | Ray is parallel to the plane and never reaches it | No finite solution |
| $\gamma=0$, $D=0$ | The entire ray lies in the plane | Depth is undetermined |
| $\gamma\ne0$, $D=0$ | Only intersection is the camera center, $Z=0$ | Cannot project this point |
| $Z<0$ | Intersection is behind the camera | Reject as a forward visible point |

**Keep the units honest:** substituting raw pixel columns for $x'$ while using a focal length in millimeters breaks the calculation before the algebra begins.
