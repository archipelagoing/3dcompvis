(lecture02)=
# Lecture 2: Projective geometry and image warping

**[Original quiz questions + fully worked solutions](quiz-workbook.md)** — complete problem statements, numbered red steps with a plain-English reason, and blue mathematics showing intermediate operations.


**How can a tilted photograph become a view from above?** The basketball-court task turns geometry into a practical tool: find a mapping, then use it to create a new image.

This chapter teaches the material added beyond Lecture 1: quaternion conversions and interpolation, planar rectification, image sampling, robust estimation, lens correction, and two-view constraints.

**Prerequisites:** [Lecture 1](../lecture01/index.md) owns homogeneous geometry, transformation families, rotations, frames, and camera projection. The source slides repeat those topics; the textbook links to their original explanations. Spring 2020 Quiz 1 remains attributed to Lecture 2 in the [quiz index](../../reference/quiz-index.md), with its foundation solutions collected in [Lecture 1](../lecture01/quiz-practice.md).

## Reading route

1. [Quaternion conversions](quaternions.md): convert rotation descriptions and interpolate orientations.
2. [Homographies](homographies.md): straighten a photographed plane and calculate cross-ratios.
3. [Image warping](warping.md): sample the source image to fill a destination grid.
4. [Estimate a reliable mapping](estimation.md): DLT, normalization, and RANSAC.
5. [Distortion and two-view geometry](two-view.md): handle lens bending and constrain matches across views.
6. [Review and formula checklist](review.md), then the final [TLDR and short quiz](tldr.md).

**Source:** `cs532_f25_Week2.pdf`, 129 PDF pages. Printed labels equal PDF pages through page 43; pages 44–49 have no visible label; from PDF page 50 onward, printed labels are one greater. Notes below use **PDF pages** unless stated otherwise. The authoring coverage register records which repeated slides are already covered in Lecture 1.
