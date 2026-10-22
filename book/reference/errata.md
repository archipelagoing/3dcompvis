(errata)=
# Errata and assumptions to verify

These source issues are flagged by the supplied study notes. Detailed corrections will be independently checked when the relevant worked examples are written.

| Source | Issue | Planned treatment |
| --- | --- | --- |
| Fall 2025 Quiz 2 | A line-coefficient vector is described as a point | Verify arithmetic, matrix rank, and the scalar epipolar constraint in Lecture 4 |
| Fall 2025 Quiz 5 | A planar grid supports a full-scene metric-upgrade claim | State calibration/view assumptions and distinguish plane from full-scene recovery in Lecture 6 |
| `cs532f15_quiz4.pdf`, `cs532f15_quiz9.pdf` | Filenames suggest 2015; printed headers identify Spring 2019 | Retain both names in citations |
| `cs532s20_quiz3.pdf` | Printed header mixes years/quiz labels | Record the filename and printed wording |

All source-solution computations remain subject to independent checking. Relevance scores describe slide relevance, not exam probabilities.

## Lecture 1: verified qualifications and convention translations

- **Projective-plane shorthand (PDF page 71):** nonzero homogeneous vectors must be identified under common scale; they are not distinct projective points. See {ref}`lec01-projective`.
- **Quaternion convention (PDF page 92):** the source sandwich is $q^{-1}Pq$. This book uses active Hamilton rotation $qPq^{-1}$ and demonstrates the inverse relationship explicitly. Conjugation alone gives the inverse only for unit quaternions. See {ref}`lec01-rotations`.
- **Camera symbols (PDF pages 111–113):** camera-to-world pose and world-to-camera extrinsics use inverse transformations. The book translates the slide's notation and clarifies that projection maps 3D to 2D; its inverse without depth is a ray. See {ref}`lec01-cameras`.
- **Plane uniqueness (Fall 2025 Quiz 1 Q4):** camera centers and the chosen object-frame origin determine a unique plane only when noncollinear. See {ref}`Example 1.11 <ex-lec01-object-plane>`.
- **Nullspace wording (PDF pages 83–85):** solve the right nullspace of the stacked incidence matrix, not “the nullspace of” the unknown point/plane. See {ref}`lec01-planes`.

Numerical companions are checked by `scripts/check_lecture01_math.py`. These qualifications do not imply that every flagged issue in later lectures has already been checked.
