(lec01-cameras)=
# Image formation: where does a 3D point appear?

You move a camera toward a stationary object. Does the object's image move toward the principal point, or away from it? This is the lecture's final hands-on question, and it ties projection to reference frames.

**Lecture source:** `wk1_2_cs532s26_IntroToGeometry.pdf`, PDF pages 104–114, printed slides 105–115. The introductory image-formation slides credit John Oliensis.

## Start with a pinhole and similar triangles

An ideal **pinhole camera** sends each visible scene point along a ray through the camera center to an image plane. The physical sensor behind the pinhole receives an inverted image. We instead use a **virtual image plane** in front of it, which gives a positive focal-length convention and avoids carrying that inversion into every equation.

```{figure} ../../images/lecture01/pinhole.*
:name: fig-lec01-pinhole
:width: 85%
:alt: A ray from a scene point crosses a virtual image plane in front of the pinhole, forming similar triangles.

A side-view similar-triangle construction. Original diagram developing PDF pages 105–107; those slide sections credit John Oliensis. The drawing's page orientation is schematic; the coordinate signs follow the labeled camera/image axes.
```

The small image triangle and large scene triangle share the ray angle. Their corresponding side lengths are proportional. The vertical ratio is $y/Y_c=f/Z_c$; the horizontal argument gives the same ratio for $x$.

````{formula-box} Formula — perspective projection in camera coordinates
```{math}
:label: eq-lec01-pinhole
x=f\frac{X_c}{Z_c},\qquad y=f\frac{Y_c}{Z_c},\qquad
\begin{pmatrix}x\\y\\f\end{pmatrix}
=\frac{f}{Z_c}\begin{pmatrix}X_c\\Y_c\\Z_c\end{pmatrix}.
```

$(X_c,Y_c,Z_c)$ is the point in camera coordinates. $x,y,f$ are coordinates and focal length on the virtual image plane in the same length unit; the ratios are dimensionless. Normalized image coordinates are $(X_c/Z_c,Y_c/Z_c)$.

**Conditions:** exact ideal central projection, $f>0$, and $Z_c\ne0$. Visible points for this forward-facing model need $Z_c>0$. Pixel coordinates require calibration; do not confuse physical focal length with focal length measured in pixels.
````

```{application} How to use it — project a point
1. Express the point in camera coordinates.
2. Check it is in front of the camera.
3. Divide the transverse coordinates by depth and multiply by focal length.
4. Check that points on one ray have the same image and that doubling depth at fixed transverse position halves the image displacement.

See {ref}`Example 1.14 <ex-lec01-projection>`.
```

(ex-lec01-projection)=
```{worked-example} Worked example 1.14 — perspective loses depth
**Source:** original numerical development of PDF pages 107–110.

Use a virtual-plane focal length of $2$ length units and a point $(1,0.5,10)$ in camera coordinates.

1. $x=2(1/10)=0.2$ and $y=2(0.5/10)=0.1$ in image-plane length units.
2. The point $(2,1,20)$ gives the same $(0.2,0.1)$ because every scene coordinate was scaled equally.
3. The point $(1,0.5,20)$ instead gives $(0.1,0.05)$: it moved deeper without increasing its transverse displacement.

One image coordinate does not uniquely determine a 3D point. The inverse is a ray unless depth or another geometric constraint is supplied.
```

## Projection properties and their exceptions

The lecture says that lines project to lines and polyhedra project to polygons (PDF 108–109). The underlying reason is that a 3D line together with the camera center defines a plane; that plane intersects the image plane in an image line.

There is a degenerate case: a 3D line through the camera center projects to a single image point, wherever its visible projection is defined. A point at the camera center has no valid projection at all. Occlusion also determines which projected edges are visible. These qualifications prevent an ideal geometric statement from being mistaken for a guarantee about every photograph.

The “distant objects are smaller” example on PDF page 110 is about equal physical objects at different depths: their projected sizes vary inversely with depth under the same camera. Changing focal length at the same time changes that comparison.

## Separate camera intrinsics from camera pose

**Intrinsics** turn normalized camera coordinates into pixel coordinates. **Extrinsics** turn world coordinates into camera coordinates. They answer different questions and have different units.

````{formula-box} Formula — calibrated pixel projection
```{math}
:label: eq-lec01-camera
\begin{aligned}
K&=\begin{pmatrix}f_x&s&c_x\\0&f_y&c_y\\0&0&1\end{pmatrix},\qquad
P=K\begin{pmatrix}R&t\end{pmatrix},\\
\lambda\begin{pmatrix}u\\v\\1\end{pmatrix}
&=PX_w,\qquad X_c=RX_{w,\mathrm{E}}+t,\qquad C=-R^Tt.
\end{aligned}
```

$K$ is $3\times3$; $f_x,f_y$ and skew $s$ are in pixels, and $(c_x,c_y)$ is the **{term}`principal point <Principal point>`** in pixels. $X_w$ is a homogeneous $4\times1$ world point; $X_{w,\mathrm{E}}$ is its Euclidean $3\times1$ form. $R,t$ map world to camera, so $P$ is $3\times4$. $C$ is the camera center in world coordinates.

**Conditions:** ideal undistorted camera, finite valid point, and a declared world-to-camera convention. With a world point normalized to last coordinate one, this calibration gives $\lambda=Z_c$. $P$ is defined up to nonzero scale. A calibrated finite camera has rank three; its nullspace is the homogeneous camera center.
````

```{application} How to use it — world point to pixel
1. Compute $X_c=RX_{w,\mathrm{E}}+t$ and check $Z_c>0$.
2. Multiply by $K$, or multiply $PX_w$ directly.
3. Divide the first two output entries by the third.
4. Check image bounds separately: a point in front can still project outside the sensor.
5. Verify the center relation by $RC+t=0$.

See {ref}`Example 1.15 <ex-lec01-camera-motion>`.
```

Expanding the first two rows makes the meaning explicit:

$$u=f_xX_c/Z_c+sY_c/Z_c+c_x,\qquad v=f_yY_c/Z_c+c_y.$$

The offsets place the optical-axis intersection at $(c_x,c_y)$, not necessarily at image coordinate zero. Pixel focal length is a physical focal length divided by pixel pitch; different pixel scales can give different $f_x,f_y$. Detailed calibration and homography estimation follow in Lecture 3.

**Convention translation for PDF page 113:** the slide writes $K[R^T\mid -R^Tt]$ when $R,t$ describe the camera's pose in world coordinates. In our notation call those $R_{w\leftarrow c},C$. Then the world-to-camera map is $[R_{w\leftarrow c}^T\mid-R_{w\leftarrow c}^TC]$. It is the same geometry, expressed with a different meaning for the symbol $R$. The slide's “2-D to 3-D” description should not suggest that $P$ uniquely inverts projection: $P$ maps 3D homogeneous points to 2D homogeneous image points.

## Work the actual camera-motion exercise

PDF page 114 asks us to choose visible points for a camera with focal length 500 and a $500\times500$ image, move the camera forward by two units, and then consider rotating/translating points. The slide leaves the points, principal point, and precise sequencing open. We must declare them.

```{figure} ../../images/lecture01/camera-motion.*
:name: fig-lec01-camera-motion
:width: 90%
:alt: A stationary 3D point is viewed from two camera centers separated along the forward axis.

Move the camera, not the object: the world point stays fixed, but its camera-relative depth decreases. Original solution diagram for PDF page 114, printed slide 115.
```

(ex-lec01-camera-motion)=
```{worked-example} Worked example 1.15 — the lecture's camera-motion problem
**Source:** numerical solution adapted from PDF page 114. All values added to complete the setup are stated here.

Assume square pixels, zero skew, $f_x=f_y=500$ pixels, and principal point $(250,250)$. Initially the camera is at the world origin with $R=I$. Choose $X_w=(1,0.5,10)$ in an arbitrary consistent length unit. Its image is inside the $500\times500$ sensor.

1. Initially, $(u,v)=(250+500/10,250+250/10)=(300,275)$ pixels.
2. Move the camera center to $C'=(0,0,2)$ without rotating it. The stationary point now has camera coordinates $(1,0.5,8)$.
3. The new pixel is $(312.5,281.25)$. Its displacement from the principal point increases because the point is closer.
4. For a separate branch starting again from the original setup, rotate the **point** by $45^\circ$ about the camera's $z$ axis and then translate it five units farther along $z$.
5. The new point is $(0.5/\sqrt2,1.5/\sqrt2,15)$. Projection gives $(261.785,285.355)$ pixels after rounding.

If the operations were meant cumulatively after the camera move, the rotated/transformed point would have depth $8+5=13$ in that moved camera, giving approximately $(263.598,290.795)$ instead. A complete answer must specify the sequence.
```

For a general forward camera displacement $\Delta$, the normalized transverse displacement changes from $X_c/Z_c$ to $X_c/(Z_c-\Delta)$; visible points need $Z_c-\Delta>0$. A point on the optical axis does not move away from the principal point. Translating the object farther away instead gives denominator $Z_c+\Delta$ and moves its image inward. Camera motion and scene motion require inverse coordinate relationships, as PDF page 111 emphasizes.

(lec01-interactive)=
````{interactive-demo} projection
The 3D explorer lets you move the point, move or turn the camera, and change focal length. Drag empty space to inspect the scene from another angle; that changes your viewing position, not the teaching camera's pose. The calculation follows **world point → camera coordinates → image pixel**, using {eq}`eq-lec01-camera`. Turning the teaching camera by yaw $\alpha$ changes the world-to-camera rotation to $R_y(-\alpha)$ and the translation to $-RC$; the plane and camera axes turn with it.

```{figure} ../../images/lecture01/projection-explorer.*
:name: fig-lec01-interactive
:width: 100%
:alt: A perspective 3D view of the camera axes, virtual image rectangle, world point, and ray intersection q.

Initial 3D scene: the orange ray from $C$ through $P$ crosses the blue virtual image plane at $q$. Camera $+Y_c$ points down and $+Z_c$ points forward. This is a static view of the rotatable web scene; depth is encoded geometrically rather than by the page's horizontal distance.
```

**Connect the scene to the numbers:** the sensor uses $0.004$ world-length units per pixel, so $f=500$ px places the virtual plane at distance $f_{\rm plane}=2$. Its width and height are each $500(0.004)=2$ units. The ray meets it at $q=(2\cdot1/10,2\cdot0.5/10,2)=(0.2,0.1,2)$. Converting those plane coordinates to pixels gives $(u,v)=(250+0.2/0.004,250+0.1/0.004)=(300,275)$.

The table holds $P=(1,0.5,10)$ fixed. The image is $500\times500$ with principal point $(250,250)$; the camera has no rotation, $f_x=f_y=f$, and skew is zero. Moving the point in the web scene changes its camera coordinates before this same projection is applied.

**Predict, then compare:** moving the camera forward makes the projected point move away from the principal point. Increasing focal length does the same without changing depth. Can a point be in front of the camera yet outside the image?

| Camera $C_z$ | $f$ (px) | Depth | Pixel $(u,v)$ | Visibility |
| --- | --- | --- | --- | --- |
| 0 | 500 | 10 | $(300,275)$ | Inside |
| 2 | 500 | 8 | $(312.5,281.25)$ | Inside |
| 2 | 1000 | 8 | $(375,312.5)$ | Inside |
| 8.5 | 500 | 1.5 | $(583.333,416.667)$ | In front; off-image |
| 10 | 500 | 0 | No finite projection | Undefined |
| 12 | 500 | $-2$ | $(0,125)$ algebraically | Behind; not visible |

The off-image row answers the question: positive depth is necessary but does not ensure sensor visibility. At zero depth division fails; negative-depth coordinates do not describe a visible point in this model. Values are rounded to three decimals.
````

## A depth-map bridge to the assigned quiz

**Source:** Fall 2017 Quiz 9, problem 1, `cs532_f17_quiz9.pdf`, PDF page 1. The quiz asks how two depth maps can become one common-frame point cloud. This is a supplementary preview; depth estimation and fusion algorithms are beyond Lecture 1.

````{formula-box} Formula — axial-depth backprojection and frame conversion
```{math}
:label: eq-lec01-backproject
q=K^{-1}\begin{pmatrix}u\\v\\1\end{pmatrix},\qquad
X_c=\frac{Z_c}{q_3}q,\qquad
X_w=R^T(X_c-t).
```

$K$ is $3\times3$, $q,X_c,X_w,t$ are $3\times1$, and $Z_c$ is **{term}`axial depth <Axial depth>`** in the camera's forward direction. For the standard intrinsic matrix $q_3=1$. The final equation assumes $R,t$ map world to camera.

**Conditions:** known calibration and camera poses in a common metric frame, invertible $K$, valid positive depth, and distortion handled. If depth means Euclidean range $r$ along the ray, use $X_c=rq/\|q\|$ instead. Mixing range and axial depth produces incorrect geometry.
````

```{application} How to use it — turn depth maps into common-frame points
1. For each valid depth pixel, use that camera's calibration to recover a viewing direction.
2. Scale it according to the depth convention.
3. Transform the camera-coordinate point into the shared world frame.
4. Repeat for both cameras and combine the points. Combining does not automatically denoise or resolve occlusion.

See {ref}`Example 1.16 <ex-lec01-depth>`.
```

**Worked example 1.16 — Fall 2017 Quiz 9, problem 1: preview solution.** {ref}`Read the original problem and every worked step <quiz-18-q1>`.

```{figure} ../../images/lecture01/depth-rays.*
:name: fig-lec01-depth-rays
:width: 70%
:alt: Two camera centers at 0 and 2 on the world x axis view the same point at x 1 and depth 10.

Both backprojected points coincide after conversion to world coordinates. Original schematic for Fall 2017 Quiz 9, problem 1; the optical-axis depth and coordinates come from Example 1.16.
```

```{understanding-check} Check 1.7 — is an off-image point behind the camera?
A point has positive camera depth but projects to $u=700$ in a 500-pixel-wide image. Which condition failed?
```

```{admonition} Solution
:class: dropdown
It is in front of the camera but outside the image bounds. Positive depth and sensor visibility are separate tests. A valid homogeneous projection alone does not establish that the camera actually measured the point.
```

```{index} pinhole camera
```

```{index} perspective projection
```

```{index} intrinsic parameters
```

```{index} extrinsic parameters
```

```{index} principal point
```

```{index} backprojection
```

```{index} axial depth
```
