(lec04-stereo)=
# Stereo depth and its errors

Hold a finger in front of your face and close one eye at a time. Its apparent horizontal shift is larger when it is close. **Disparity** measures that shift in a rectified camera pair.

**Sources:** lecture PDF pages 58–64; Fall 2025 Quiz 3, `cs532f25_quiz_3_solution.pdf`, Q1–Q2, page 1; Spring 2019 Quiz 5, `cs532s19_quiz5-2.pdf`, P1's three bullets, page 1; Spring 2020 Quiz 5, `cs532s20_quiz5.pdf`, same questions under an overprinted 2019/2020 header.

```{index} Disparity; Stereo depth; Depth uncertainty
```

## Turn horizontal shift into axial depth

Assume aligned rectified cameras with a horizontal baseline $b>0$, shared horizontal focal length $f$ in pixels, and matched principal-point columns. Put the left center at $(0,0,0)$ and the right center at $(b,0,0)$.

For a scene point $(X,Y,Z)$, the two horizontal projections obey
$u_L-c_x=fX/Z$ and $u_R-c_x=f(X-b)/Z$. Subtract them: $u_L-u_R=fb/Z$.

````{formula-box} Formula — rectified stereo depth
```{math}
:label: eq-lec04-depth
d=u_L-u_R,\qquad Z=\frac{fb}{d}.
```

$f$ and $d$ use pixels; $Z$ uses the same length unit as $b$. $Z$ is axial depth. Require $d>0$ under this camera order and forward-view convention. If principal-point columns differ, use corrected disparity $d=(u_L-c_{xL})-(u_R-c_{xR})$ instead. A zero disparity is the ideal infinite-depth limit, not a finite reconstruction.
````

```{application} Reconstruct with a known baseline
1. **Input:** rectified correspondence, calibrated pixel focal length, and baseline length.
2. Check equal image rows and subtract horizontal coordinates in the stated order.
3. Compute $Z=fb/d$. Then use [calibrated backprojection](../lecture01/cameras.md) if you also need $X,Y$.
4. **Check:** doubling disparity halves depth; doubling baseline at fixed disparity doubles depth. Keep centimeters and meters consistent.

The source's BAD/GOOD rectification examples (PDF pages 59–60) illustrate that stereo needs compatible row alignment, not independently straightened pictures.
```

```{figure} ../../images/lecture04/stereo-rays.*
:name: fig-lec04-stereo-rays
:width: 90%
:alt: Aligned left and right cameras observe a point. The image projections shift horizontally, and their viewing rays meet at the scene point.

A side view along the horizontal baseline: the difference between two projections fixes the ray intersection's depth. Virtual image planes are drawn in front of the cameras.
```

## A pixel error produces an asymmetric depth error

Let the true disparity be $d$ and the measured disparity $d+\delta$. Define **signed error** as estimated depth minus true depth. Subtract the two depth fractions before approximating.

````{formula-box} Formula — exact and first-order depth error
```{math}
:label: eq-lec04-depth-error
\begin{aligned}
\Delta Z&=\frac{fb}{d+\delta}-\frac{fb}{d}
=-\frac{fb\,\delta}{d(d+\delta)},\\
\Delta Z&\approx-\frac{fb}{d^2}\delta\quad (|\delta|\ll d),\qquad
\frac{|\Delta Z|}{Z}\approx\frac{|\delta|}{d}.
\end{aligned}
```

Require $d>0$ and $d+\delta>0$ for two finite forward-depth estimates. The approximation is the derivative of $fb/d$ times $\delta$. Its magnitude is often quoted without the minus sign; retain the sign when explaining whether the point moves nearer or farther.
````

```{application} Report uncertainty honestly
1. **Input:** $f,b,d$ and a signed disparity error $\delta$.
2. Compute the true and estimated depths; subtract for an exact error.
3. Use the derivative only when $|\delta|/d$ is small; label it an approximation.
4. **Check:** overestimating positive disparity makes depth too small. Underestimating it makes depth too large, by a larger magnitude for equal-size errors.

For bounded error $|\delta|\le\epsilon<d$, the possible depths lie between $fb/(d+\epsilon)$ and $fb/(d-\epsilon)$. If the interval reaches zero disparity, there is no finite upper depth bound under this model.
```

(ex-lec04-stereo-fall)=
````{worked-example} Worked example 4.6 — the one-pixel Fall 2025 question
**Adapted from:** Fall 2025 Quiz 3, Q1.

**Given:** $b=10\,\mathrm{cm}$, $f=50$ pixels, true $d=25$ pixels. Then $fb=500\,\mathrm{cm\,pixels}$ and $Z=500/25=20\,\mathrm{cm}$.

| Measured disparity | Estimated depth | Signed exact error |
| --- | --- | --- |
| $24$ pixels ($\delta=-1$) | $500/24=20.8333\,\mathrm{cm}$ | $+0.8333\,\mathrm{cm}$ |
| $26$ pixels ($\delta=+1$) | $500/26=19.2308\,\mathrm{cm}$ | $-0.7692\,\mathrm{cm}$ |

The first-order magnitude is $500/25^2=0.8\,\mathrm{cm}$. The supplied solution reports this approximation. It is sensible here because $1/25=4\%$, but it is not either exact signed error. “By one pixel” needs a direction or an explicit magnitude convention.
````

(ex-lec04-stereo-spring)=
````{worked-example} Worked example 4.7 — why ±1 pixel is not symmetric
**Adapted from:** Spring 2019 Quiz 5, P1, all three bullets. Spring 2020 Quiz 5 is the closed-notes retest.

**Given:** $b=10\,\mathrm{cm}$, $f=5$ pixels, $d=3$ pixels. True depth is $50/3=16.6667\,\mathrm{cm}$.

1. **Underestimate by one:** measured $d=2$, depth $25\,\mathrm{cm}$, error $25-50/3=25/3\approx+8.3333\,\mathrm{cm}$.
2. **Overestimate by one:** measured $d=4$, depth $12.5\,\mathrm{cm}$, error $12.5-50/3=-25/6\approx-4.1667\,\mathrm{cm}$.
3. **Larger true disparities:** errors do not stay constant. Their magnitudes are $fb/[d(d-1)]$ and $fb/[d(d+1)]$ for one-pixel under/overestimation, respectively. Both decrease as $d$ increases above one.

At $d=3$, a one-pixel error is one third of the true disparity. The linearized magnitude $50/9\approx5.5556\,\mathrm{cm}$ misses the strong asymmetry, so use the exact fractions.
````

## Explore the real 3D geometry

Move the true point in depth, change the camera baseline or focal length, and perturb the measured disparity. The orange point is the truth; the purple point is the estimate from the perturbed right-image match. Orbiting the scene changes only your inspection view.

````{interactive-demo} stereo
**Print/no-JavaScript experiment:** use the two-camera ray diagram above with $b=10\,\mathrm{cm}$, $f=50$ pixels and true $Z=20\,\mathrm{cm}$. The point is centered between the cameras at $X=5\,\mathrm{cm}$. For a principal column $c_x=125$, its projections are $u_L=137.5$ and $u_R=112.5$, giving $d=25$ pixels.

Keep $u_L$ fixed. A disparity error $\delta$ means an observed right column $\widehat u_R=u_R-\delta$. Intersect the left ray with the ray through that perturbed right observation:

| $\delta$ | $\widehat u_R$ | Estimated depth | What happens |
| --- | --- | --- | --- |
| $-1$ pixel | $113.5$ | $20.8333\,\mathrm{cm}$ | Rays meet farther away |
| $0$ | $112.5$ | $20\,\mathrm{cm}$ | Estimate meets the truth |
| $+1$ pixel | $111.5$ | $19.2308\,\mathrm{cm}$ | Rays meet nearer |

At true depth $100\,\mathrm{cm}$, disparity is only $5$ pixels. The same ±1-pixel error gives depths $125$ and $83.3333\,\mathrm{cm}$. Small disparity makes depth fragile. Zero or negative measured disparity does not give a finite forward point in this convention.

```{figure} ../../images/lecture04/depth-sensitivity.*
:name: fig-lec04-depth-sensitivity
:width: 85%
:alt: Depth decreases as disparity increases. A one-pixel interval at disparity five spans a much larger depth range than at disparity twenty-five.

Equal-width disparity errors produce unequal depth errors, especially near zero disparity. This static curve carries the interactive's main result into print.
```
````

## Convert a permitted depth range into search limits

````{formula-box} Formula — disparity search from a depth interval
```{math}
:label: eq-lec04-disparity-range
0<Z_{\min}\le Z\le Z_{\max}
\quad\Rightarrow\quad
\frac{fb}{Z_{\max}}\le d\le\frac{fb}{Z_{\min}}.
```

The inequalities reverse because depth and positive disparity are inversely related. Use consistent length units and the corrected disparity convention when principal points differ.
````

```{application} Limit the stereo search
1. Convert $b,Z_{\min},Z_{\max}$ to the same length unit.
2. Compute the continuous disparity endpoints.
3. For integer hypotheses inside that interval, use the ceiling of the lower endpoint and floor of the upper endpoint. If subpixel or calibration uncertainty matters, include an appropriate margin before discretizing.
4. Check that the larger disparity belongs to the nearer depth.
```

(ex-lec04-search)=
```{worked-example} Worked example 4.8 — restrict the Fall 2025 search
**Adapted from:** Fall 2025 Quiz 3, Q2.

Use $b=0.1\,\mathrm m$, $f=50$ pixels, and depth range $[1,5]\,\mathrm m$. Then $fb=5\,\mathrm{m\,pixels}$, so $d_{\min}=5/5=1$ pixel and $d_{\max}=5/1=5$ pixels. Search integer disparities $1,2,3,4,5$, or subpixel values in that interval.

For a left column $u_L$, candidates are at $u_R=u_L-d$ on the matching row. Also clip the search to valid image coordinates; a geometrically permitted match can still fall outside the image.
```
