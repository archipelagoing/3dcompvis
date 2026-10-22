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

**Worked example 3.1 — the 640 × 480 camera.** {ref}`Read the original problem and every worked step <quiz-10-q1>`.

## A principal point has several descriptions

The **principal point** is where the optical axis meets the image plane. Its pixel coordinates, normalized coordinates, and physical 3D position describe related things in different units.

**Worked example 3.2 — finish the calibration quiz.** {ref}`Read the original problem and every worked step <quiz-10-q3>`.

```{understanding-check} Retest without duplicating the lesson
Use Spring 2020 Quiz 3 as a closed-notes retest. Answer all four problems, then check Examples 3.1–3.2. Before writing any coordinate, label it **pixel**, **normalized**, or **physical 3D**.
```
