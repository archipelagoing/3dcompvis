(lec03-ransac-practice)=
# Probability and the pentagon puzzle

**How many random tries are enough?** First ask what counts as a successful try. RANSAC's trial budget depends on that definition and on how samples are drawn.

**Sources:** lecture PDF pages 46–55; Fall 2025 Quiz 1, `cs532f25_quiz_1_solution.pdf`, Q1–Q2, PDF page 1; Spring 2019 Quiz 3, `cs532s19-quiz3.pdf`, P1's four bullets, PDF page 1. The general RANSAC algorithm and trial-count formula remain in [Lecture 2](../lecture02/estimation.md).

## Start with the coin quiz

**Worked example 3.6 — a winning streak, then repeated attempts.** {ref}`Read the original problem and every worked step <quiz-17-q1>`.

## Five corners, twenty-five possible matches

Assume two pictures show only a generic irregular pentagon. All five corners are detected, but their identities are unknown. The quiz asks you to try **every possible pairing**.

**Worked example 3.7 — count matches and budget the search.** {ref}`Read the original problem and every worked step <quiz-7-q1>`.

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

**Worked example 3.8 — replace the shape with a regular pentagon.** {ref}`Read the original problem and every worked step <quiz-7-q1>`.

```{figure} ../../images/lecture03/pentagon-symmetry.*
:name: fig-lec03-pentagon
:width: 85%
:alt: Three identical regular pentagons show one original corner ordering, a rotated ordering, and a reflected ordering; the outlines are indistinguishable.

The numbers are explanatory labels, not visible features in the quiz images. The identical outlines cannot tell you which ordering is intended.
```

```{understanding-check} What does your confidence actually mean?
Before quoting “99%,” finish the sentence: “a 99% chance of drawing at least one ___, under the sampling assumption ___.” If your answer says “a 99% chance the reconstruction is right,” you have claimed more than the calculation supports.
```
