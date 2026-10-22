(errata)=
# Errata and assumptions

The supplied study notes flag these source issues. Completed chapters give independently checked corrections below; later chapters retain provisional entries.

| Source | Issue | Treatment or status |
| --- | --- | --- |
| Fall 2025 Quiz 2 | A line-coefficient vector is described as a point | Verified in [Lecture 4](../lectures/lecture04/epipolar-practice.md): line/point equality corrected; supplied matrix has rank three |
| Fall 2025 Quiz 5 | A planar grid supports a full-scene metric-upgrade claim | State calibration/view assumptions and distinguish plane from full-scene recovery in Lecture 6 |
| `cs532f15_quiz4.pdf`, `cs532f15_quiz9.pdf` | Filenames suggest 2015; printed headers identify Spring 2019 | Retain both names in citations |
| `cs532s20_quiz3.pdf` | Printed header mixes years/quiz labels | Record the filename and printed wording |

Completed chapters report their independent checks; later entries remain provisional. Relevance scores describe slide relevance, not exam probabilities.

## Lecture 1: verified qualifications and convention translations

- **Projective-plane shorthand (PDF page 71):** nonzero homogeneous vectors must be identified under common scale; they are not distinct projective points. See {ref}`lec01-projective`.
- **Quaternion convention (PDF page 92):** the source sandwich is $q^{-1}Pq$. This book uses active Hamilton rotation $qPq^{-1}$ and demonstrates the inverse relationship explicitly. Conjugation alone gives the inverse only for unit quaternions. See {ref}`lec01-rotations`.
- **Camera symbols (PDF pages 111–113):** camera-to-world pose and world-to-camera extrinsics use inverse transformations. The book translates the slide's notation and clarifies that projection maps 3D to 2D; its inverse without depth is a ray. See {ref}`lec01-cameras`.
- **Plane uniqueness (Fall 2025 Quiz 1 Q4):** camera centers and the chosen object-frame origin determine a unique plane only when noncollinear. See {ref}`Example 1.11 <ex-lec01-object-plane>`.
- **Nullspace wording (PDF pages 83–85):** solve the right nullspace of the stacked incidence matrix, not “the nullspace of” the unknown point/plane. See {ref}`lec01-planes`.

Numerical companions are checked by `scripts/check_lecture01_math.py`. These qualifications do not imply that every flagged issue in later lectures has already been checked.

## Lecture 2: verified corrections and assumptions

- **Matrix-to-quaternion formula, PDF page 49:** the scalar component needs $w=\frac12\sqrt{1+\operatorname{tr}R}$. The slide omits $+1$; identity, quarter-turn, and cyclic-axis checks expose the error. Near a half-turn, use a component branch instead of dividing by $w$. See {ref}`lec02-quaternions`.
- **Quaternion convention, PDF pages 43, 48–49:** the sandwich and quaternion-to-matrix slide use the inverse/passive convention relative to the book, while the displayed skew-entry extraction uses active signs. The book uses active Hamilton formulas consistently and verifies matrix round trips.
- **Geometry shorthand, PDF pages 11, 23–25:** identify homogeneous vectors under nonzero scale; compute the right nullspace of the incidence coefficient matrix, not of the unknown vector. These repeat Lecture 1's qualifications.
- **Camera direction, PDF page 60:** the displayed projection goes from 3D to 2D despite the prose saying 2D to 3D. Without depth, inverse projection gives a ray. See {ref}`lec01-quiz-practice`.
- **Radius notation, PDF page 109:** the displayed polynomial and radius definition mix squared-radius conventions. The book defines $r^2$ explicitly and states the correction direction and coefficient units. See {eq}`eq-lec02-radial`.
- **Fundamental-matrix uniqueness, PDF page 124:** uniqueness is up to scale for a fixed nondegenerate camera pair; a finite match set can be ambiguous. Coincident camera centers do not yield a nonzero fundamental matrix. See {ref}`lec02-two-view`.
- **Quiz degeneracy, Spring 2020 Quiz 1 P1:** repeated points make the cross-product line undefined, although the determinant still correctly indicates linear dependence and existence of a containing line. P3 requires $d>0$ for distinct vertical lines. See {ref}`lec01-quiz-practice`.

Lecture 2's numerical examples are checked by `scripts/check_lecture02_math.py`.

## Lecture 3 qualifications

- **Spring 2020 Quiz 3:** the page carries mixed Spring 2019 Quiz 2 / Spring 2020 Quiz 3 headers and near-duplicate camera questions; it is retained as a retest.
- **Camera quiz P2/P4:** horizontal FOV does not specify all of $K$ or a physical focal length. [The solutions](../lectures/lecture03/calibration.md) state the extra assumptions, image-center convention, and pixel-pitch requirement.
- **Pentagon quiz:** “equilateral” alone does not imply regular. Ten equally supported corner alignments require the regular-polygon assumption. [The RANSAC solution](../lectures/lecture03/probability-ransac.md) also distinguishes standard independent-status trial counts from exact finite-pool counts and explicitly chooses 99% confidence.
- **Repeated slide issues:** PDF page 11's projection-direction wording and page 60's radial-radius notation retain the corrections already explained in Lectures 1–2.

## Lecture 4 verified corrections and conventions

- **Fall 2025 Quiz 2 Q2:** $x'^TF$ is a line row, not a point. The condition is $x'^TFx=0$. The supplied matrix has determinant four, so it is rank three and cannot be a physical fundamental matrix. [Example 4.3](../lectures/lecture04/epipolar-practice.md) solves the given equation without relabeling it as valid camera geometry.
- **Fall 2025 Quiz 3 Q1:** 0.8 cm is the first-order error magnitude. The exact signed errors are +0.8333 cm for disparity 24 and −0.7692 cm for disparity 26. [Stereo solutions](../lectures/lecture04/stereo.md) define estimated-minus-true signs.
- **L4 PDF page 35, printed slide 39:** the shown seven-point RANSAC table uses approximately 95% confidence. A 99% budget at 80% inliers is 20 trials, rather than the table's 13.
- **Spring 2020 Quiz 5:** the printed header overprints 2019/2020; its problem repeats Spring 2019 Quiz 5. Both filenames and headers remain documented.
- **NCC, PDF page 68:** use a self-consistent centered-norm denominator and reject zero-variance patches. The [explicit formula](../lectures/lecture04/matching.md) avoids ambiguity about whether standard deviations include a sample-count factor.
- **Repeated radial notation, PDF page 6:** the radius/squared-radius clarification remains at its canonical Lecture 2 location.
