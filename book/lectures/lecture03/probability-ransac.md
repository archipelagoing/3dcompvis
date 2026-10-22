(lec03-ransac-practice)=
# Probability and the pentagon puzzle

**How many random tries are enough?** First ask what counts as a successful try. RANSAC's trial budget depends on that definition and on how samples are drawn.

**Sources:** lecture PDF pages 46–55; Fall 2025 Quiz 1, `cs532f25_quiz_1_solution.pdf`, Q1–Q2, PDF page 1; Spring 2019 Quiz 3, `cs532s19-quiz3.pdf`, P1's four bullets, PDF page 1. The general RANSAC algorithm and trial-count formula remain in [Lecture 2](../lecture02/estimation.md).

## Start with the coin quiz

(ex-lec03-probability)=
````{worked-example} Worked example 3.6 — a winning streak, then repeated attempts
**Adapted from:** Fall 2025 Quiz 1, Q1–Q2.

**Q1:** You must win three independent fair coin flips in a row. Each flip has win probability $1/2$, so one complete attempt succeeds with probability

$$q=(1/2)^3=1/8.$$

**Q2:** Make one independent attempt each day for seven days. What is the probability of at least one successful day?

It is easier to count **no wins**. Each day fails with probability $7/8$. All seven days fail with probability $(7/8)^7$. Subtract from one:

$$P(\text{at least one win})=1-(7/8)^7\approx0.607304=60.73\%.$$

Seven attempts do not give probability $7/8$: that addition counts overlapping success events repeatedly. The complement calculation handles all possible numbers of wins at once.

**Connection:** a RANSAC hypothesis needs several good matches together, just as this attempt needs several wins together. Repeating hypotheses then uses the same “one minus all failures” reasoning. The quiz's geometry questions are solved in [Lecture 1](../lecture01/frames-quizzes.md).
````

## Five corners, twenty-five possible matches

Assume two pictures show only a generic irregular pentagon. All five corners are detected, but their identities are unknown. The quiz asks you to try **every possible pairing**.

(ex-lec03-pentagon)=
````{worked-example} Worked example 3.7 — count matches and budget the search
**Adapted from:** Spring 2019 Quiz 3, P1, first three bullets.

1. **Putative matches:** each of five source corners can pair with any of five destination corners: $5\times5=25$ candidate pairs.
2. **Correct matches:** relative to the intended homography, one partner per source corner is correct: five pairs. The inlier fraction is $w=5/25=0.2$.
3. **Minimal homography sample:** four nondegenerate correspondences. Under the usual independent-match approximation, a clean sample has probability $q=w^4=0.0016$.
4. **Choose confidence:** the question does not give one. Taking $p=0.99$ and applying {eq}`eq-lec02-ransac` gives

$$
N=\left\lceil\frac{\log(0.01)}{\log(1-0.0016)}\right\rceil
=2876.
$$

**Interpretation:** under this model, 2,876 trials give about a 99% chance of drawing at least one all-inlier sample. This does not guarantee a correct final homography: samples must also be nondegenerate, and scoring must distinguish the intended model.
````

### The small-pool qualification

Here the pool is unusually small. Four independent draws are an approximation to a real four-correspondence sampler. If asked for an **exact** count, specify the sampling rule.

Let $q$ denote the probability that **one counted trial** is clean. Assuming independent trials and a generic pentagon with no three corners collinear:

| Sampling rule for one counted trial | Clean-sample probability $q$ | Trials for 99% |
| --- | --- | --- |
| Independent inlier-status approximation | $(5/25)^4=0.0016$ | 2,876 |
| Four distinct pairs drawn uniformly from all 25; count even invalid samples | $\binom54/\binom{25}4=1/2530$ | 11,649 |
| Reject repeated source or destination corners; count only valid four-pair samples | $5/[\binom54^2\,4!]=1/120$ | 551 |

Why the last denominator? Choose four of five source corners, four of five destination corners, then one of $4!$ bijections: $5\times5\times24=600$ valid sets. Only five are subsets of the intended five matches. These are different experiments, so their trial counts need not agree. If rejected draws consume runtime, include their cost separately.

**For an exam:** state the standard $w^4$ assumption before giving 2,876. If the sampling procedure is specified more precisely, use its corresponding $q$ in the same complement-probability calculation.

## Try the sampling experiment

Change the inlier percentage and trial count. Blue dots are good matches; orange dots are bad. Four blue dots make a clean hypothesis. The display compares the predicted chance of **at least one** clean sample with results from 200 simulated experiments.

````{interactive-demo} ransac
**Static experiment:** assume four independently drawn match statuses per hypothesis. Then $q=w^4$ and $P=1-(1-q)^N$. The simulator uses this approximation, not the exact finite-pool pentagon samplers above.

| Inlier fraction $w$ | Trials $N$ | Chance of at least one clean sample |
| --- | --- | --- |
| 20% | 100 | $1-(1-0.2^4)^{100}=14.80\%$ |
| 20% | 2,876 | $1-(1-0.2^4)^{2876}=99.0001\%$ |
| 50% | 72 | $1-(1-0.5^4)^{72}=99.04\%$ |

A single experiment can succeed or fail. Across many independent experiments, the observed success fraction tends toward the predicted probability; it need not equal it exactly. A clean sample is a sampling event, not proof of a correct model.

```{figure} ../../images/lecture03/ransac-probability.*
:name: fig-lec03-probability
:width: 85%
:alt: Success probability rises slowly with trial count at twenty percent inliers and much faster at fifty percent; ninety-nine percent is marked.

More inliers can reduce the required trial count dramatically. The vertical axis measures sampling success, not geometric accuracy.
```
````

## More trials cannot solve a symmetry

```{index} Symmetry ambiguity
```

(ex-lec03-symmetry)=
````{worked-example} Worked example 3.8 — replace the shape with a regular pentagon
**Adapted from:** Spring 2019 Quiz 3, P1, final bullet.

A regular pentagon has five rotations that map its corner set onto itself. It also has five reflections. Composing the true image homography with any of these symmetries gives another homography supported by all five corners.

- With no orientation restriction, there are **ten equally supported corner alignments**.
- If an external orientation constraint rules out reflections, **five rotations** remain.
- A visible distinctive mark, corner identity, or other asymmetric evidence can break the tie. More random samples of the same unlabeled corners cannot.

The 20% inlier rate is measured relative to **one selected alignment**. Do not combine the ten alignments into one larger consensus: they are different models.

**Source wording:** the quiz calls a regular pentagon “equilateral.” Equal side lengths alone do not imply equal angles or these ten symmetries. This answer assumes a genuinely **regular** pentagon, as the question names it.
````

```{figure} ../../images/lecture03/pentagon-symmetry.*
:name: fig-lec03-pentagon
:width: 85%
:alt: Three identical regular pentagons show one original corner ordering, a rotated ordering, and a reflected ordering; the outlines are indistinguishable.

The numbers are explanatory labels, not visible features in the quiz images. The identical outlines cannot tell you which ordering is intended.
```

```{understanding-check} What does your confidence actually mean?
Before quoting “99%,” finish the sentence: “a 99% chance of drawing at least one ___, under the sampling assumption ___.” If your answer says “a 99% chance the reconstruction is right,” you have claimed more than the calculation supports.
```
