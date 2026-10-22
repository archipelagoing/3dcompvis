(lec02-review)=
# Review and formula checklist

Check the new tools below. Foundation explanations and Spring 2020 Quiz 1 solutions are in {ref}`lec01-quiz-practice`. Source ranges below are PDF pages in `cs532_f25_Week2.pdf`.

| Topic and source pages | Canonical formula or explanation | Practice |
| --- | --- | --- |
| Quaternion conversion, 44–49 | {eq}`eq-lec02-qmatrix`; {eq}`eq-lec02-matrixq` | {ref}`Example 2.1 <ex-lec02-conversions>` |
| Smooth rotation interpolation, 45 | {eq}`eq-lec02-slerp` (explanatory companion) | Identity to quarter-turn midpoint |
| Directional affine scaling, 68 | {eq}`eq-lec02-affine-factors` | Stretch along a diagonal |
| Planar rectification and cross-ratio, 62–71 | {eq}`eq-lec02-homography`; {eq}`eq-lec02-crossratio` | {ref}`Example 2.2 <ex-lec02-homography>`; court warp |
| Warping and interpolation, 72–81 | {eq}`eq-lec02-inversewarp`; {eq}`eq-lec02-bilinear` | {ref}`Example 2.3 <ex-lec02-bilinear>` |
| Homography estimation, 82–94 | {eq}`eq-lec02-dlt`; {eq}`eq-lec02-normalize` | {ref}`Example 2.4 <ex-lec02-dlt>` |
| Robust estimation and matching, 95–104 | {eq}`eq-lec02-ransac`; {ref}`lec02-estimation` | {ref}`Example 2.5 <ex-lec02-ransac>` |
| Radial correction, 105–110 | {eq}`eq-lec02-radial` | Correct $(100,0)$ to $(101,0)$ |
| Epipolar geometry, 111–126 | {eq}`eq-lec02-fundamental`; {eq}`eq-lec02-fcamera`; {eq}`eq-lec02-eightpoint` | {ref}`Example 2.6 <ex-lec02-fundamental>` |
| Rectification, 127–129 | {eq}`eq-lec02-rectify` | Equal-row and epipole checks |

## Can you do these without notes?

- Convert a rotation matrix to a quaternion and verify the round trip.
- Check quaternion signs with a cyclic-axis rotation and handle a half-turn without dividing by zero.
- Explain why a homography has eight DOF and needs four nondegenerate matches.
- Write two DLT rows for a match and identify the correct right singular vector.
- Undo coordinate normalization in the correct order.
- Explain why inverse warping still needs interpolation and a boundary rule.
- Distinguish noise, outliers, and the wrong geometric model.
- Map an image point to an epipolar line, then test a possible match.

**Choose the right image model:** a homography maps planar points to points; a fundamental matrix maps a point to a correspondence line in another view.

Finish with the [TLDR and short quiz](tldr.md). [Lecture 3](../lecture03/index.md) adds camera calibration and projective homography practice. [Lecture 4](../lecture04/index.md) adds noisy epipolar estimation, calibrated poses, stereo, and the assigned quizzes.
