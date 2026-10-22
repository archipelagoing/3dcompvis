(lec01-motivation)=
# Why reconstruct a world from photographs?

Imagine collecting photographs of the same building from people who never met. They used different cameras, stood in different places, and photographed it at different times. Could those disconnected pictures become one 3D model?

That is the opening challenge of Lecture 1: **“the Internet as a camera.”** Here the phrase describes a collection of viewpoints, not one physical camera or a claim that arbitrary pictures can always be reconstructed. The reconstruction must discover which images overlap, which pixels refer to the same scene features, and where the cameras were.

**Lecture source:** `wk1_2_cs532s26_IntroToGeometry.pdf`, PDF pages 2–61. Printed slide labels match PDF pages through page 24; from PDF page 25 onward labels are offset by one. The application descriptions below summarize the supplied lecture, not the current state of a research project.

## Work backward from an image

**{term}`Computer vision`** infers properties of a scene from measured images. Computer graphics usually starts with scene geometry, materials, lighting, and a viewpoint to produce an image. Vision faces the inverse question: given the image, what could have produced it?

This distinction matters because the inverse need not be unique. A small nearby object and a larger distant object may occupy the same pixels. Surface color and illumination can also trade off: a dark pixel might belong to a dark material or a shadow. The ambiguous figures and lighting illusions on PDF pages 30–42 are reminders that an image is evidence, not a complete description of the world.

```{figure} ../../images/lecture01/ambiguity.*
:name: fig-lec01-ambiguity
:width: 75%
:alt: Two 3D points at different depths lie on the same ray through a camera and image point.

One image point specifies a viewing ray, not a unique depth. Original diagram explaining the projection ambiguity illustrated on Lecture 1 PDF pages 37 and 105–107.
```

The picture gives us a useful distinction between **geometric information**—positions, shapes, and camera motion—and **semantic information**, such as whether a region depicts a building or vegetation. Both can help a vision system, but this book concentrates on geometry. A geometric reconstruction can have accurate surface positions without knowing the names of the objects.

```{index} computer vision; inverse problem
```

```{index} geometric reconstruction
```

```{index} semantic information
```

## A reconstruction is a chain of linked problems

The Colosseum sequence on PDF pages 19–24 motivates the following pipeline. The arrows are logical dependencies; practical systems may revisit earlier stages.

```{figure} ../../images/lecture01/pipeline.*
:name: fig-lec01-pipeline
:width: 100%
:alt: Photographs lead to feature association, camera registration, dense depth, and surface representation.

From independent photographs to a geometric representation. Original redrawing of the lecture's reconstruction workflow, PDF pages 18–26. The underlying lecture figures use the Colosseum as an example.
```

1. **Associate:** identify measurements of the same scene feature across images. A similar-looking window is not automatically the same physical window.
2. **Register:** estimate camera positions/orientations and a sparse set of 3D points. **Structure from motion (SfM)** estimates scene structure and camera motion together from image correspondences.
3. **Estimate dense depth:** recover geometry for many pixels, not just a few distinctive corners.
4. **Represent:** organize the recovered geometry as a point cloud, surface, or another useful model. Dense depth, point-cloud fusion, and meshes are previews here; their full algorithms lie beyond these six lectures.

A **{term}`depth map <Depth map>`** stores a depth value at each valid image location. A **{term}`point cloud <Point cloud>`** stores 3D point positions. They are different representations: a depth map still depends on its camera coordinates; a point cloud can express all points in one common frame.

## Follow the fountain from pixels toward shape

PDF pages 50–51 show photographs, depth estimates, fusion, and colored geometry of a fountain. This is particularly useful because its decorative details are visible in both the photograph and geometric output.

```{figure} ../../images/lecture01/fountain-input.png
:name: fig-lec01-fountain-photo
:width: 62%
:alt: Photograph of a red stone fountain with a carved central ornament and projecting basin.

An input view from the fountain example, extracted from Lecture 1 PDF page 50, printed slide 51. Source: supplied Enrique Dunn lecture deck; the original photograph's creator is not identified on that slide.
```

```{figure} ../../images/lecture01/fountain-depth.png
:name: fig-lec01-fountain-depth
:width: 62%
:alt: Grayscale depth output of the fountain, showing its shape, basin, and missing or noisy background regions.

A depth output from the same example, extracted from PDF page 51, printed slide 52. The slide compares raw and fused estimates. Grayscale is an encoding of the source's depth data; its numerical scale is not specified, so do not infer metric depths from brightness alone. Source: supplied lecture deck; original figure creator not specified there.
```

Notice three things. First, matching must identify the same ornament or basin location in different views. Second, a depth estimate is a geometric hypothesis and can contain holes, noise, or mistakes near occlusion boundaries. Third, fusion must place estimates in a common reference frame; simply stacking pixel arrays would not align their 3D points.

The slides also show urban capture in Chapel Hill (PDF 47–49), large photo-collection reconstructions (52–54), visual SLAM (55), dynamic reconstruction (56), and remote sensing, autonomous systems, augmented reality, and geolocalization (57–61). These illustrate different data conditions, not extra algorithms to memorize in Lecture 1. **Visual SLAM** emphasizes estimating a moving camera's pose while building a map. A dynamic scene introduces an additional challenge: the same object may move between images.

## Why the geometry is difficult

The lecture's examples identify several different obstacles:

- **Projection loses depth:** many 3D points can lie on one image ray.
- **Appearance is not geometry:** shadows, reflections, materials, and exposure change pixel intensities.
- **Measurements are imperfect:** noise, quantization, blur, occlusion, and camera-model errors affect the observations.
- **Association is ambiguous:** repeated textures and locally similar patches can produce incorrect matches.
- **More data creates more work:** a large photo collection can improve coverage but also increases matching and optimization costs.

The answer is not to abandon images. It is to state the model and assumptions clearly, use multiple sources of evidence, and check the resulting estimates.

```{understanding-check} Check 1.1 — is a correspondence already a 3D point?
Two images contain matching pixels on the same fountain ornament. Do those two pixel coordinates alone provide its position in meters?
```

```{admonition} Solution
:class: dropdown
No. We still need suitable camera geometry and a scale reference for metric units. Matching establishes data association. Reconstruction uses the image measurements and cameras to infer geometry. Even a valid monocular reconstruction generally has an unknown global scale unless additional information fixes it.
```

## What to remember

The rest of Lecture 1 builds the language needed to describe this pipeline: homogeneous points and lines, transformations, planes, rotations, reference frames, and camera projection. The goal is to understand how a calculation relates to a geometric question, not to mistake a visually convincing output for a verified reconstruction.
