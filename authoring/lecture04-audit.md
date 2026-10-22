# Lecture 4 source audit and teaching ownership

Source: `wk4_cs532s26_TwoViewGeometry.pdf`, all 77 PDF pages extracted and inspected visually in four rendered contact sheets, with the unnumbered page 54 inspected separately. Printed numbers match PDF pages 1–34, jump to 39 at PDF page 35, and remain PDF+4 where visible. Page 54 has no visible number. The printed-number gap does not imply unexamined PDF pages.

## Ownership and coverage

- Pages 2–21 repeat the L2 distortion and epipolar introduction, including fundamental-matrix properties and linear rows. L2 retains canonical formula references; following user feedback, L4 also includes a guided ray/plane/line recap and original numerical point-to-line, candidate, transpose and epipole-nullspace calculations before the expanded symbolic and three-view quiz applications.
- Pages 22–23 add E, its equal-pair singular-value condition and five DOF, four poses, and positive-depth selection. L4 gives a derivation and computational SVD companion with an independently solved four-pose example. Official OpenCV documentation was consulted only to cross-check decomposition/translation-direction/cheirality conventions; its link is retained beside the material.
- Pages 24–37 add numerical F estimation, nearest rank-two projection, geometric pixel residuals, normalization experiments, seven-point robust hypotheses, guided matches and degenerate scenes. General point normalization, existing linear rows, and general RANSAC probability remain at L2/L3. The twelve-match noisy numerical dataset is in `lecture04-matches.csv`; the checker regenerates its camera projections/noise and held-out data.
- Pages 38–41 repeat search reduction/rectification; retain L2 canonical teaching.
- Pages 42–57 introduce dense depth hypotheses, cost volumes, hypothesis evaluation/aggregation/selection, oriented planes and matching representations/algorithms. L4 develops the matching model and costs; L1 remains the home for the overall reconstruction/application pipeline.
- Pages 58–64 revisit rectification, then introduce disparity and stereo depth. The BAD/GOOD pair-rectification sequence is interpreted as compatible row alignment, with the L2 explanation linked. L4 derives Z=fb/d and applies the assigned quizzes.
- Pages 65–77 add patch costs, window size, ambiguity/occlusion, score curves, fronto-parallel support, shifted/rod-shaped windows, rank/Census and adaptive weighting. These receive named formulas/applications and original numerical companions where useful. The named mutual-information/learning methods and joint optimization families receive concise descriptions at the source's level; no full algorithm absent from the slides is claimed.

Every page's disposition and selected example are recorded in `coverage.csv`.

## Quiz completeness and corrections

- Both Spring 2019 Quiz 4 filenames: P1 line expression/sketch reference; P2 exact four-entry scalar expansion and vector-product form. Second file retained as same-content retest.
- Fall 2025 Quiz 2 Q1: two predicted lines in C, homogeneous intersection, coherent original numerical example and camera construction, coincident/parallel/noisy cases and visibility qualification.
- Fall 2025 Quiz 2 Q2: independently verified row (2,4,6), two finite consistent points, line/point source correction; determinant=4 makes the given matrix rank three. The exercise is solved as the supplied bilinear constraint without pretending to repair the matrix silently.
- Fall 2025 Quiz 3 Q1: true depth and both signed exact one-pixel errors, compared with the supplied 0.8 cm linearized magnitude. Q2: centimeter/meter conversion and 1–5 pixel search range.
- Spring 2019 Quiz 5 all three bullets: exact +25/3 cm and −25/6 cm errors and their decreasing magnitudes at larger disparity. Spring 2020 retest retains mixed printed 2019/2020 header.
- RANSAC slide table verified as 95% seven-point budgets, distinguished from 99% and from an eight-point solver's sample size.
- NCC normalization explicitly defined with centered norms and zero-variance exclusion, rather than inferring the slide's standard-deviation convention.

## Selected visuals and interaction

Five original paired SVG/PDF diagrams: a sloping epipolar-line/candidate illustration, third-view intersection, rectified stereo rays, inverse-depth sensitivity with one-pixel intervals, and support crossing a depth boundary. The actual toy/plant reference/matching images are extracted from PDF page 46, printed 50; editable panel labels retain the unmodified JPEG assets. The window-size comparison is extracted unchanged from PDF page 66, printed 70. Source credits/unknown individual creators and permissions are preserved in captions and `figure-credits.csv`.

The lecture has one actual Three.js stereo scene: aligned cameras with correctly sized virtual planes, epipolar plane, true/perturbed ray intersections, linked left/right image columns, and numerical substitution cards. True depth, baseline, focal length and signed disparity error are adjustable. Point dragging changes modeled depth; inspection orbit/zoom does not change the model. Invalid measured disparities and off-image correspondences are identified. The static explanation/table/curve carries the full learning objective into PDF/no-JavaScript reading. Camera markers are schematic; projection geometry uses a disclosed physical pixel pitch.

## Checks and handoff

`check_lecture04_math.py` independently checks all quiz subparts, generated noisy data and held-out errors, singular-value constraints/pose selection, exact signed errors/search limits, sampler budgets, score direction/normalization, rank/Census and adaptive costs. `check_lecture04_browser.py` checks eight pages and ten stereo states, actual ray-plane intersections, 3D gestures, reset/keyboard, mobile, earlier widget initialization, and all static fallbacks. Build/print/bundle inspection results are recorded in `LECTURE04_STATUS.md` after execution. The next user review checkpoint precedes L5; L5/L6 remain outlines. No publishing or pushes are authorized by this chapter task.

## Requested clarity revision

The landing page now directly indexes epipolar calculations A–C and each assigned geometry/stereo example. Quiz solutions expose row/column products, cross-product components, scalar checks and homogeneous division. Stereo gives the common-denominator derivation, signed-error convention, derivative and non-calculus approximation, distance-squared sensitivity at fixed cameras, a near/far table, a bounded-error interval and both quiz errors with explicit fraction arithmetic. These derived explanations are original pedagogical companions to the lecture/quiz material. Stable quiz/example labels and the single 3D explorer are preserved.
