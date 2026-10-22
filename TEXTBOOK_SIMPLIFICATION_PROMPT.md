# Revision prompt: concise, beginner-friendly CS 532 textbook

## Task

Revise the textbook into an approachable, “For Dummies”-level learning guide: plain English, clear mathematics, useful pictures, and worked problems. Assume the reader has taken the prerequisites but is new to 3D computer vision.

**Use the fewest words that explain the idea properly.** Remove unnecessary information, repetition, and academic padding. Keep the steps that make difficult reasoning understandable. Concise means efficient teaching, not unexplained formulas or compressed jargon.

Apply this style to all currently written textbook content, including reference pages. Use it for future lectures when they are authorized. Keep unwritten chapters clearly labeled; this revision does not authorize filling them or advancing past an existing lecture-review checkpoint.

## Read first and resolve conflicts

- `TEXTBOOK_PROMPT.md`: subject coverage, visuals, quiz integration, and shared web/LaTeX requirements.
- `ExamToDo.md`: emphasis, required gaps, and mathematical qualifications.
- `3dcvMid/lectures/quizByLec.md`: quiz placement and overlaps.
- `todo.md`, `authoring/STYLE_GUIDE.md`, and the source/coverage registers.
- The relevant slides and quizzes when checking or changing their explanations.

This prompt governs **brevity, reading level, and presentation** wherever an earlier instruction would produce excessive detail or a rigid, repetitive section structure. Preserve mathematical correctness, relevant lecture coverage, quiz assignments, attribution, and printable completeness.

## What belongs in the book?

Keep material that helps the reader understand a relevant concept, interpret a required formula, solve an assigned problem, or avoid a likely mistake. Use the slide and quiz priorities to decide how much space it deserves.

- Keep all relevant lecture topics and formulas accounted for in the coverage register.
- Keep the required exam-gap topics and their worked problems.
- Keep distinct, relevant quiz questions integrated beside the concepts they test.
- Use the strongest slide example or image when it genuinely explains the idea.
- Remove invented extensions, historical background, tangents, repeated reminders, and extra examples that add no new understanding.
- Consolidate repeated topics and duplicate quiz exposition. Preserve duplicate quizzes as short retest references.
- Give lower-priority material proportionately less space. Never omit a necessary topic merely because its mathematics is difficult.

Do not turn the book into a collection of optional extras. Use a short **Going deeper** subsection only when a longer derivation or subtle qualification is useful but would interrupt the first reading. If a detail has no clear learning purpose, remove it rather than relocating it.

## How to explain difficult material

1. **Say the idea plainly.** Start with the question being solved and a direct explanation. Use a short everyday analogy only if it clarifies the actual geometry.
2. **Show the formula.** Define unfamiliar symbols beside it. State units, coordinate conventions, and essential conditions briefly.
3. **Make it usable.** Give the shortest reliable application procedure and a small worked calculation.
4. **Connect to the quiz.** Use the assigned problem as the worked example whenever possible; add a separate toy example only when the quiz is too difficult for a first encounter.

Explain why a dense mathematical step works in one or two direct sentences. Show intermediate algebra when skipping it would hide an important idea. Combine routine substitutions that the prerequisite-trained reader can follow. Expand an unfamiliar operation locally instead of sending the reader through several prerequisite pages.

Use accurate explanations such as “The cross product gives a direction perpendicular to both vectors.” Avoid substituting jargon such as “apply the dual-space incidence operator” for an explanation. Introduce the technical name after its meaning is clear.

## Formula boxes and companion procedures

Retain the existing `formula-box` and `application` directives and stable equation labels. Each substantive formula has one canonical teaching location; later uses link back to it.

Keep the pair compact:

| Formula box | Companion procedure |
| --- | --- |
| Short descriptive name and numbered equation | What the reader wants to find |
| Symbols and units, preferably one compact line or small table | Required inputs |
| Meaning in one or two sentences | Usually 2–4 numbered steps |
| Essential assumptions and the most relevant limitation | Output, quick check, and worked-example link |

Use as many steps as correctness requires; these are guides, not quotas. The companion should explain application, not repeat the formula box in prose. For an identity or constraint, give an interpretation/checking procedure rather than inventing an algorithm.

Keep sign conventions, transform directions, zero denominators, and other conditions that can change the answer next to the formula. Put lengthy proofs or rare numerical edge cases in **Going deeper** only when needed. Keep intermediate algebra outside boxes.

## Readable formatting

- Use short paragraphs, usually 2–4 sentences, with one main idea each.
- Use clear, descriptive headings. Avoid a new heading or box for every sentence.
- Bold key terms on first definition and a few important conclusions. Retain glossary links and index entries without highlighting entire paragraphs.
- Use bullets for parallel ideas, numbered lists for procedures, and tables for comparisons. Keep lists shallow.
- Prefer one well-explained figure to several near-duplicates. Captions should tell the reader what to notice.
- Keep source citations precise but quiet: use short source notes or footnotes, with full filenames and verified page references in the source register/reference section. Retain necessary figure attribution without repeating long provenance paragraphs in the exposition.
- Remove authoring/build details from student-facing prose. Keep them in authoring documentation.
- Keep solutions accessible online and fully available in print. Avoid repetitive “what to remember” sections when they merely restate the preceding paragraph.

Do not force every section to contain a hook, analogy, diagram, derivation, toy problem, quiz problem, exercise, warning, and summary. Choose the pieces that make that topic clear.

## Example of the intended voice

**Too formal:** “The inverse homogeneous transformation requires inversion of the rotational block and appropriate transformation of the translation component.”

**Better:** “To undo the motion, subtract the translation first, then undo the rotation. A rotation's inverse is its transpose.”

Then show the actual calculation with defined inputs:

> If the forward rule is \(p'=Rp+t\), the reverse rule is \(p=R^T(p'-t)\). Here \(p,p'\) are point coordinates, \(R\) is the rotation, and \(t\) is the translation. Subtract \(t\), multiply by \(R^T\), and check that you recover the original point.

Be direct and encouraging. Avoid baby talk, forced jokes, exaggerated enthusiasm, and claims that difficult material is “obvious” or “easy.”

## Revision workflow

1. Review the written material lecture by lecture. Identify repeated explanations, unnecessary extras, source-heavy interruptions, and dense passages needing a clearer explanation.
2. Rewrite the main learning path using this prompt. Preserve or update stable labels, formula/example numbering, images, references, and quiz mappings.
3. Check every cut against the coverage register. Record deliberate consolidation or relocation; keep required topics, assumptions, and worked reasoning.
4. Update the glossary, formula reference, quiz index, and authoring conventions to match. Do not create repetitive new summaries or large “optional” appendices to compensate for cuts.
5. Build both editions from the same Markdown source. Use `BUILDING.md`; do not edit the generated LaTeX independently.
6. Check mathematics affected by the rewrite, web rendering, image placement, references, PDF readability, and visible print solutions. Run the existing numerical checks where relevant.
7. Report the before/after prose length, what was consolidated, and any real coverage changes. Measure prose separately from Markdown directives/equations where practical. Do not chase a fixed reduction percentage or claim concision without reviewing the result.

Prepare the revision locally. Publish only when authorized. Follow existing review checkpoints before advancing to another unwritten lecture.

## Acceptance check

- Can a prerequisite-trained beginner explain each main idea after reading it once?
- Can they identify what a formula does and how to use it without searching several pages?
- Does each dense step have a short, accurate explanation?
- Are the relevant topics, formulas, quiz examples, and essential conditions preserved?
- Does every paragraph, figure, example, and optional detail earn its space?
- Are both the website and PDF readable, complete for the written scope, and synchronized?

If a passage is shorter but harder to understand, revise it again.

## One-line invocation

“Apply `TEXTBOOK_SIMPLIFICATION_PROMPT.md` to all currently written textbook content. Preserve required coverage and quiz integration, remove unnecessary detail, and rebuild the web and LaTeX/PDF editions.”
