(glossary)=
# Glossary

Terms are added as their explanations are written. First-use definitions, glossary terms, and PDF index entries share stable references.

```{glossary}
Homogeneous coordinates
  Coordinates representing a projective point by a nonzero vector up to nonzero scale. See {ref}`notation` and {eq}`eq-homogeneous-scale` for the definition and comparison procedure.

Coordinate frame
  A reference origin and axes used to express coordinates. Transform directions are specified in {ref}`notation`; detailed geometry is developed in {ref}`lec01-frames`.
```

```{glossary}
Computer vision
  Inferring scene properties from images. See {ref}`lec01-motivation` for the inverse-problem viewpoint.

Structure from motion
  Joint recovery of camera motion and scene structure from corresponding image measurements. See {ref}`lec01-motivation`; full estimation follows in Lecture 6.

Depth map
  An image-indexed array of depth measurements or estimates. Its depth convention and camera model must be specified. See {ref}`lec01-cameras`.

Point cloud
  A collection of 3D point positions, often expressed in one common frame. See {ref}`Example 1.16 <ex-lec01-depth>`.

Projective plane
  Nonzero 3-vectors identified under nonzero scale, representing finite and ideal 2D points. See {ref}`lec01-projective`.

Incidence
  A point lying on a line or plane, tested through a zero dot product of homogeneous coordinates and coefficients. See {eq}`eq-lec01-incidence`.

Ideal point
  A projective point with last homogeneous coordinate zero; also called a point at infinity. See {eq}`eq-lec01-ideal`.

Line at infinity
  The projective line containing all ideal points of a plane. See {ref}`lec01-projective`.

Vanishing point
  An image location corresponding to a scene direction, often where projected parallel scene lines intersect. It need not be an ideal point of the image plane. See {ref}`lec01-projective`.

Horizon
  The image of a scene plane's line at infinity. See {ref}`lec01-projective`.

Degrees of freedom
  The number of independent continuous parameters. Matrix entries can be constrained or equivalent under scale. See {eq}`eq-lec01-hierarchy` and {ref}`lec01-rotations`.

Nullspace
  The vectors mapped to zero by a matrix. Homogeneous geometry seeks a nonzero solution, often unique up to scale. See {eq}`eq-lec01-plane-null`.

Plücker coordinates
  A homogeneous representation of a spatial line; for a finite line the direction/moment pair is $(d,p\times d)$ with $d^Tm=0$. See {eq}`eq-lec01-plucker`.

Reciprocal product
  A scalar formed from two valid direction/moment line representations; it tests their coplanarity and supports a shortest-distance formula. See {eq}`eq-lec01-line-distance`.

Surface normal
  A direction perpendicular to local surface tangent directions. An oriented face normal requires a winding or outward convention. See {ref}`Example 1.12 <ex-lec01-tetrahedron>`.

Rotation matrix
  A real orthogonal matrix with determinant $+1$ representing a proper rotation. See {eq}`eq-lec01-orthogonal`.

Axis–angle
  A rotation representation consisting of a unit axis and an angle. Extraction needs special handling near zero and a half-turn. See {eq}`eq-lec01-axis-angle`.

Quaternion
  A scalar–vector algebraic object; unit quaternions represent rotations under a declared multiplication and active/passive convention. See {eq}`eq-lec01-quaternion`.

Intrinsic rotation
  A rotation about an axis attached to the moving body. It is unrelated to camera intrinsic calibration despite the shared word. See {eq}`eq-lec01-ordered-angles`.

Extrinsic rotation
  A rotation about a fixed reference axis. See {eq}`eq-lec01-ordered-angles`.

Gimbal lock
  A singular three-angle description in which independent parameter effects coincide. The physical orientation still exists. See {ref}`lec01-rotations`.

Rigid transformation
  A proper rotation and translation preserving distances and angles. See {eq}`eq-lec01-rigid3`.

Circular points
  Two complex ideal points shared by all Euclidean circles in a plane, encoding metric structure projectively. These are a vocabulary preview in {ref}`lec01-transformations`.

Absolute conic
  A complex conic on the plane at infinity encoding the 3D Euclidean metric. Its role in metric upgrades is deferred to Lecture 6; see {ref}`lec01-frames` for the hierarchy context.

Pinhole camera
  An ideal central-projection model in which rays pass through one camera center. See {eq}`eq-lec01-pinhole`.

Principal point
  The pixel location where the optical axis intersects the ideal image plane. It is not automatically the pixel origin. See {eq}`eq-lec01-camera`.

Intrinsic parameters
  Camera calibration parameters that map normalized camera coordinates to pixels, including focal entries, skew, and principal point. See {eq}`eq-lec01-camera`.

Extrinsic parameters
  Rotation and translation linking world and camera frames, with a declared transform direction. See {ref}`lec01-cameras`.

Backprojection
  Mapping a pixel to a camera ray, then using specified depth to recover a 3D point. See {eq}`eq-lec01-backproject`.

Axial depth
  The point's coordinate along the camera's forward axis; it differs from Euclidean range along the ray. See {eq}`eq-lec01-backproject`.
```
