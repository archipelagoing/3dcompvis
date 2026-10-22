(lecture06)=
# Lecture 6: Reconstruct a scene—and improve it

**The goal:** turn tracks across photographs into camera poses and 3D points. Then adjust both until their projections agree with the measurements.

Read [what reconstruction cannot determine](ambiguity.md), [affine factorization](factorization.md), [triangulation](triangulation.md), [the multi-view pipeline](pipeline.md), and [bundle adjustment](optimization.md). Finish with the [complete quiz workbook](quiz-workbook.md), [formula and source map](review.md), and [TLDR + short quiz](tldr.md).

**Source:** all 72 PDF pages of `wk6_cs532s24_SFM1.pdf`, Enrique Dunn. The deck credits Szeliski, Seitz, Snavely, Lazebnik, Hebert, and Choudhary. Page references below are one-based PDF pages. Repeated titles and repeated optimization slides are consolidated.

We use Lecture 4's camera and epipolar geometry rather than teach it again. This chapter adds reconstruction ambiguity, many-view estimation, factorization, and optimization. Exactly one interactive appears at the point where a numerical update becomes a visible 3D improvement.
