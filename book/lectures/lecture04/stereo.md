(lec04-stereo)=
# Stereo depth, sensitivity and worked error examples

Hold a finger in front of your face and close one eye at a time. Its apparent horizontal shift is larger when it is close. **Disparity** measures that shift in a rectified camera pair.

**Quick route:** {ref}`derive depth <stereo-derive-depth>`, [understand sensitivity](#stereo-depth-sensitivity), [Fall quiz: ±1 pixel](#ex-lec04-stereo-fall), [Spring quiz: larger errors](#ex-lec04-stereo-spring), [3D explorer](#stereo-explorer), [depth range → search range](#ex-lec04-search).

**Sources:** lecture PDF pages 58–64; Fall 2025 Quiz 3, `cs532f25_quiz_3_solution.pdf`, Q1–Q2, page 1; Spring 2019 Quiz 5, `cs532s19_quiz5-2.pdf`, P1's three bullets, page 1; Spring 2020 Quiz 5, `cs532s20_quiz5.pdf`, same questions under an overprinted 2019/2020 header.

```{index} Disparity
```

```{index} Stereo depth
```

```{index} Depth uncertainty
```

(stereo-derive-depth)=
## Turn horizontal shift into axial depth

Assume aligned rectified cameras with a horizontal baseline $b>0$, shared horizontal focal length $f$ in pixels, and matched principal-point columns. Put the left center at $(0,0,0)$ and the right center at $(b,0,0)$.

For a scene point $(X,Y,Z)$, the left camera sees horizontal position $X$, while the right camera sees $X-b$ relative to its own center. Perspective divides each by the same depth:

$$u_L-c_x=\frac{fX}{Z},\qquad u_R-c_x=\frac{f(X-b)}{Z}.$$

**Subtract the right observation from the left.** The principal point cancels, then the unknown $X$ cancels:

$$
\begin{aligned}
d&=(u_L-c_x)-(u_R-c_x)\\
&=\frac{fX}{Z}-\frac{f(X-b)}{Z}
=\frac{fX-fX+fb}{Z}=\frac{fb}{Z}.
\end{aligned}
$$

Multiply both sides by $Z$, giving $dZ=fb$. Divide by positive $d$: **$Z=fb/d$**. This is why the horizontal shift alone can recover depth once the cameras are calibrated.

````{formula-box} Formula — rectified stereo depth
```{math}
:label: eq-lec04-depth
d=u_L-u_R,\qquad Z=\frac{fb}{d}.
```

$f$ and $d$ use pixels; $Z$ uses the same length unit as $b$. $Z$ is axial depth. Require $d>0$ under this camera order and forward-view convention. If principal-point columns differ, use corrected disparity $d=(u_L-c_{xL})-(u_R-c_{xR})$ instead. A zero disparity is the ideal infinite-depth limit, not a finite reconstruction.
````

```{raw} latex
\Needspace{12\baselineskip}
```

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

(stereo-depth-sensitivity)=
## Stereo depth sensitivity: why one pixel matters

**Faraway points barely move between the two images.** Their disparity is small, so one pixel is a large fraction of the signal. Nearby points have a larger shift and tolerate the same pixel error better.

Let the true disparity be $d$ and the measured disparity $d+\delta$. Here $\delta$ is a **disparity error**, not automatically the error in one particular image coordinate. Since $d=u_L-u_R$, measurement errors $\epsilon_L,\epsilon_R$ give $\delta=\epsilon_L-\epsilon_R$. If the left coordinate is held fixed, a right-coordinate error has the opposite sign to $\delta$.

Define **signed depth error** as estimated depth minus true depth. Start with the two depths, give their fractions a common denominator, and simplify:

$$
\begin{aligned}
\Delta Z&=\widehat Z-Z=\frac{fb}{d+\delta}-\frac{fb}{d}\\
&=\frac{fb\,d-fb(d+\delta)}{d(d+\delta)}\\
&=\frac{fb\,d-fb\,d-fb\,\delta}{d(d+\delta)}
=-\frac{fb\,\delta}{d(d+\delta)}.
\end{aligned}
$$

**Read the sign:** $\delta>0$ means too much disparity and an estimate too near ($\Delta Z<0$). $\delta<0$ means too little disparity and an estimate too far ($\Delta Z>0$), provided measured disparity stays positive.

````{formula-box} Formula — exact and first-order depth error
```{math}
:label: eq-lec04-depth-error
\begin{aligned}
\Delta Z&=\frac{fb}{d+\delta}-\frac{fb}{d}
=-\frac{fb\,\delta}{d(d+\delta)},\\
\Delta Z&\approx-\frac{fb}{d^2}\delta\quad (|\delta|\ll d),\qquad
\frac{|\Delta Z|}{Z}\approx\frac{|\delta|}{d},\\
\left|\frac{dZ}{dd}\right|&=\frac{fb}{d^2}=\frac{Z^2}{fb}.
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

### Understand the approximation, not just the formula

Write $Z=fb\,d^{-1}$. Differentiating with respect to disparity gives

$$\frac{dZ}{dd}=fb(-d^{-2})=-\frac{fb}{d^2}.$$

A derivative is the **local slope**: approximately how much depth changes for a small change in disparity. Multiply this slope by $\delta$ to get $\Delta Z\approx-fb\delta/d^2$. Its units are length per pixel times pixels, giving length.

You can also see the approximation without calculus. If $|\delta|$ is much smaller than $d$, replace the exact denominator $d(d+\delta)$ by $d^2$. Dividing the resulting error magnitude by $Z=fb/d$ gives

$$\frac{|\Delta Z|}{Z}\approx
\frac{fb|\delta|}{d^2}\frac{d}{fb}=\frac{|\delta|}{d}.$$

**A 1-pixel error at 25 pixels is roughly a 4% depth error. At 5 pixels it is roughly 20%.** Close to zero disparity, this approximation becomes unreliable; use the exact depths instead.

### Why distance makes sensitivity grow so quickly

Substitute $d=fb/Z$ into the slope magnitude:

$$\left|\frac{dZ}{dd}\right|
=\frac{fb}{(fb/Z)^2}=\frac{Z^2}{fb}.$$

At fixed focal length and baseline, **double the true depth → about four times the absolute error** for the same small disparity error. At fixed true depth, a larger baseline or longer pixel focal length reduces this local sensitivity. A larger baseline also makes occlusions and matching more difficult; geometry alone does not guarantee a usable correspondence.

For $f=50$ pixels and $b=10\,\mathrm{cm}$, so $fb=500$:

| True depth | True disparity | Depth if disparity is 1 pixel too small | Depth if disparity is 1 pixel too large | Local sensitivity |
| --- | --- | --- | --- | --- |
| $20\,\mathrm{cm}$ | $25$ px | $20.8333\,\mathrm{cm}$ | $19.2308\,\mathrm{cm}$ | $0.8\,\mathrm{cm/px}$ |
| $40\,\mathrm{cm}$ | $12.5$ px | $43.4783\,\mathrm{cm}$ | $37.0370\,\mathrm{cm}$ | $3.2\,\mathrm{cm/px}$ |
| $100\,\mathrm{cm}$ | $5$ px | $125\,\mathrm{cm}$ | $83.3333\,\mathrm{cm}$ | $20\,\mathrm{cm/px}$ |

For example, the last row uses $d=500/100=5$, then $500/(5-1)=125$ and $500/(5+1)=83.3333$. The exact errors are **$+25$ and $-16.6667\,\mathrm{cm}$**, despite equal one-pixel disparity errors.

### A bounded error gives a depth interval

Suppose $d=5$ pixels and the disparity error is at most $0.5$ pixel. With $fb=500$, the permitted measured disparities are $[4.5,5.5]$. Because larger disparity means smaller depth, reverse the endpoints:

$$\widehat Z\in
\left[\frac{500}{5.5},\frac{500}{4.5}\right]
=[90.9091,111.1111]\,\mathrm{cm}.$$

Relative to the true depth $100\,\mathrm{cm}$, the errors lie in $[-9.0909,+11.1111]\,\mathrm{cm}$. The derivative estimate would give approximately $\pm10\,\mathrm{cm}$. A bound is an interval, not a probability statement. If permitted disparity reaches zero, finite upper depth is no longer bounded.

**Worked example 4.6 — the one-pixel Fall 2025 question.** {ref}`Read the original problem and every worked step <quiz-4-q1>`.

**Worked example 4.7 — why ±1 pixel is not symmetric.** {ref}`Read the original problem and every worked step <quiz-5-q1>`.

(stereo-explorer)=
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

**Worked example 4.8 — restrict the Fall 2025 search.** {ref}`Read the original problem and every worked step <quiz-4-q2>`.
