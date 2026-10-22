(lecture04)=
# Lecture 4: Two views reveal depth

**A one-pixel mistake can move a reconstructed point by centimeters—or much more. Why?** Two views turn image matches into 3D geometry, but the result depends on finding the right match and measuring its position accurately.

This chapter adds the assigned epipolar quizzes, noisy matrix estimation, calibrated pose recovery, stereo depth/error calculations, and dense matching. The [two-view introduction](../lecture02/two-view.md) already owns distortion correction, epipoles, the fundamental constraint, and rectification; use those explanations as prerequisites.

## Reading route

1. [Solve the epipolar quizzes](epipolar-practice.md): expand a constraint, intersect two predicted lines, and check a supplied matrix.
2. [Estimate F from noisy matches](estimation.md): enforce rank two and measure error in pixels.
3. [Recover camera pose](essential.md): use calibration, decompose the essential matrix, and test which solution faces the scene.
4. [Stereo depth and its errors](stereo.md): derive the depth equation, solve both quiz sets, and explore the geometry in 3D.
5. [Find matches across an image](matching.md): compare patches, aggregate evidence, and handle depth boundaries.
6. [Review and source checklist](review.md), then the final [TLDR and answered quiz](tldr.md).

**Source:** `wk4_cs532s26_TwoViewGeometry.pdf`, 77 PDF pages. Printed numbers match PDF pages 1–34; from PDF page 35 onward, visible printed numbers are four greater. PDF page 54 has no visible number. References below use one-based **PDF pages**. The coverage register records repeated material and its original teaching location.
