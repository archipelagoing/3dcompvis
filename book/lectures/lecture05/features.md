(lec05-features)=
# Find a small set of recognizable points

**To stitch two mountain photos, first find the same places in both.** Aligning all pixels blindly is expensive and easily confused by sky or repeated snow. A smaller set of distinctive neighborhoods gives the alignment process useful anchors.

**Source:** Lecture 5 PDF pages 3–10.

```{figure} ../../images/lecture05/panorama.*
:name: fig-lec05-panorama
:width: 95%
:alt: The source mountain photographs, feature correspondences, and aligned panorama.

The lecture's panorama sequence: detect points, find correspondences, then align. Alignment uses the homography methods already taught in Lectures 2–3; here the question is how to obtain their inputs. Source PDF pages 4–6; individual photographer/reuse terms unidentified.
```

A **feature detector** finds an interesting location. A **descriptor** summarizes its surrounding appearance. A **matcher** proposes which descriptor in another image belongs to the same physical feature. These are three separate decisions: a strong corner can still get a wrong match.

Useful features combine four properties:

- **Repeatability:** the same physical location can be detected again after viewpoint or illumination changes.
- **Distinctiveness:** its patch differs from plausible alternatives.
- **Locality:** the description uses a limited neighborhood, helping with clutter and partial occlusion.
- **Compactness:** there are far fewer features than pixels, and comparing their descriptions is efficient.

```{figure} ../../images/lecture05/mars.*
:name: fig-lec05-mars
:width: 95%
:alt: NASA Mars Rover views with small colored feature-match markers.

The lecture's difficult Mars Rover pair, with SIFT matches revealed. NASA imagery; match figure credited to Noah Snavely in PDF page 10. Look at the tiny corresponding marks rather than expecting the two entire views to look alike. SIFT motivates the problem; this deck's detailed descriptor material is BRIEF, ORB, and BRISK.
```

**What makes this hard?** A distinctive rock may change size or orientation. Repeated texture produces look-alikes. A feature may disappear behind another surface. Features help image alignment, reconstruction, tracking, navigation, retrieval, and recognition, but none of those applications makes a proposed correspondence automatically correct.

Next, [test whether a patch fixes a location in both directions](corners.md).

```{index} Feature detector
```
```{index} Feature descriptor
```
