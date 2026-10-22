(lec04-review)=
# Review and source checklist

Start with the [epipolar visual guide and calculations A–C](epipolar-practice.md): point-to-line multiplication, candidate checks, transpose, and epipole nullspaces. Then work through the expanded quiz examples below. The {ref}`stereo sensitivity walkthrough <stereo-depth-sensitivity>` explains exact errors, the derivative, distance-squared sensitivity, and uncertainty intervals.

## Formula and application map

| Task | Formula box and procedure |
| --- | --- |
| Correct a noisy fitted F to rank two | {eq}`eq-lec04-ranktwo`, [estimation](estimation.md) |
| Measure pixel distance from epipolar predictions | {eq}`eq-lec04-epipolar-error` |
| Use calibration to isolate camera motion | {eq}`eq-lec04-essential`, [pose recovery](essential.md) |
| Generate and test four pose candidates | {eq}`eq-lec04-poses` |
| Compute rectified stereo depth | {eq}`eq-lec04-depth`, [stereo](stereo.md) |
| Distinguish exact from first-order error | {eq}`eq-lec04-depth-error` |
| Restrict disparity using a depth interval | {eq}`eq-lec04-disparity-range` |
| Aggregate a cost volume and select a hypothesis | {eq}`eq-lec04-cost-volume`, [matching](matching.md) |
| Compare patch appearance | {eq}`eq-lec04-patch-costs` |
| Encode relative brightness order | {eq}`eq-lec04-census` |
| Adapt support at boundaries | {eq}`eq-lec04-adaptive` |

The canonical fundamental constraint, linear eight-point rows, radial correction, and rectification formulas remain in [Lecture 2](../lecture02/two-view.md). Normalized point-coordinate transforms remain in [Lecture 2 estimation](../lecture02/estimation.md).

## Worked examples and assigned quizzes

| Example | Source or purpose |
| --- | --- |
| {ref}`4.1 <ex-lec04-symbolic>` | Both Spring 2019 Quiz 4 files: P1 line, P2 explicit constraint; duplicate retained for retest |
| {ref}`4.2 <ex-lec04-third-view>` | Fall 2025 Quiz 2 Q1: third-view intersection and degeneracies |
| {ref}`4.3 <ex-lec04-invalid-f>` | Same quiz Q2: consistent points, line/point correction, invalid rank-three F |
| {ref}`4.4 <ex-lec04-eightpoint>` | Original noisy normalized fit and held-out numerical checks |
| {ref}`4.5 <ex-lec04-pose>` | Original essential-matrix/four-pose calculation |
| {ref}`4.6 <ex-lec04-stereo-fall>` | Fall 2025 Quiz 3 Q1: both exact signs versus the supplied linearization |
| {ref}`4.7 <ex-lec04-stereo-spring>` | Spring 2019 Quiz 5, all three bullets; Spring 2020 duplicate retest |
| {ref}`4.8 <ex-lec04-search>` | Fall 2025 Quiz 3 Q2: depth range to disparity bounds |
| {ref}`4.9 <ex-lec04-patches>` | Original SAD/SSD/NCC calculation |
| {ref}`4.10 <ex-lec04-census>` | Original rank/Census distinction |
| {ref}`4.11 <ex-lec04-adaptive>` | Original boundary-weighting calculation |

## Slide coverage without repeated teaching

| PDF pages | Disposition |
| --- | --- |
| 1 | Title and source metadata |
| 2–21 | Distortion, epipolar planes/epipoles/F and linear rows already taught in L2; guided geometry recap and expanded quiz applications here |
| 22–23 | Essential-matrix constraints, four poses and cheirality |
| 24–37 | Noisy normalized F fitting, rank projection, residuals, seven-point robust sampling and model degeneracy |
| 38–41 | Search reduction and rectification already taught in L2; linked as prerequisites |
| 42–57 | Dense depth hypotheses, cost volumes, support choices, matching criteria and representation/algorithm overview |
| 58–64 | Rectification linked to L2; new stereo derivation and depth applications |
| 65–77 | Window size, cost curves, texture/occlusion ambiguity, rank/Census, shiftable/rod/adaptive support |

**What to check in an exam answer:** image order, coordinate units, matrix rank, transform direction, positive depths in both cameras, signed versus absolute errors, and whether a score must be minimized or maximized.

Finish with the [TLDR and short quiz](tldr.md).
