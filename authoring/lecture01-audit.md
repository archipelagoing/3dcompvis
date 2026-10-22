# Lecture 1 source audit and example selections

All 114 PDF pages of `wk1_2_cs532s26_IntroToGeometry.pdf` were extracted and visually inspected in rendered contact sheets; image-only mathematical slides were also read visually. A larger render of PDF page 92 verified quaternion conventions. Embedded source images were inspected before selection. The chapter consolidates repeated visual builds instead of repeating every slide.

## Source labels

Printed labels match PDF page numbers through page 24; from PDF page 25 onward the deck generally uses PDF page plus one. Page 86's image-only line slide has no visible/extractable slide label; page 49's embedded output does not supply a reliable extracted label. Cite these by PDF page. The coverage ledger records exceptions rather than inventing printed references.

## Selected slide examples

| Actual source example | Why use it | Textbook treatment |
| --- | --- | --- |
| Internet as camera; Colosseum workflow, PDF 2–26 | Connects each geometric tool to a reconstruction task | Opening narrative and an original pipeline diagram |
| Ambiguous images/projection, PDF 30–42 | Explains why inference needs models and assumptions | Plain-language appearance/depth discussion and original viewing-ray diagram |
| Fountain image/depth sequence, PDF 50–51 | Real imagery connects image measurements to geometric output | Two embedded source image assets, with unknown individual creators stated |
| Railway and ideal points, PDF 68–71 | Distinguishes ideal world directions from finite image vanishing points | Source photograph, original schematic, and numerical line intersections |
| Rotation about a chosen center, PDF 77 | Makes composition order tangible | Explicit pivot subtraction/rotation/restoration and worked numbers |
| Quarter-turn vector, PDF 89 | Supplies an immediate sign/axis sanity check | Original numbers retained in the rotation explanation |
| Fixed/body axis sequences, PDF 93–100 | Exposes convention and noncommutativity pitfalls | Ordered products, expanded matrix, and original branching vector diagram |
| Hands-on camera motion, PDF 114 | Combines frames, calibration, and projection | Worked numerical solution with declared principal point, point, and independent/cumulative branches |

## Scope and consolidation

The first lecture already contains core geometry, quaternion operations, line/plane duality, and camera projection. They are covered here. Lecture 2 will cross-reference this material and add its expanded rotation/warping/estimation content. The epipolar and disparity formulas embedded in workflow previews on PDF pages 25–26 are explicitly assigned to Lecture 4's full treatment. Circular points and the absolute conic in the hierarchy figures receive definitions as vocabulary previews for metric reconstruction in Lecture 6.

Administrative policies/logistics on PDF 7–8 are excluded. The reading list on 9–10 is preserved as source context. Video-title slides are summarized as applications; no unavailable video content is invented.

## Assigned quizzes and checks

Fall 2025 Quiz 1 Q3–Q4 is fully developed with frame-direction, scale/time, and noncollinearity qualifications. Its probability Q1–Q2 remain pending for Lecture 3. Fall 2017 Quiz 9 P2(a–b) is solved using outward unit normals and active positive-z rotation. P1 receives a supplementary backprojection/common-frame solution after the camera prerequisites, with fuller calibration/fusion work deferred.

`lecture01-formulas.csv` maps labeled equations to source pages or marked supplements. `scripts/check_lecture01_math.py` independently verifies numerical intersections, nullspaces/cofactors, closest-line distance, rotations/quaternions, frame composition, quiz normals, projection, and backprojection. It uses alternative constructions where feasible, including rotated-vertex normal checks and least-squares closest points.

Review the completed HTML/PDF artifacts before progressing to Lecture 2. This source audit does not claim the later chapters are written.
