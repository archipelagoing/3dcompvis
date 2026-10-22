# Lecture boundaries and overlap decisions

Status: **Lectures 1–4 fully audited and drafted; later full audits pending**. PDF pages below are one-based. Printed slide labels differ in places and must be verified independently.

| Deck | Observed PDF page ranges | Teaching ownership |
| --- | --- | --- |
| Lecture 1 | 2–61 motivation/applications; 62–103 geometry, transformations, rotations/quaternions; 104–114 camera introduction | Teach actual foundations here and retain the motivating applications; introduce projection to the depth of the deck |
| Lecture 2 | 2–41 repeated geometry; 42–50 expanded axis-angle/quaternions; 51–61 camera introduction; 62–104 projectivities, warping, DLT, RANSAC; 105–129 distortion/two-view introduction | Cross-reference Lecture 1; teach conversions, planar warping, normalized DLT/RANSAC, distortion and epipolar introductions here. Lectures 3/4 retain their assigned quizzes and expanded practice. |
| Lecture 3 | All 80 pages audited; pages 2–80 repeat L2 PDF 51–129 | Retain canonical L1/L2 teaching; add FOV calibration, ray–plane depth, complete projective normalized DLT, probability/pentagon quiz applications and sampling explorer |
| Lecture 4 | All 77 pages audited; repeated distortion/epipolar/rectification mapped to L2 | User-requested guided epipolar recap with new step-by-step applications; noisy F fitting/residuals, essential poses/cheirality, stereo depth/sensitivity/error and dense costs/support |
| Lecture 5 | Corners, tracking, descriptors; full audit pending | Detection, tracking, matching and assigned quizzes |
| Lecture 6 | Structure from motion; full audit pending | Reconstruction, factorization, triangulation, optimization and assigned quizzes |

Primary quiz placement follows `quizByLec.md`, not the first slide mentioning a concept. Spring 2020 Quiz 1 remains in Lecture 2 and links back to Lecture 1 foundations. Fall 2025 Quiz 1's geometry belongs to Lecture 1 and its probability questions to Lecture 3. Defer advanced questions until their prerequisites are taught.

The first two chapter titles describe emphasis rather than exclusive boundaries. A topic may be introduced, revisited, and applied later but has one canonical full explanation and formula box.

Lecture 1 completion details and verified source dispositions are recorded in `lecture01-audit.md` and `coverage.csv`. Its chapter covers the actual full deck; later chapters should cross-reference repeated foundations.

Lecture 2 page-level decisions, selected examples and corrections are recorded in `lecture02-audit.md`; its 129 pages are accounted for in `coverage.csv`.

The user subsequently required unique content across chapters. Repeated L2 teaching is now assigned only to L1; its distinct foundation quiz solutions moved to L1 while original L2 source placement remains recorded. See `lecture01-02-overlap-audit.md`.

Lecture 3 overlap and page-level source dispositions are recorded in `lecture03-audit.md` and `coverage.csv`. No repeated theoretical derivations were added.

Lecture 4 ownership, actual slide-image selections, printed-number discontinuity, and source corrections are recorded in `lecture04-audit.md` and `coverage.csv`.

## Full quiz-workbook revision

The user explicitly requested the complete problem and red-step/blue-math solution for every quiz across all lectures. Six canonical quiz workbooks follow the booklet's primary lecture assignments. Concept explanations retain one teaching location, while repeated historical quizzes deliberately retain their own full walkthroughs. Existing example labels now lead to the complete question instead of an abbreviated answer. Lecture 2's foundation quiz has its full workbook here; Lecture 1 links to it. All assigned Lecture 5–6 quiz questions are available before their unfinished main chapters.
