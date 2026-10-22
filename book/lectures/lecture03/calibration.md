(lec03-calibration)=
# From field of view to a camera matrix

A wider view fits more of the scene into the same image. That means a shorter focal length **in pixels**. A right triangle tells us exactly how much shorter.

**Sources:** lecture PDF pages 3–12; Spring 2019 Quiz 2, `cs532s19_quiz2-2.pdf`, P1–P4, PDF page 1. Spring 2020 Quiz 3, `cs532s20_quiz3.pdf`, page 1, repeats these questions under a mixed Spring 2019/Spring 2020 header.

```{index} Field of view; Pixel pitch; Principal point
```

## Fit the view into the image

The **horizontal field of view** $\theta$ is the angle between the rays through the left and right image boundaries. For a centered, undistorted pinhole image, half the image width and the focal length form a right triangle.

```{figure} ../../images/lecture03/fov.*
:name: fig-lec03-fov
:width: 80%
:alt: Top view of two image-boundary rays enclosing ninety degrees, meeting an image plane of width 640 at focal distance 320 in pixel-scaled units.

Half the view makes a right triangle: opposite side $W/2$, adjacent side $f_x$. Both lengths must use the same units.
```

````{formula-box} Formula — focal length from centered horizontal field of view
```{math}
:label: eq-lec03-fov
\tan\frac{\theta}{2}=\frac{W/2}{f_x},\qquad
f_x=\frac{W}{2\tan(\theta/2)}.
```

$W$ is image width in pixels, $f_x$ is horizontal focal length in pixels, and $0<\theta<180^\circ$. Use a centered principal point and a rectilinear pinhole model. An off-center principal point needs separate left/right angles; strong lens distortion needs its own model.
````

```{application} Build a calibration estimate
1. **Input:** image width and horizontal FOV. Set the calculator's angle units correctly.
2. Compute $f_x$ with the boxed equation.
3. To form $K$, supply the remaining assumptions: vertical focal length, skew, and principal point.
4. **Check:** doubling image resolution at unchanged FOV doubles focal length in pixels. A wider FOV reduces it.

FOV alone does not determine every entry of $K$.
```

(ex-lec03-calibration)=
````{worked-example} Worked example 3.1 — the 640 × 480 camera
**Adapted from:** Spring 2019 Quiz 2, P1–P2; near-duplicate Spring 2020 Quiz 3, P1–P2.

**Given:** $W=640$, height $480$, horizontal FOV $90^\circ$.

1. Half-angle: $45^\circ$, with $\tan45^\circ=1$.
2. Focal length: $f_x=640/(2\times1)=320$ pixels.
3. Assume square pixels, zero skew, and a centered principal point. Then $f_y=320$ and $(c_x,c_y)=(320,240)$:

$$
K=\begin{pmatrix}320&0&320\\0&320&240\\0&0&1\end{pmatrix}.
$$

**Check:** the boundary ray has horizontal offset $320$ and axial distance $320$ in pixel-scaled image-plane units, so its angle to the axis is $45^\circ$.

**Convention:** this uses image boundaries at $0$ and $640$. If pixel centers are indexed $0,\ldots,639$, a centered principal point can instead be written $(319.5,239.5)$. State the convention; do not mistake a half-pixel choice for a different camera.
````

## A principal point has several descriptions

The **principal point** is where the optical axis meets the image plane. Its pixel coordinates, normalized coordinates, and physical 3D position describe related things in different units.

(ex-lec03-principal)=
````{worked-example} Worked example 3.2 — finish the calibration quiz
**Adapted from:** Spring 2019 Quiz 2, P3–P4; Spring 2020 Quiz 3, P3–P4.

**P3: dimensions and scale.** In $x\sim K[R\mid t]X$, the sizes are $K:3\times3$, $R:3\times3$, $t:3\times1$, $[R\mid t]:3\times4$, $X:4\times1$, and $x:3\times1$. Multiplying the right side by two gives the same image point after homogeneous division. The foundational worked treatment is {ref}`Example 1.18 <ex-lec02-projection>`.

**P4: principal point in the camera frame.** With the positive virtual image plane:

| Description | Coordinates | Units |
| --- | --- | --- |
| Pixel location | $(320,240)$ | pixels |
| Normalized image direction | $(0,0,1)^T$ | normalized coordinates |
| 3D point on the virtual image plane | $(0,0,f_{\rm phys})^T$ | physical length |

Here $f_{\rm phys}$ is the focal length in millimeters, meters, or another physical unit. The quiz's $320$-pixel focal length does **not** determine that length. You need the **pixel pitch** $s_x$ (physical width of a pixel): $f_{\rm phys}=s_x f_x$.

For example, $s_x=0.005\,\mathrm{mm/pixel}$ gives $f_{\rm phys}=1.6\,\mathrm{mm}$ and principal point $(0,0,1.6)\,\mathrm{mm}$. You may write $(0,0,320)$ only if you explicitly choose a pixel-scaled virtual image plane. A physical sensor behind the pinhole uses negative image-plane depth under this axis convention.
````

```{understanding-check} Retest without duplicating the lesson
Use Spring 2020 Quiz 3 as a closed-notes retest. Answer all four problems, then check Examples 3.1–3.2. Before writing any coordinate, label it **pixel**, **normalized**, or **physical 3D**.
```
