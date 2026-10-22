# Lecture 1–2 ownership and duplicate-content audit

The supplied decks overlap substantially. The textbook follows the user's later requirement: teach a concept once, then add only new material. Source-deck coverage and original quiz assignments remain traceable independently of teaching placement.

| Shared topic | Sole teaching location | Change in Lecture 2 |
| --- | --- | --- |
| Homogeneous coordinates, incidence, ideal points, joins/intersections | L1 projective geometry | Removed review exposition and foundation TLDR/quiz questions; prerequisite link only |
| Collinearity test and repeated-point distinction | L1 foundation quiz practice | Moved the distinct assigned quiz solution and canonical formula here |
| 2D/3D transformation hierarchy, DOF, invariants, dual transforms | L1 transformations/frames | Removed duplicate table and invariance explanations; retained only new directional-scale factorization and explicit cross-ratio calculation |
| Planes, nullspaces/cofactors, Plücker lines/distance | L1 points/planes/lines | Removed the repeated review table; coverage ledger points to L1 |
| Elementary rotations, ordered axes, axis–angle, rigid inverse | L1 rotations/frames | Prerequisite link; no repeated derivation or summary items |
| Quaternion definition, Hamilton product, active convention, sign equivalence | L1 rotations | Removed repeated definition/sign-equivalence teaching; reference to canonical convention |
| Basic quaternion quarter-turn | L1 example 1.9 | Replaced L2's repeated numerical case with a 120-degree cyclic-axis conversion/round-trip example plus a half-turn branch |
| Camera dimensions, projection fractions, depth and motion | L1 cameras/foundation quiz practice | Moved all Spring 2020 Quiz 1 solutions into L1; removed these topics from L2's TLDR and end quiz |

## Lecture 2 additions retained

Quaternion/matrix conversions and stable branch handling; SLERP; explicit image-plane homography application and court rectification; directional affine scaling; cross-ratio computation; forward/inverse resampling and bilinear interpolation; homography DLT, noise and normalized coordinates; RANSAC and matching/refinement; radial correction; epipolar geometry, camera-derived/estimated F and rectification.

Lecture 1 mentions some later tools as workflow names or vocabulary previews. Such mentions are not second derivations or parallel teaching sections. Later applications may use prior formulas, but should link to their canonical explanation. Within-chapter TLDRs intentionally summarize only their own chapter's additions.

## Quiz and reference integrity

Spring 2020 Quiz 1 retains primary_lecture=2 in `quiz-index.csv` because this is its source assignment. Its unique worked solutions are now Examples 1.17–1.19 in `book/lectures/lecture01/quiz-practice.md`. Original stable `ex-lec02-*`, `eq-lec02-collinear`, `fig-lec02-lines` and section alias `lec02-geometry` remain valid for existing cross-references. The figure asset stays in its original folder so regeneration remains reproducible.

The coverage register maps every repeated L2 slide to its sole L1 teaching location. Formula registers, public references, source/quiz notes, chapter routes, and counts are updated together. The unique-content rule is added to the style guide and simplification prompt for later lectures.

Final checks: compared substantive paragraphs across both chapters (no identical explanatory paragraphs), and manually checked concept ownership, tables, formulas, worked examples and TLDR/quiz topics. L2 source decreased from 6,716 to 5,753 whitespace-separated words including equations/directives; this is a source-size measure, not a prose-only reading-length estimate. Both editions and relocated references compile successfully.
