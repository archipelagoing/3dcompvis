(lecture01)=
# Lecture 1: Foundations and 3D geometry

Can photographs taken from different viewpoints reveal a shared 3D world? Lecture 1 introduces that problem and builds the geometric language used to solve it.

This chapter follows the actual supplied deck, including its early introduction to camera projection. Later lectures revisit these foundations and develop their estimation algorithms. Read the sections in order; use the final checklist to return to a specific formula or quiz example.

**What you will learn**

- Explain why a pixel alone does not determine scene depth.
- Join points, intersect lines, and recognize ideal points in homogeneous coordinates.
- Distinguish point transformations from line/plane transformations.
- Construct planes and spatial lines, and recognize degenerate inputs.
- Apply and compare rotation matrices, ordered angles, axis–angle, and quaternions.
- Compose rigid frame transforms with explicit directions.
- Project a world point into a camera and reason about camera motion.

**Reading route**

1. [Why reconstruct a world from photographs?](motivation.md)
2. [Points, lines, and infinity](projective.md)
3. [2D transformations and invariants](transformations.md)
4. [Planes and lines in 3D](planes-lines.md)
5. [Rotation representations](rotations.md)
6. [Frames and integrated quiz problems](frames-quizzes.md)
7. [Camera projection and the hands-on exercise](cameras.md)
8. [Review and source-coverage checklist](review.md)

**How the quizzes fit**

Fall 2025 Quiz 1, questions 3–4, develops relative camera pose and a camera/object plane. Fall 2017 Quiz 9 supplies the tetrahedron normals/rotation problem and a supplementary depth-backprojection bridge. The supplied lecture mapping classifies both quiz sets as supplementary; the core geometric ideas are still prerequisites for the higher-priority camera and two-view topics.

**Source:** `wk1_2_cs532s26_IntroToGeometry.pdf`, all 114 PDF pages audited. Repeated visual builds are consolidated. Course logistics are excluded from the mathematics; research applications are summarized rather than treated as extra algorithms. Geometry slide sections credit M. Pollefeys and D. Cappelleri; image-formation sections credit John Oliensis. All newly added numerical values and diagrams are labeled as original or adapted.
