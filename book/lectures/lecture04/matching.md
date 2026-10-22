(lec04-matching)=
# Find matches across an image

Geometry narrows the search to a row. **Appearance chooses a position along it.** That is still difficult: repeated textures can look identical, flat regions have little evidence, and some pixels are visible in only one camera.

**Source:** lecture PDF pages 42–77, printed slides 46–81 except unnumbered PDF page 54. Stereo contributors named on PDF page 42: Rick Szeliski, Pascal Fua, P. Mordohai, and E. Dunn.

## Generate, evaluate, select

The slide sequence on pages 45–53 follows one practical pipeline:

1. **Generate hypotheses:** sample possible disparities or depths. Each projects the reference pixel to a candidate in another view.
2. **Evaluate:** compare image appearance at the candidate, then combine neighboring evidence.
3. **Select:** choose a supported hypothesis, or reject the pixel when evidence is unreliable.

A **cost volume** stores one score for each image position and hypothesis: dimensions width × height × number of disparities. A depth map selects one hypothesis per reference pixel; it is view-dependent and need not contain occluded surfaces. The [earlier reconstruction pipeline](../lecture01/motivation.md) explains how depth can feed other 3D representations.

```{index} Cost volume
```

```{index} Photo-consistency
```

```{index} Occlusion
```

````{formula-box} Formula — aggregate costs and select disparity
```{math}
:label: eq-lec04-cost-volume
\overline C(p,d)=\frac1{|\Omega_p|}\sum_{q\in\Omega_p}C(q,d),
\qquad \widehat d(p)\in\operatorname*{arg\,min}_{d\in D_p}\overline C(p,d).
```

$p,q$ are pixel positions, $D_p$ the allowed disparity set, and $\Omega_p$ a support window. $C(q,d)$ is a dissimilarity between left location $q$ and right location $q-(d,0)$. Require valid samples and nonempty support. An argmin can contain several disparities: a tie is evidence of ambiguity, not a unique measurement.
````

```{application} Build a simple dense stereo estimate
1. **Input:** rectified images and the permitted disparity range.
2. Evaluate a cost at every valid candidate. Stack these candidate costs into the volume.
3. Aggregate support and pick the smallest cost; retain a confidence measure such as separation from competing minima.
4. Reject inconsistent left–right matches and occlusions. Convert reliable disparities to depth.

This is **winner-take-all** selection. The slides also name feature/edge matching followed by interpolation and joint optimization using iterative updates, dynamic programming, energy minimization, or graph methods. Those alternatives add spatial reasoning; they do not make missing image evidence appear.
```

```{figure} ../../images/lecture04/stereo-pair.*
:name: fig-lec04-pair
:width: 90%
:alt: Two supplied photographs show the same toy-and-plant scene from different viewpoints, revealing shifts and occlusions.

The actual reference/matching photographs from PDF page 46, printed slide 50. Look at the toy and leaf boundaries: viewpoints change which surfaces are visible. Extracted photographs with original project labels; individual photography credits and reuse terms are not identified on the slide.
```

## Compare patches, not isolated colors

**Photo-consistency** means that projections of the same scene point have compatible image appearance under the chosen model. For a patch, write its paired samples as $L_i,R_i(d)$, $i=1,\ldots,m$.

````{formula-box} Formula — SAD, SSD, and zero-mean NCC
```{math}
:label: eq-lec04-patch-costs
\begin{aligned}
\operatorname{SAD}(d)&=\sum_i|L_i-R_i(d)|,\qquad
\operatorname{SSD}(d)=\sum_i(L_i-R_i(d))^2,\\
\operatorname{NCC}(d)&=
\frac{\sum_i(L_i-\overline L)(R_i(d)-\overline R(d))}
{\sqrt{\sum_i(L_i-\overline L)^2\sum_i(R_i(d)-\overline R(d))^2}}.
\end{aligned}
```

$\overline L,\overline R$ are patch means. Minimize SAD/SSD; **maximize** NCC, or minimize a cost such as $1-\operatorname{NCC}$. NCC lies in $[-1,1]$ for nonconstant patches and is undefined if either centered patch has zero norm. SAD uses intensity units, SSD squared intensity units, NCC is dimensionless.
````

```{application} Choose and check a patch score
1. Use the same valid support and disparity convention for each candidate.
2. For SAD/SSD, compare aligned intensities directly. SSD penalizes large differences more strongly.
3. For NCC, subtract each patch's own mean and divide by its centered norm. Reject near-zero-variance supports.
4. Inspect the full score curve: multiple similar peaks or minima indicate uncertainty.

Positive affine brightness changes preserve ideal NCC, but clipping, reflections, shadows, and nonuniform exposure can break that assumption. The source's formula image leaves normalization factors dependent on its standard-deviation convention; the explicit sum-of-squares denominator above avoids that ambiguity.
```

(ex-lec04-patches)=
````{worked-example} Worked example 4.9 — when raw intensity picks the wrong patch
**Original companion to:** PDF pages 65–70.

Reference $L=(10,20,30)$ has two candidate patches: true but brighter $R_A=(30,40,50)$, and wrong $R_B=(10,20,10)$.

| Candidate | SAD | SSD | NCC |
| --- | --- | --- | --- |
| A: brighter match | $20+20+20=60$ | $3\times400=1200$ | $1$ |
| B: wrong texture | $0+0+20=20$ | $400$ | $0$ |

Raw difference scores favor B. For NCC, A's centered values equal the reference's $(-10,0,10)$, giving correlation one. B's centered values are $(-10/3,20/3,-10/3)$, perpendicular to the reference vector, giving zero. NCC favors A under the uniform brightness-offset model.

A flat patch such as $(20,20,20)$ instead has zero centered norm. It cannot supply a defined NCC score or a distinctive texture match.
````

## Window size trades detail for support

```{figure} ../../images/lecture04/window-size.png
:name: fig-lec04-window-size
:width: 85%
:alt: Two supplied depth estimates compare a small three-pixel window with a larger twenty-pixel window; the larger support is smoother and loses thin details.

The source's $w=3$ versus $w=20$ results, left to right (PDF page 66, printed slide 70). Larger support suppresses isolated mistakes but can erase detail. Extracted source illustration; its individual creator and reuse terms are not identified on that slide.
```

A constant-disparity window assumes **fronto-parallel support**: one axial depth. Slanted surfaces violate this assumption; windows crossing foreground and background mix different depths.

```{figure} ../../images/lecture04/support-boundary.*
:name: fig-lec04-support
:width: 85%
:alt: A window centered near a foreground edge crosses into background; an alternative shifted window stays mostly on the foreground.

A larger window can vote for two different depths. Adapting its position or weights changes which surface contributes evidence.
```

The slides offer several ways to adapt support:

- **Shiftable windows:** choose among windows that contain the reference pixel; favor support that stays on one surface.
- **Rod-shaped supports:** test elongated directions that may follow an approximately constant-disparity contour.
- **Adaptive weights:** downweight neighbors far away in position or color.
- **Oriented-plane hypotheses:** allow disparity to vary across a slanted plane instead of assuming one constant value.

All add assumptions. Similar colors can still occur at different depths, and an image edge need not be a depth edge.

## Rank and Census use relative intensity order

```{index} Census transform
```

```{index} Rank transform
```

```{index} Adaptive support
```

````{formula-box} Formula — rank, Census, and Hamming distance
```{math}
:label: eq-lec04-census
\begin{aligned}
r(p)&=\sum_{q\in\mathcal N_p}\mathbf1[I(q)<I(p)],\\
\mathcal C(p)&=\bigl(\mathbf1[I(q_1)<I(p)],\ldots,
\mathbf1[I(q_m)<I(p)]\bigr),\\
H(\mathcal C_L,\mathcal C_R)&=\sum_{i=1}^{m}\mathbf1[\mathcal C_{L,i}\ne\mathcal C_{R,i}].
\end{aligned}
```

$\mathcal N_p$ contains $m$ ordered neighbors excluding the center; $\mathbf1[\cdot]$ is one when its condition is true and zero otherwise. Rank ranges from $0$ to $m$; Census keeps the complete ordered bit string. Use the same neighbor order and tie convention in both images. Both preserve strictly increasing intensity remappings within the compared support.
````

```{application} Match relative-intensity patterns
1. Compare each neighbor with the center using the fixed strict inequality.
2. Sum the comparisons for rank, or retain their order for Census.
3. Compare rank-transformed images with a difference cost; compare Census strings by Hamming distance.
4. Check for repeated patterns and ties. Relative order is robust to some brightness changes, not to all lighting or geometry changes.
```

(ex-lec04-census)=
```{worked-example} Worked example 4.10 — equal ranks can hide different patterns
**Original companion to:** PDF page 74, printed slide 78.

Let the center intensity be 20. Ordered neighbors $(10,30,15,25)$ give Census **1010** and rank 2. A second patch with center 20 and neighbors $(5,10,30,40)$ gives **1100**, also rank 2. Their Census Hamming distance is **2**: bits 2 and 3 disagree.

The rank compresses spatial evidence into one count. Census retains which neighbors were darker. Adding the same brightness offset to every pixel of either patch preserves its comparisons, provided clipping does not change them.
```

## Give nearby, similar neighbors more influence

````{formula-box} Formula — locally adaptive support
```{math}
:label: eq-lec04-adaptive
\begin{aligned}
\Delta_c(p,q)&=\|\operatorname{Lab}(p)-\operatorname{Lab}(q)\|_2,
\quad \Delta_s(p,q)=\|p-q\|_2,\\
w(p,q)&=\exp\left[-\frac{\Delta_c(p,q)}{\gamma_c}
-\frac{\Delta_s(p,q)}{\gamma_s}\right],\\
\overline C_w(p,d)&=\frac{\sum_{q\in\Omega_p}w(p,q)C(q,d)}
{\sum_{q\in\Omega_p}w(p,q)}.
\end{aligned}
```

$\operatorname{Lab}(p)=(L_p,a_p,b_p)^T$ is a three-channel color vector. $\gamma_c>0$ uses color-distance units; $\gamma_s>0$ uses pixels, making both exponents dimensionless. These are reference-image weights with a nonzero sum. Other methods also include shifted right-image weights; specify the convention. A common weight multiplier cancels.
````

```{application} Aggregate without crossing every edge equally
1. Compute color distance in CIE Lab and spatial distance within the support.
2. Calculate positive weights with the chosen scales.
3. Form a weighted average cost for each disparity and compare candidates.
4. Inspect whether the support follows actual surfaces. Color similarity helps; it does not prove shared depth.

PDF pages 52/76 credit Yoon and Kweon (PAMI 2006); page 53 credits Lu et al. (CVPR 2013) for an oriented-plane extension. These descriptions explain their roles; they do not reproduce the full methods.
```

(ex-lec04-adaptive)=
```{worked-example} Worked example 4.11 — a two-sample depth boundary
**Original companion to:** PDF pages 75–76.

Two support samples are each one pixel away. One has the same color as the reference; the other differs by 40 Lab units. With $\gamma_c=10$, $\gamma_s=2$, their weights are $e^{-0.5}\approx0.60653$ and $e^{-4.5}\approx0.01111$.

At the true disparity, their costs are $(0,10)$; at a wrong disparity, $(10,0)$. Uniform averaging ties both at 5. Adaptive averaging gives about **0.180** for the true disparity and **9.820** for the wrong one. The same-color sample now contributes most of the evidence.

If that color boundary did not correspond to a depth boundary, this weighting preference could be misleading. The source's result images compare such support choices, not a universal guarantee of correctness.
```

The slide list also names **mutual information** (statistical dependence between intensities) and **learning-based methods** (learned appearance features or costs). They change how hypotheses are scored. The same geometry, visibility limits, and need to recognize uncertain matches remain.
