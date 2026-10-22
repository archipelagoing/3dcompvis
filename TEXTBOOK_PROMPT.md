# Implementation prompt: CS 532 illustrated textbook and printable LaTeX edition

## Objective

Turn the existing TeachBook in `book/` into a coherent, professional, illustrated textbook covering the six lecture PDFs in `3dcvMid/lectures/`. Use the lectures as the syllabus and the quizzes as the backbone of integrated worked examples. Write connected explanations, derivations, and transitions rather than transcribing slide bullets or embedding entire slide decks.

Produce both a polished TeachBooks website and a complete, ordinary textbook PDF from a maintained, easily compilable LaTeX manuscript. These are two editions of the same book and must stay synchronized.

## Read these sources first

- `ExamToDo.md`: authoritative guide to exam emphasis, quiz ranking, required gap topics, errata, and duplicate-retest intent. Its relevance scores are **not predictions of exam probability**.
- `todo.md`: implementation checklist; complete one lecture at a time in order, from Lecture 1 through Lecture 6.
- `3dcvMid/lectures/quizByLec.md`: primary quiz-to-lecture mapping and secondary overlaps. Integrate the assigned quizzes beside relevant concepts and use the strongest actual examples from each lecture's slides.
- All six lecture PDFs in `3dcvMid/lectures/`, plus `lecdirec.md` for the lecture mapping. Later lectures listed in that directory document are outside the core scope.
- `3dcvMid/quizzesf25sol/` and `3dcvMid/olderquizzes/`.
- The existing `book/_toc.yml`, `book/_config.yml`, requirements, and deployment workflow.
- If present, `CS532_18_Quizzes_Step_by_Step.tex` and its PDF, referenced by `ExamToDo.md`. Locate and inspect them; do not assume they exist or silently claim to have read them.

Inspect PDF pages visually when equations, diagrams, or extraction quality require it. Preserve original filenames and record printed titles separately where they disagree. Do not treat extracted PDF text as an infallible transcription of mathematics.

## Editorial architecture

Start with six major chapters aligned to Lectures 1–6, subdivided into readable topic pages. The concept outline below is provisional: verify full slide coverage before fixing boundaries, especially the overlap between Lectures 1 and 2, and align the final chapter titles and quiz placement with `quizByLec.md` and the actual PDFs.

| Chapter | Core topics | Quiz integration |
| --- | --- | --- |
| Geometry foundations | Homogeneous coordinates, points and lines, incidence, projective intersections, points at infinity | Collinearity tests and parallel-line intersections |
| Transformations and 3D geometry | Coordinate frames, rigid transformations, projective transformations, 3D points and planes | Relative camera pose through a shared object; plane normals |
| Image formation and homographies | Pinhole model, intrinsics/extrinsics, field of view, planar mappings, DLT, robust estimation | Calibration matrices, projection dimensions, pentagon matching and RANSAC |
| Two-view geometry | Distortion, epipolar geometry, fundamental/essential matrices, relative pose, triangulation, rectified stereo | Epipolar lines, three-view correspondence, disparity/depth errors and search bounds |
| Features and matching | Gradients, structure tensor, Harris, Lucas–Kanade/KLT, descriptors and matching | Tracking corners versus edges; exposure changes |
| Structure from motion | Reconstruction ambiguity, affine factorization, sequential/incremental reconstruction, bundle adjustment | Reconstruction upgrades and weak-overlap capture scenarios |

Include a notation guide, prerequisite refresher, formula reference with assumptions, source/figure credits, and a quiz practice index. Use cross-references when a topic serves multiple chapters rather than repeating its full explanation.

Establish consistent conventions for homogeneous equality, coordinate frames, transform direction, camera centers, translation, pixel versus normalized coordinates, and units. Clearly distinguish exact results, approximations, and special cases.

## Exam priorities

Use the teaching sequence above for the main book, while making the study priorities in `ExamToDo.md` accessible through a study route and practice index.

1. Emphasize Lecture 3–4 mathematics: epipolar lines and constraints, stereo depth and exact versus approximate error, homography correspondences, RANSAC probability, and polygon symmetry.
2. Give substantial attention to homogeneous geometry, camera calibration, brightness constancy, tracking solvability, and coordinate reasoning.
3. Cover SfM upgrades and factorization carefully; label advanced transfer problems according to their prerequisites and scope.

Explicitly cover the seven gaps identified in `ExamToDo.md`, each with a derivation and at least one new worked numerical or reasoning problem:

- Homography DLT, the `2n × 9` system, SVD, and normalized DLT (L3 slides 34–45).
- Harris gradient sums, structure tensor, eigenvalues, determinant/trace response, and non-maximum suppression (L5 slides 11–30).
- Lucas–Kanade linearization, least-squares system, displacement, and aperture problem (L5 slides 39–50).
- Essential matrix, calibration relationship, singular-value constraints, four candidate poses, and cheirality (L4 slides 22–41).
- Linear triangulation and SVD nullspace recovery (L6 slides 48–52).
- Bundle-adjustment residuals, Jacobians, gauge freedom, and Gauss–Newton/LM updates (L6 slides 46, 62–70).
- Centered measurement matrices, rank-three affine factorization, and affine/metric ambiguity (L6 slides 25–37).

Verify the cited slide ranges against the actual PDFs; distinguish PDF page numbers from printed slide numbers.

## Section teaching pattern

Use this pattern where it supports learning, without making every section mechanically identical:

1. Introduce a concrete visual problem and learning objectives.
2. Explain the geometry intuitively before introducing algebra.
3. Define all symbols and assumptions.
4. Derive the key result with meaningful intermediate steps.
5. Solve a relevant quiz example immediately beside the concept it tests.
6. Offer a short independent exercise, with a collapsible solution online and a visible solution or explicit solution reference in print.
7. Explain common mistakes, degeneracies, and a concise takeaway.

Use full prose, numbered equations where referenced, descriptive figure captions, and consistent example/exercise numbering. Make solutions detailed enough for independent study.

## Clarity, formula coverage, and learning support

Write at a strong high-school reading level for a student who has completed the course prerequisites but is encountering 3D computer vision for the first time. Preserve the full mathematical rigor and scope of the lectures. Make dense mathematics accessible through plain-language interpretations, explicit intermediate steps, and small numerical examples. Briefly refresh prerequisite ideas such as matrix multiplication, dot/cross products, derivatives, eigenvalues, and SVD when first needed; link to the prerequisite refresher for additional detail. Expand acronyms on first use and explain technical terms in plain language. Do not assume that a short statement in a slide is self-explanatory.

- Develop each substantial concept through intuition → definitions → labeled diagram where useful → mathematical formulation → derivation → worked example → independent practice.
- Show intermediate algebra, substitutions, matrix dimensions, and coordinate conversions. Explain why each meaningful step is valid; avoid skipping reasoning with phrases such as “clearly” or “it follows” when a student would need an explanation.
- For each important formula, give its purpose, define every symbol, state scalar/vector/matrix dimensions and units where applicable, and identify its coordinate conventions.
- Explain when to use the formula, its assumptions, when it fails or becomes degenerate, and whether it is exact or approximate. Connect it to a worked example and an intuitive interpretation of the result.
- For algorithms, explain the inputs, outputs, numbered procedure, governing equations, and failure cases. Include a small numerical walkthrough where it improves understanding.
- Address likely misconceptions explicitly, and use a simple case before extending to the general case.
- Label essential exam material and supplementary extensions consistently, using `ExamToDo.md` for emphasis without omitting relevant lecture content.
- Maintain a coverage ledger of all substantive lecture topics and formulas, with source PDF/slide/page and destination section/equation. Account explicitly for duplicates, administrative slides, and out-of-scope material; do not silently omit difficult topics.
- End each chapter with a topic-and-formula checklist linked to its explanations, worked examples, and source lecture pages. Include the same references as readable section/equation numbers in print.
- Make the consolidated formula reference useful for problem solving: include purpose, assumptions, symbol definitions or a precise notation reference, and links back to the full derivation and example.

## Engagement, pacing, and readable formatting

Combine the approachable, easy-to-scan presentation of a clear conversational explanation with professional textbook structure. Keep connected reasoning intact and use formatting to reveal its structure.

- Open each substantial topic with a concrete question, visual puzzle, or practical problem. Explain why solving it matters and return to it after developing the method.
- Use short, focused paragraphs and descriptive subheadings. Use bullets for parallel facts or comparisons and numbered lists for ordered reasoning and procedures. Avoid long unbroken walls of text and excessive nested lists.
- Use bold selectively for first definitions, important conditions, and key conclusions. Keep equations as properly typeset mathematics and distinguish definitions, worked examples, practice questions, and common mistakes with consistent styles.
- Alternate explanation with purposeful figures, small worked calculations, and brief “check your understanding” questions at natural conceptual breaks. Give answers with reasoning, collapsible online and available in print.
- Signal what the reader should know already, what the current section establishes, and how it connects to the next idea. Introduce one new difficulty at a time before combining concepts.
- Use a restrained visual hierarchy and sufficient whitespace. Avoid decorative callouts, excessive bolding, or so many boxes that key results become hard to find.
- Review the pilot in both web and PDF formats for reading order, pacing, notation load, figure proximity, scanability, and visual clutter. Refine it before extending the style to the remaining chapters. Judge clarity from the explanation and examples as well as from appearance.

## Formula boxes and companion application procedures

Present every distinct substantive formula or governing equation in a consistent **Formula and application** format at its main teaching location. Include important definitions, constraints, objectives, and update rules, not just final numerical formulas. Keep intermediate algebra outside boxes. Cross-reference recurring formulas rather than repeating full boxes at every use.

Use two clearly associated components:

| Formula box | Companion application procedure |
| --- | --- |
| Descriptive name and stable equation number | The question or task it addresses |
| Clearly typeset equation | Required inputs and prerequisites |
| Symbol meanings, dimensions, units, and coordinate conventions | Numbered application steps, including conversions or normalization |
| Assumptions, validity conditions, and degeneracies | Expected output and how to interpret it |
| Exact/approximate status and limitations | Sanity checks and common mistakes |
| References to derivation, source lecture, and related concepts | Reference to a fully worked example |

- Make the companion an algorithm-like recipe for computational formulas: identify inputs, explain each operation, and state the output. Use pseudocode only where it adds clarity.
- For theoretical identities and geometric constraints, give an interpretation/checking procedure instead of inventing a computational algorithm: explain what the statement means, how to test or apply it, and what it does or does not establish.
- Pair each major formula with a small worked numerical or geometric example. Reuse an integrated quiz example where appropriate, with a precise reference.
- Use the same content and labels in both editions, with web callouts and print-safe LaTeX boxes. Allow long boxes to break across pages, keep text legible in grayscale, and avoid clipping or shrinking dense mathematics.
- The consolidated formula reference must link to these canonical boxes and their companion procedures. Track coverage in the formula ledger so no substantive lecture formula is silently left without treatment.

## Keywords, glossary, and source references

- Highlight important technical keywords in **bold at their first substantive introduction**, with a clear definition immediately beside them. Avoid highlighting entire paragraphs or repeatedly bolding every occurrence.
- Give each key concept a stable reference label. Connect its definition to the relevant numbered equations, figures, worked examples, and sections, and cite the source lecture PDF with verified slide/page numbers.
- Add a linked glossary online and an alphabetical keyword index with page references in the PDF. Each glossary entry should give a concise definition, useful synonyms/acronyms, and references to its main explanation and related concepts.
- Keep the glossary and print index synchronized with the same concept labels. Use actual LaTeX index entries and document the index-generation step; verify that final page references resolve.
- Keep internal learning references distinct from source attribution. For quiz examples, include the original filename and question number as well as any printed year/title discrepancy. Do not invent page references or bibliographic details.
- For example, the **epipolar constraint** entry should connect its definition to the equation `x′ᵀFx = 0`, its geometric figure, a worked quiz example, the relevant textbook section, and the source lecture slide/page.

## Quiz integration and verification

- Inventory all 18 relevant quiz PDFs listed in `ExamToDo.md`. Map every question/subquestion to a section and record its disposition: worked example, guided exercise, independent practice, duplicate retest, or explicitly scoped extension.
- Integrate as many distinct relevant questions as possible without interrupting the exposition. Provide a practice index linking every listed source to its treatment.
- Preserve exact and near-duplicate quiz entries as intentional closed-notes retests, as requested by `ExamToDo.md`; share explanations when appropriate rather than padding the exposition.
- Identify sources precisely, for example, “Adapted from Fall 2025, Quiz 3, Question 1.” Label newly authored problems and numerical variants separately.
- Independently verify solutions. Explain corrections and assumptions in a concise errata record; never copy an incorrect answer merely because it appears in a supplied solution.
- Correct the epipolar constraint/line-coefficient confusion in Fall 2025 Quiz 2. Check the numerical matrix’s rank before treating it as a physically valid fundamental matrix, and distinguish a formal algebra exercise from valid camera geometry if necessary.
- Treat metric upgrades from a planar grid carefully: state what is identifiable on the plane and what additional calibration/view assumptions are needed for a full-scene upgrade.
- For disparity errors, give exact results before first-order approximations and explain sign, asymmetry, and units.
- State assumptions such as independent RANSAC trials, nondegenerate samples, calibrated/rectified cameras, nonzero disparity, and nonzero patch variance.
- Fall 2025 Quizzes 7 and 8 (ICP and mesh topology) are excluded from core coverage. For the partially relevant Fall 2017 Quiz 9, include the relevant geometry and explicitly label beyond-scope parts.
- End with an exam-readiness route reflecting the derivations, retests, and unit/assumption checks in `ExamToDo.md`.

## Visual requirements

Use abundant **purposeful** illustrations. Every figure must answer a specific geometric or computational question and be explained in the surrounding text.

- Create precise original vector diagrams for coordinate frames, homogeneous geometry, camera projection, homographies, epipolar geometry, stereo, and reconstruction ambiguity.
- Include real-image demonstrations of corners, matching, warping, rectification, and reconstruction where suitable source imagery is available. Record provenance and permission/license information; do not invent attribution.
- Use computed plots for depth sensitivity, RANSAC success, eigenvalue behavior, and optimization where useful.
- Add selected interactive demonstrations only when they materially improve understanding. Each must have a complete static figure, explanation, and representative result in the PDF.
- Give figures a consistent palette, typography, labels, dimensions, captions, and source credits. Ensure legibility at printed page size and in grayscale.
- Prefer vector assets for mathematical diagrams, with web and LaTeX-compatible versions generated from the same source. Use adequate-resolution raster assets for photographs.
- Reuse lecture figures selectively with original credits preserved. Avoid blurry screenshots containing large blocks of slide text.

## LaTeX and PDF requirements

The printable edition is a first-class deliverable, not a browser printout or a collection of chapter PDFs.

- Provide a canonical full manuscript at `print/CS532_Textbook.tex`, with a preamble and a continuous document body covering the complete book in reading order. The delivered file should compile directly without requiring the user to assemble chapter fragments.
- If authoring is modular or the file is generated, maintain a reproducible exporter that emits this single complete `.tex` file. Keep local figures in a clearly organized relative asset directory.
- Keep website and print content synchronized through a documented source-of-truth and build/export process. Do not rely on separately editing two copies of every chapter.
- Choose and document a practical LaTeX engine and required packages. Provide one straightforward compile command, preferably through `latexmk`, plus a script or Makefile target that generates the manuscript and compiles the final PDF.
- Include all essential prose, equations, worked examples, exercises, solutions, tables, figures, references, and appendices. Expand web-only collapsible content appropriately for print.
- Use conventional textbook typography: title page, contents, numbered chapters/sections/equations/figures, page numbers, hyperlinks, and readable margins. Keep printed study pages usable without color.
- Resolve citations and cross-references. Include a usable bibliography in the export; document any bibliography tool needed. Avoid machine-specific paths, remote image dependencies, required network access during compilation, and unresolved template syntax.
- Preserve selectable text and mathematical typesetting. The PDF must remain understandable without interactive widgets, JavaScript, or internet access.
- Supply the compiled PDF and a portable bundle containing the `.tex`, local assets, bibliography/support files, and concise build instructions. If dependencies are unavailable, report the exact unverified step rather than claiming compilation succeeded.

## Implementation sequence

1. **Audit and coverage map:** inventory lecture topics, figures, quiz subquestions, duplicates, errata, and exam gaps. Record slide/page provenance and proposed chapter destinations.
2. **Editorial and technical foundation:** establish notation, page/figure styling, source-of-truth, web navigation, and the LaTeX export/build path.
3. **Lecture 1 first:** complete its chapter with selected slide examples, polished visuals, derivations, assigned quiz examples, and exercises. Produce both web and LaTeX/PDF versions to validate the entire workflow early.
4. **Review checkpoint:** present Lecture 1 and its coverage map for feedback before advancing. Continue independent technical checks while awaiting feedback.
5. **Complete Lectures 2–6 in order:** finish and review each lecture in both editions before moving to the next. Follow `todo.md` and `quizByLec.md`, cover higher-priority exam material in depth, and include every required gap topic. This lecture-by-lecture workflow supersedes the former Lecture 3 pilot plan.
6. **Validate and package:** build the website and complete PDF, inspect both visually, verify the content map, and provide the portable print bundle and build instructions.

Keep changes focused on the book and supporting authoring/build assets. Preserve original source PDFs and unrelated files. Prepare local changes and previews first; publish only when authorized by the user.

## Acceptance criteria

- Every substantive topic in the six lectures has a documented destination or an explicit reason for omission; overlapping slides are consolidated.
- `ExamToDo.md` priorities and all seven gap topics are addressed, with source labels and independently checked solutions.
- All 18 relevant quiz PDFs have traceable entries, including duplicate retests and scoped extensions.
- Chapters read as connected textbook explanations and contain useful, readable illustrations rather than slide dumps.
- Important formulas have explicit meanings, symbol definitions, dimensions/units, assumptions, applicability, limitations, derivations, and worked-example references. Chapter checklists and the coverage ledger account for relevant lecture topics and formulas.
- Every distinct substantive formula has a named, numbered formula box and an associated application or interpretation procedure at its main teaching location, with equivalent content in the web and print editions.
- Explanations use a strong high-school reading level while preserving prerequisite-based mathematical rigor. The pilot demonstrates intermediate reasoning, prerequisite refreshers, purposeful engagement questions, and readable formatting in both editions.
- Key terms are defined and highlighted on introduction; the linked glossary, source references, and alphabetical PDF index have working destinations and resolved page references.
- Website navigation, equations, assets, links, citations, and cross-references work.
- The complete book exports to one compilable `.tex` manuscript and one continuous PDF, with all essential content and static equivalents of interactive material.
- The print bundle builds using documented commands and relative local assets; successful checks and remaining limitations are reported accurately.
