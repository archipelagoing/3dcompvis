(lec06-ambiguity)=
# What can the photographs actually determine?

**A good-looking reconstruction can still have the wrong scale.** Photographs measure directions to points. Without a known length, a miniature scene close to the cameras can look identical to a large scene farther away.

**Source:** PDF pages 4–19. Worked exam companions: {ref}`reconstruction upgrades, Fall 2025 Quiz 5 <quiz-12-q1>` and {ref}`its second scenario <quiz-12-q2>`.

```{figure} ../../images/lecture06/tracks.*
:name: fig-lec06-tracks
:width: 95%
:alt: Corresponding facade features are connected across three photographs.

The source facade tracks, PDF page 5. Each track should represent one physical 3D point observed in several images. Attribution follows the lecture deck; original image creator is not individually identified.
```

## Count measurements, then count unknowns

Each observed image point supplies two coordinates. A calibrated camera has six pose parameters; each 3D point has three. But an arbitrary common translation, rotation, and scale changes no image. Those seven free choices are the **similarity gauge**.

````{formula-box} Formula — necessary measurement counts
```{math}
:label: eq-lec06-counts
\begin{aligned}
\text{Calibrated:}\quad&2mn\ge 6m+3n-7,\\
\text{Projective:}\quad&2mn\ge 11m+3n-15,\\
\text{Affine:}\quad&2mn\ge 8m+3n-12.
\end{aligned}
```

$m$ is the number of views and $n$ the number of points, assuming every point is visible in every view and generic geometry. A projective camera has 11 parameters up to scale; an affine camera has 8. The gauge freedoms have dimensions 15 and 12 respectively. These inequalities are **necessary counts, not sufficient guarantees of a unique or stable solution**. Missing observations reduce the left side to twice the number actually observed.
````

```{application} Use a count without overclaiming
1. Identify the camera model and count actual observations.
2. Subtract the appropriate common gauge from the unknowns.
3. Check the inequality. Failure means insufficient data; success means only that the count permits a solution.
4. Check configuration, ambiguity, outliers, and numerical conditioning separately.
```

For two calibrated views, $4n\ge12+3n-7$ gives $n\ge5$. For two projective views, $4n\ge22+3n-15$ gives $n\ge7$. These explain the minimal counts behind five-point and seven-point methods; they do not remove their multiple candidate solutions.

## Why a different 3D shape can produce the same images

````{formula-box} Formula — projective reconstruction ambiguity
```{math}
:label: eq-lec06-gauge
x_{ij}\sim P_iX_j
=(P_iH^{-1})(HX_j),\qquad \det H\ne0.
```

$X_j$ is a homogeneous $4\times1$ point, $P_i$ a $3\times4$ camera, and $H$ one common invertible $4\times4$ projective transformation. Transforming all points and compensating every camera preserves their image projections. Arbitrary $H$ need not preserve lengths, angles, parallelism, or calibration.
````

```{application} Check a claimed reconstruction upgrade
1. State what was recovered: projective, affine, or metric geometry.
2. State the extra information: parallel directions, orthogonality, calibration, or known lengths.
3. Use it to constrain the allowable common transformation.
4. Report the ambiguity that remains. A metric reconstruction usually still has arbitrary common rotation, translation, and scale.
```

```{figure} ../../images/lecture06/house-ambiguity.*
:name: fig-lec06-house
:width: 95%
:alt: The lecture's house reconstructions show projective, affine, and similarity ambiguity.

Selected house reconstructions from PDF pages 15, 17, and 19. Different reconstruction classes preserve different geometric properties. These are source examples, not three stages computed by this book.
```

**A concrete scale example:** replace every Euclidean point $X$ and camera center $C_i$ by $2X$ and $2C_i$, leaving rotations unchanged. Camera coordinates become $R_i(2X-2C_i)=2R_i(X-C_i)$. Dividing by depth cancels the factor two. Merely multiplying a homogeneous point vector by two describes the *same* point and is not this physical change of scale.

## What the upgrades add

A projective reconstruction has not located the **plane at infinity** correctly. Establishing that plane gives an affine reconstruction, where parallel lines remain parallel. Recovering the metric additionally constrains angles and relative lengths, commonly through calibration or sufficient orthogonality constraints.

A known length fixes global scale after a metric reconstruction. One right angle alone generally does not determine an entire metric upgrade. Use the independent constraints and assumptions in the specific question; the two Fall 2025 scenarios are worked separately in the workbook.

```{index} Gauge freedom
```
```{index} Projective reconstruction ambiguity
```
