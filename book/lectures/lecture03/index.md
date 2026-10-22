(lecture03)=
# Lecture 3: Put camera geometry to work

**[Original quiz questions + fully worked solutions](quiz-workbook.md)** — complete problem statements, numbered red steps with a plain-English reason, and blue mathematics showing intermediate operations.


**Can you turn an image size into a camera matrix, or a pixel into a 3D point?** This chapter puts the earlier geometry to work on the assigned quizzes, then shows why even thousands of random trials cannot resolve an ambiguous match.

The Lecture 3 deck repeats theory already taught in Lectures 1–2. Those explanations keep their original homes. Here we add **new applications**, a complete projective calculation, and a sampling experiment.

## Reading route

1. [Calibration from field of view](calibration.md): solve the camera quiz and keep pixels separate from physical lengths.
2. [Find depth on a known plane](ray-plane.md): intersect a viewing ray with geometry you know.
3. [A complete projective DLT calculation](homography-practice.md): normalize, solve, undo normalization, and check a new point.
4. [Probability and the pentagon puzzle](probability-ransac.md): count matches, choose a trial budget, and experiment with RANSAC sampling.
5. [Review and source checklist](review.md), then the final [TLDR and short quiz](tldr.md).

**Prerequisites:** [camera projection](../lecture01/cameras.md), [homographies](../lecture02/homographies.md), [image warping](../lecture02/warping.md), and [DLT and RANSAC](../lecture02/estimation.md).

**Source:** `wk3_cs532s26_ImageFormation+Homographies-1.pdf`, 80 PDF pages. Visible printed slide numbers match PDF page numbers on pages 2–80; the title page is unnumbered. References below use one-based **PDF pages**. Its pages 2–80 repeat Lecture 2's PDF pages 51–129. The coverage register maps every page to its teaching location.
