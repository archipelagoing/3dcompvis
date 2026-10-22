(lecture05)=
# Lecture 5: Find points you can track

**Which part of a picture can you recognize after the camera moves?** A plain wall gives no location cue. An edge gives only one direction. A corner can constrain both. This chapter turns that observation into a detector, a tracker, and a matching procedure.

**[Original quiz questions and fully worked solutions](quiz-workbook.md)** include Spring 2019 Quiz 6, Fall 2025 Quiz 4, and the numerical Harris/Lucas–Kanade booklet problems. Every original question has red numbered steps, a short reason, and blue mathematical workings.

## Reading route

1. [Find distinctive features](features.md): the mountain panorama and Mars Rover matches.
2. [Understand Harris corners](corners.md): shifted windows → gradients → a 2×2 matrix → eigenvalues → selected corners. Includes the 3D error-surface explorer.
3. [Track with Lucas–Kanade](tracking.md): build and solve the patch equations, then handle large motion, drift, and exposure changes.
4. [Describe and match features](descriptors.md): BRIEF, ORB, BRISK, Hamming distance, ratio tests, and measured matching quality.
5. [Full quiz workbook](quiz-workbook.md), [formula/source checklist](review.md), and final [TLDR with answered quiz](tldr.md).

**Source:** `wk5_cs532_Corners.pdf`, 91 PDF pages. References use one-based PDF pages; visible page labels match them where printed. Early unnumbered slides are identified by their PDF positions. Source illustrations retain their credits in captions and the figure register. The chapter develops new feature-selection/tracking mathematics; Lecture 4 remains the reference for patch costs and stereo geometry.
