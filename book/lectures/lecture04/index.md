(lecture04)=
# Lecture 4: Epipolar geometry and stereo depth

**[Original quiz questions + fully worked solutions](quiz-workbook.md)** — complete problem statements, numbered red steps with a plain-English reason, and blue mathematics showing intermediate operations.


**A one-pixel mistake can move a reconstructed point by centimeters—or much more. Why?** Two views turn image matches into 3D geometry, but the result depends on finding the right match and measuring its position accurately.

**Start here:** [Epipolar geometry, explained visually with worked math](epipolar-practice.md). Learn why a pixel predicts a line, then calculate the line, test matches, reverse the mapping, find epipoles, and solve the assigned quizzes step by step.

**Looking for stereo errors?** Go to {ref}`depth sensitivity and signed errors <stereo-depth-sensitivity>`, including both quiz sets, exact versus approximate answers, and why distant points are harder to measure. The {ref}`3D stereo explorer <stereo-explorer>` connects the equations to actual camera rays.

## Find the worked math quickly

| I want to… | Go straight to… |
| --- | --- |
| Understand what an epipolar line means | {ref}`Ray → plane → line <epipolar-ray-plane>` |
| Multiply F by a point, one row at a time | {ref}`Guided calculation A <epipolar-point-line>` |
| Test several matches and measure a miss | {ref}`Guided calculation B <epipolar-test-match>` |
| Use the transpose or solve for epipoles | {ref}`Guided calculation C <epipolar-reverse>` |
| Expand the symbolic Quiz 4 constraint | {ref}`Worked example 4.1 <ex-lec04-symbolic>` |
| Intersect third-view epipolar lines | {ref}`Worked example 4.2 <ex-lec04-third-view>` |
| Correct the supplied Quiz 2 matrix answer | {ref}`Worked example 4.3 <ex-lec04-invalid-f>` |
| Calculate ±1-pixel depth errors | {ref}`Fall quiz 4.6 <ex-lec04-stereo-fall>` and {ref}`Spring quiz 4.7 <ex-lec04-stereo-spring>` |
| Set a disparity search range | {ref}`Worked example 4.8 <ex-lec04-search>` |

## Reading route

1. [Understand epipolar geometry and solve its quizzes](epipolar-practice.md): visual intuition, fully expanded linear algebra, and checked answers.
2. [Estimate F from noisy matches](estimation.md): enforce rank two and measure error in pixels.
3. [Recover camera pose](essential.md): use calibration, decompose the essential matrix, and test which solution faces the scene.
4. [Stereo depth and its errors](stereo.md): derive the depth equation, solve both quiz sets, and explore the geometry in 3D.
5. [Find matches across an image](matching.md): compare patches, aggregate evidence, and handle depth boundaries.
6. [Review and source checklist](review.md), then the final [TLDR and answered quiz](tldr.md).

**Source:** `wk4_cs532s26_TwoViewGeometry.pdf`, 77 PDF pages. Printed numbers match PDF pages 1–34; from PDF page 35 onward, visible printed numbers are four greater. PDF page 54 has no visible number. References below use one-based **PDF pages**. The coverage register records repeated material and its original teaching location.
