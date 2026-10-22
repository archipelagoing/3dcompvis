(lec02-warping)=
# Image warping: where do the new pixels come from?

Mapping a point is not enough to create an image. Source pixels lie on a grid; transformed positions usually fall between destination pixels. We need a rule for filling the destination grid.

**Source:** PDF pages 72–81, printed slides 73–82; the section credits Steve Seitz.

## Move colors, or look them up?

**Image filtering** changes pixel values at fixed coordinates, such as darkening a picture. **Image warping** changes where the content appears. A global parametric warp uses the same coordinate function everywhere, though its displacement can vary with position.

```{figure} ../../images/lecture02/warp-grids.*
:name: fig-lec02-warp-grids
:width: 100%
:alt: Forward mapping places source pixels at uneven destination positions; inverse mapping starts from every output grid point.

Forward mapping asks where each source pixel lands. Inverse mapping asks where each output pixel should sample. Original diagram of the distinction on PDF pages 76–79.
```

````{formula-box} Formula — inverse image sampling
```{math}
:label: eq-lec02-inversewarp
g(u',v')=f\!\left(\operatorname{dehom}\bigl(H^{-1}(u',v',1)^T\bigr)\right).
```

$f$ is the source image, $g$ the output; $H$ maps **source to destination**. The operator $\operatorname{dehom}$ divides the first two coordinates by the last. Pixel values may be grayscale scalars or color vectors. This describes continuous sampling; discrete images require interpolation and a boundary rule.
````

```{application} Fill an output image
1. Visit every output pixel center and multiply by $H^{-1}$.
2. Divide by the homogeneous denominator; mark invalid/out-of-source samples as background.
3. Interpolate the source image and store that value.

This avoids holes caused by rounded forward placement. Forward warping is still useful when samples must be projected or splatted. When shrinking an image substantially, prefilter it to reduce aliasing; interpolation alone is insufficient.
```

## Bilinear interpolation: blend four neighbors

Suppose inverse mapping returns source location $(i+a,j+b)$, where $i,j$ are integers and $0\le a,b<1$. First interpolate horizontally in each row, then vertically between those results.

````{formula-box} Formula — bilinear interpolation
```{math}
:label: eq-lec02-bilinear
\begin{aligned}
f(i+a,j+b)\approx{}&(1-a)(1-b)f(i,j)+a(1-b)f(i+1,j)\\
&+(1-a)b f(i,j+1)+ab f(i+1,j+1).
\end{aligned}
```

$a,b$ are unitless fractions of a pixel; the output has the same intensity units as the samples. We write coordinates as $(\text{column},\text{row})$; an image array usually indexes $f[\text{row},\text{column}]$. The four weights are nonnegative and sum to one. Specify how samples outside the image are handled.
````

```{application} Calculate a sampled intensity
1. Take the floor of each continuous coordinate to find $i,j$.
2. Compute $a,b$ and the four weights.
3. Blend each image channel separately.

Check that a constant patch remains constant and that integer coordinates reproduce the stored pixel. See Example 2.3.
```

(ex-lec02-bilinear)=
```{worked-example} Worked example 2.3 — a pixel between pixels
**Source:** original numerical companion to PDF page 80, printed slide 81.

The four intensities at $(i,j),(i+1,j),(i,j+1),(i+1,j+1)$ are $10,30,50,70$. At $a=1/4$, $b=1/2$, the weights are $3/8,1/8,3/8,1/8$.

The sampled value is $(3\cdot10+30+3\cdot50+70)/8=35$. Equivalently, the two horizontal interpolations give $15$ and $55$, whose halfway blend is $35$. It lies within the range of the four inputs.
```

```{understanding-check} Check 2.2 — which inverse?
If $H$ shifts source content ten pixels right, where does output pixel $(20,8)$ sample?
```

```{admonition} Answer
:class: dropdown
At source $(10,8)$. Using $H$ instead of $H^{-1}$ would sample $(30,8)$ and move content in the wrong direction.
```

```{index} inverse warping
```

```{index} bilinear interpolation
```
