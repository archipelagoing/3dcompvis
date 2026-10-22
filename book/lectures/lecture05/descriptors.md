(lec05-descriptors)=
# Describe a patch, then judge its matches

**A detector says “look here.” A descriptor says “this is what it looks like.”** Two distant views may need descriptor matching even when frame-to-frame tracking is impossible.

**Source:** PDF pages 61–91. The deck's BRIEF/ORB/BRISK material credits J. Heinly and the original method authors. Distortion and viewpoint changes can alter a descriptor even when its intended invariance helps.

## Binary descriptors make comparisons cheap

````{formula-box} Formula — binary tests, smoothing and Hamming distance
```{math}
:label: eq-lec05-binary
\begin{aligned}
\bar I_\sigma(p)&=\sum_q G_\sigma(q)I(p-q),\quad \sum_qG_\sigma(q)=1,\\
\tau_i&=\mathbf1[\bar I(p_i)<\bar I(q_i)],\qquad
B=(\tau_1,\ldots,\tau_K),\\
D_H(B,C)&=\sum_{i=1}^K\mathbf1[B_i\ne C_i].
\end{aligned}
```

Each ordered sample pair produces one bit; equality gives zero under the stated strict comparison. $G_\sigma$ is a Gaussian smoothing kernel, $K$ is the number of tests, and Hamming distance counts differing positions. This is related to Lecture 4's Census bit comparisons, but these methods use selected point pairs rather than necessarily comparing every neighbor to the center. Normalize a truncated Gaussian's weights.
````

```{application} Build and compare a binary description
1. Smooth the patch to reduce sensitivity to pixel noise.
2. Apply the same ordered sampling pattern in both patches, with the method's orientation/scale handling.
3. Store one bit per intensity comparison. A 256-bit description occupies 32 bytes.
4. Count XOR bits to compare descriptors. Reject ambiguous candidates rather than assuming the smallest distance is correct.
```

```{figure} ../../images/lecture05/descriptor-patterns.*
:name: fig-lec05-descriptor-patterns
:width: 95%
:alt: Source eye-patch diagrams compare BRIEF point pairs, ORB orientation, and BRISK ring sampling.

BRIEF, ORB and BRISK on the lecture eye patch: PDF pages 65, 72 and 77. Credits: J. Heinly slides, with Calonder et al., Rublee et al., and Leutenegger et al. named in their source sections. The sampling geometry changes; the output remains a compact bit string.
```

**BRIEF** uses fixed intensity-pair tests, with Gaussian-distributed sample locations in the source illustration. It is fast, but an unrotated fixed pattern does not itself compensate for image rotation or scale change. The slides list 128, 256 or 512 bits.

**ORB** combines FAST corner detection with orientation and rotated BRIEF tests. FAST looks for a sufficiently long contiguous bright or dark arc around a center relative to a threshold; the lecture illustrates a 12-pixel arc on a 16-pixel circle and rapid rejection tests. Other FAST variants use other arc lengths. Harris ranking/NMS selects useful candidates.

````{formula-box} Formula — orientation from intensity moments
```{math}
:label: eq-lec05-orientation
m_{pq}=\sum_{x,y}x^py^qI(x,y),\quad
C=\left(\frac{m_{10}}{m_{00}},\frac{m_{01}}{m_{00}}\right),\quad
\theta=\operatorname{atan2}(m_{01},m_{10}),\quad
p_i^{steered}=R(\theta)p_i.
```

Patch coordinates are centered on the keypoint; use a consistent intensity convention and circular support. $C$ is the intensity centroid. A zero/near-zero centroid direction gives unstable orientation; $m_{00}=0$ makes the centroid undefined. Steering rotates the **sampling pattern**, not the physical object.
````

```{application} Align the description before comparing it
1. Estimate the patch's orientation from the intensity moments.
2. Rotate all test locations consistently with the selected reference orientation.
3. Interpolate/smooth samples and compute bits in the same test order.
4. Use comparisons with good variance and low mutual correlation; redundant bits contribute less independent information.
```

For example, $m_{10}=0$, $m_{01}>0$ yields $\theta=90^\circ$. Rotating pair endpoint $(1,0)^T$ gives $(0,1)^T$. The geometry is the rotation rule from Lecture 1 applied to descriptor sampling.

**Scale qualification:** the lecture summary lists no scale invariance for ORB. The full ORB pipeline detects features over an image pyramid, providing multiscale handling; a single steered descriptor at a fixed scale does not supply that by itself. See the [official ORB description](https://docs.opencv.org/4.13.0/d1/d89/tutorial_py_orb.html) and [ORB class documentation](https://docs.opencv.org/3.4.7/db/d95/classcv_1_1ORB.html). Distinguish orientation compensation, scale selection, and robustness instead of promising perfect invariance.

**BRISK** estimates location and scale, uses a concentric sampling pattern with Gaussian-smoothed intensities, estimates orientation from long-distance pairs, and encodes short-distance comparisons. The source's “avoid short-distance comparisons” bullet on page 81 is misleading: long pairs estimate orientation; short pairs build the descriptor. The 512-bit descriptor uses 64 bytes. Its detection/description pipeline targets rotation and scale changes, while smoothing improves noise robustness. The [authors' implementation](https://github.com/ethz-mrl/brisk) and [original paper](https://www.iro.umontreal.ca/~mignotte/IFT6150/Articles/BriskDetector.pdf) support this distinction. The scale diagram is conceptual; do not infer that BRISK is simply SIFT's DoG detector.

## A small distance is not enough

With $m$ and $n$ descriptors of $K$ bits, exhaustive comparison takes $O(mnK)$ bit-level work (or fewer machine-word XOR/popcount operations). The cross-image distance matrix has shape $m\times n$. It need not be square, symmetric, or have a zero diagonal. Those properties apply to distances within the same ordered set, as qualified from source page 85.

````{formula-box} Formula — nearest-neighbor distance ratio
```{math}
:label: eq-lec05-ratio
j_1=\arg\min_jD(A,B_j),\qquad
\rho=\frac{d_1}{d_2},\qquad
\text{accept if }d_1<\tau d_2,\quad 0<\tau<1.
```

$d_1\le d_2$ are the first and second candidate distances for the **same query**, with $d_2>0$. A small ratio indicates a distinctive nearest candidate. If $d_2=0$, there are tied exact candidates; reject or resolve the ambiguity explicitly. A threshold is a chosen policy, not a universal constant. A mutual-nearest test checks agreement in both matching directions.
````

```{application} Filter proposed correspondences
1. Compute a metric appropriate to the descriptor; use Hamming for the binary convention above.
2. Compare an absolute threshold, nearest-neighbor choice, and the ratio test for the intended task.
3. Require mutual matching or spatial/geometric verification when appropriate.
4. Pass surviving pairs to the earlier RANSAC/epipolar/homography procedures; descriptor similarity is appearance evidence, not a geometry proof.
```

(ex-lec05-bits)=
`````{worked-example} Worked example 5.2 — a distinctive binary match
```{original-question} Original practice question
**Original companion to:** pages 68 and 89–90. Query $A=10110010$ has candidates $B=10110011$ and $C=01001100$. Apply a ratio threshold of 0.8 and state the next verification step.
```

````{solution-step} 1 — Count differing positions
**Why:** Binary descriptors are compared by Hamming distance.

$A\oplus B=00000001$ has one set bit, so $D_H(A,B)=1$. $A\oplus C=11111110$ has seven, so $D_H(A,C)=7$.
````

````{solution-step} 2 — Apply an explicit acceptance rule
**Why:** The second-nearest candidate reveals how distinctive the best one is.

With $\tau=0.8$, $\rho=1/7\approx0.143<0.8$, so accept $B$ provisionally. If the two distances were $7$ and $8$, the ratio $0.875$ would fail even though one candidate is closest.
````

````{solution-step} 3 — Check geometry
**Why:** A unique appearance match can still pair different physical surfaces.

Verify the candidate with the relevant geometric model before using it for reconstruction.
````
`````

```{figure} ../../images/lecture05/matching-choice.*
:name: fig-lec05-matching-choice
:width: 85%
:alt: Source diagram contrasts fixed-radius matching, nearest-neighbor matching, and a nearest-neighbor ratio test.

Source PDF page 90. A distance threshold uses a fixed radius; nearest-neighbor matching always selects the closest candidate; the ratio test asks whether that choice is sufficiently better than the next one.
```

## Measure the quality of the decisions

````{formula-box} Formula — matching evaluation
```{math}
:label: eq-lec05-quality
\begin{aligned}
\text{precision}&=\frac{TP}{TP+FP},&
\text{recall}=TPR&=\frac{TP}{TP+FN},\\
FPR&=\frac{FP}{FP+TN},&
\text{accuracy}&=\frac{TP+TN}{TP+FP+FN+TN}.
\end{aligned}
```

TP/FP/FN/TN are true positives, false positives, false negatives and true negatives against known match labels. Require nonzero denominators for each reported ratio. The ROC curve plots TPR against FPR as the threshold changes; its ideal operating region has high TPR and low FPR. Accuracy can look high merely because nonmatches dominate.
````

```{application} Evaluate a matching rule
1. Label the evaluation pairs and count all four outcomes.
2. State the threshold and compute the relevant ratios.
3. Vary the threshold to inspect the false-match/missed-match tradeoff.
4. Keep the evaluation dataset and candidate-pair definition fixed when comparing methods.
```

(ex-lec05-confusion)=
`````{worked-example} Worked example 5.3 — the slide's 100-pair table
```{original-question} Source slide example
**Source:** PDF page 87 gives $TP=18$, $FP=4$, $FN=2$, $TN=76$. Compute precision, recall, false-positive rate and accuracy.
```

````{solution-step} 1 — Check the counts
**Why:** The four cells must account for the same evaluation population.

There are $18+4+2+76=100$ pairs, $18+2=20$ real matches and $4+76=80$ real nonmatches.
````

````{solution-step} 2 — Compute precision and recall
**Why:** Accepted-match reliability and recovered-match coverage answer different questions.

$$\text{precision}=\frac{18}{18+4}=\frac{18}{22}\approx0.8182,\qquad
\text{recall}=\frac{18}{18+2}=0.9.$$
````

````{solution-step} 3 — Compute false-positive rate and accuracy
**Why:** These use different denominators from precision.

$$FPR=\frac4{4+76}=0.05,\qquad
\text{accuracy}=\frac{18+76}{100}=0.94.$$

This reproduces the source values. A false-positive rate of 5% does not mean 95% of accepted matches are correct; their precision is about 82%.
````
`````

For large descriptor databases, multidimensional trees or hashing can reduce search work. Their speed and approximation quality depend on dimensionality, distance metric and data distribution; exact exhaustive search remains the comparison baseline. These are the indexing alternatives on PDF page 91, not a guarantee of logarithmic query time.

```{index} BRIEF
```
```{index} ORB
```
```{index} BRISK
```
```{index} Hamming distance
```
```{index} Nearest-neighbor distance ratio
```
