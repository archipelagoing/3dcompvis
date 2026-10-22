# CS 532 textbook — lecture-by-lecture TODO

## How to use this checklist

Complete **Lecture 1 → Lecture 2 → Lecture 3 → Lecture 4 → Lecture 5 → Lecture 6**. Finish each lecture's prose, figures, worked examples, exercises, and web/print checks before starting the next. Lecture 1 establishes the presentation style and export workflow; do not begin with the former Lecture 3 pilot.

Follow [TEXTBOOK_PROMPT.md](TEXTBOOK_PROMPT.md) for editorial and technical requirements. Use [quizByLec.md](3dcvMid/lectures/quizByLec.md) for primary quiz placement and secondary overlaps, and [ExamToDo.md](ExamToDo.md) for emphasis, errata, and exam gaps. Relevance scores are not exam probabilities. Check the actual PDFs before finalizing topic boundaries or source references.

**Current next action:** review the cross-lecture quiz-workbook revision. The user requested all assigned quiz problems in full, with red numbered steps and blue intermediate mathematics. Main Lecture 5–6 explanations remain unfinished; their quiz workbooks are now supplied.

## 0. Prepare the shared foundation

- [x] Inspect the current book and establish six lecture-aligned navigation groups. Verify the first two lecture boundaries from their PDFs; the earlier concept-based outline is provisional.
- [x] Set a consistent notation guide, prerequisite refresher, heading hierarchy, example numbering, keyword styling, and “Formula and application” box format.
- [x] Create `book/images/lecture01/` through `lecture06/` as needed; organize corresponding LaTeX-compatible assets under `print/images/`. Preserve editable figure sources and credits.
- [x] Choose a shared content source and reproducible export process for the website and complete `print/CS532_Textbook.tex`. Establish one-command PDF compilation and a portable Overleaf-compatible bundle.
- [x] Create a coverage ledger with lecture filename, printed slide/PDF page, topic/formula, textbook destination, selected slide example/figure, quiz question, and completion status.
- [x] Create a quiz index, figure-credit register, glossary/index labels, and errata record. Preserve source PDFs.

Step 0 completed locally. See [BUILDING.md](BUILDING.md) for commands and [the foundation status](authoring/STEP0_STATUS.md) for verification and remaining work.

## Repeat for every lecture

These are completion requirements for each lecture below, not a separate pass after all six drafts.

- [ ] Include exactly one interactive demonstration at the most relevant teaching point, following `authoring/INTERACTIVES.md`. Supply its full static PDF/no-JavaScript explanation and results; verify calculations, controls, reset, and mobile behavior.
- [ ] For spatial concepts, use a rotatable 3D scene where it clarifies the geometry, with linked numerical substitutions and image/reconstruction results. Distinguish inspecting the scene from changing the modeled camera.
- [ ] Compare against earlier chapters before writing: teach each concept once, link to existing formulas/derivations, and add only new material or distinct worked applications. Check the TLDR and quiz for repeated earlier-chapter content too.

- [ ] Read the entire lecture, including image-heavy slides. Record every substantive topic and formula; account for repeated or administrative slides explicitly.
- [ ] Select the most interesting or relevant **actual slide examples**: favor examples that reveal the geometry, explain a difficult formula, illustrate failure, or connect to the assigned quizzes. Record verified slide/page references and why each was chosen.
- [ ] Develop selected examples into textbook explanations with labeled figures, intermediate steps, and an interpreted result. Preserve attribution; distinguish lecture examples, adaptations, and newly authored examples.
- [ ] Write approachable prose at a strong high-school reading level for a prerequisite-trained student. Use intuition → definitions → diagram → mathematics → derivation → application, with prerequisite refreshers where needed.
- [ ] Give each substantive formula a named, numbered box and companion application/interpretation procedure, including symbols, units/dimensions, assumptions, limitations, sanity checks, and a worked-example reference.
- [ ] Place assigned quiz questions immediately beside the concepts they test. Independently solve and check each subquestion. Use duplicate PDFs as closed-notes retests rather than repeated exposition.
- [ ] Add original worked problems for uncovered topics; label them as new. Include short understanding checks and exercises with explained solutions in both editions.
- [ ] End with a final section called **TLDR**, summarizing that lecture's additions and providing a short quiz with explained answers. Answers must be accessible online and fully visible in print.
- [ ] Add bold first-use keywords, glossary entries, source references, and links to relevant equations, figures, and examples. Update the formula reference, quiz index, and chapter checklist.
- [ ] Build the website and cumulative LaTeX/PDF. Inspect mathematics, figures, captions, formula boxes, grayscale readability, page breaks, links, and cross-references. Ensure all web solutions and interactive explanations have print equivalents.
- [ ] Record remaining issues and present the finished lecture's web/print artifacts for review. Incorporate feedback before advancing; update this checklist only when work is actually complete.

## 1. Lecture 1 — Foundations and 3D geometry

Source: `3dcvMid/lectures/wk1_2_cs532s26_IntroToGeometry.pdf`.

- [x] Audit actual lecture coverage and distinguish its material from Lecture 2. Select a compelling application/image sequence from the slides to introduce the course's geometric questions.
- [x] Explain the lecture's foundational geometry and coordinate reasoning, with simple diagrams before dense notation. Introduce later concepts only to the depth justified by the lecture.
- [x] Integrate **Fall 2025 Quiz 1**, `quizzesf25sol/cs532f25_quiz_1_solution.pdf`: shared-object relative camera pose and the plane through camera/object positions. State transform directions and degenerate cases. Place its probability questions beside RANSAC in Lecture 3, with a cross-reference from this quiz's index entry.
- [x] Integrate the relevant geometry from **Fall 2017 Quiz 9**, `olderquizzes/cs532_f17_quiz9.pdf`: rotated vectors/normals where supported by the slides. Label depth-map fusion or other beyond-scope content as an extension, and defer prerequisite-dependent backprojection to Lecture 3/4 with cross-references.
- [x] Choose the strongest slide illustrations to redraw or reuse with credits; add a fully worked coordinate/geometry example if the quizzes do not adequately teach the foundations.
- [x] Add the camera-motion interactive after Example 1.15, with a static print/no-JavaScript equivalent. Upgraded to a rotatable 3D scene with point dragging, camera translation/yaw, focal-length controls, linked image, and world→camera→pixel calculations.
- [x] Complete the authoring and technical checks, including the compiled PDF and internal layout review.
- [x] Review Lecture 1 with the user and incorporate style/content feedback before starting Lecture 2. User approved progression after the TLDR addition.

## 2. Lecture 2 — Projective geometry and linear algebra

Source: `3dcvMid/lectures/cs532_f25_Week2.pdf`.

- [x] Verify the lecture's coverage of homogeneous geometry, linear algebra, transformations, rotation representations, and quaternions. Remove repeated teaching, summaries, and quiz content; link to Lecture 1 prerequisites.
- [x] Select the clearest slide examples of projective intersections and transformations; use precise diagrams and small computations to explain the geometry.
- [x] Retain the Lecture 2 source assignment for **Spring 2020 Quiz 1**, but place its worked solutions with Lecture 1 foundations to satisfy the user's unique-content requirement. Source: `olderquizzes/cs532s20_quiz1.pdf`: collinearity via dot/cross products, finite/ideal intersections, and projection-matrix dimensions. Identify degenerate configurations explicitly.
- [x] Add new worked examples for slide topics absent from the quiz, especially rotation representations, quaternions, and transformation hierarchies where covered. State composition order and conventions.
- [x] Cross-reference Lecture 1's relative-pose example and preview the camera formulation developed in Lecture 3.
- [x] Add the perspective-warp/cross-ratio interactive, with a paired static figure and print/no-JavaScript explanation.
- [x] Complete every item in the repeated lecture checklist.

- [x] Review Lecture 2 with the user and incorporate feedback before Lecture 3. User authorized progression to Lecture 3.

## 3. Lecture 3 — Camera projection, homographies, and RANSAC

Source: `3dcvMid/lectures/wk3_cs532s26_ImageFormation+Homographies-1.pdf`.

- [x] Audit Lecture 3 against completed Lectures 1–2 and record the additions. Link to existing projection, homography, warping, DLT/normalization, and RANSAC explanations instead of repeating them.
- [x] Select engaging actual slide examples of projection and planar image mappings. Reuse Lecture 2's court-warp example by reference; add a distinct real-image application only if it teaches something new.
- [x] Integrate **Spring 2019 Quiz 2**, `olderquizzes/cs532s19_quiz2-2.pdf`: 640×480 image, 90° horizontal FOV, focal length, calibration matrix, projection dimensions, homogeneous scaling, and principal-point conventions.
- [x] Use **Spring 2020 Quiz 3**, `olderquizzes/cs532s20_quiz3.pdf`, as the near-duplicate camera-calibration retest; retain its mixed printed header in provenance notes.
- [x] Integrate **Spring 2020 Quiz 2**, `olderquizzes/cs532s20_quiz2.pdf`: pinhole projection and collinear viewing-ray vectors.
- [x] Integrate **filename “2015” Quiz 9**, `olderquizzes/cs532f15_quiz9.pdf` (printed Spring 2019): derive ray–plane depth, with parallel-ray and invalid-depth cases.
- [x] Integrate **Spring 2019 Quiz 3**, `olderquizzes/cs532s19-quiz3.pdf`: pentagon putative matches, inlier fraction, RANSAC iteration count, and regular-polygon ambiguity. Explain sampling assumptions.
- [x] Integrate Fall 2025 Quiz 1's probability questions here as new worked applications of the complement-probability reasoning already introduced in Lecture 2; cross-link its Lecture 1 geometry examples.
- [x] Check the DLT/SVD exam gap against Lecture 2's completed derivation and numerical example. Add only remaining gaps or distinct numerical practice; link back for the `2n × 9` system, nullspace/reshape, normalization/denormalization, and inverse warping. Update the coverage register rather than duplicating the treatment.
- [x] Add the lecture's single **RANSAC sampling explorer** beside the probability application: vary inlier ratio and trial count, compare observed all-inlier samples with predicted success probability, and show the numerical substitutions. Include static results in print.
- [x] Finish with a final **TLDR** and short quiz with explained answers, focused on Lecture 3's additions.
- [x] Complete every item in the repeated lecture checklist; give this high-priority mathematics sufficient depth.

- [x] Review Lecture 3 with the user and incorporate feedback before Lecture 4. User approved and requested Lecture 4.

## 4. Lecture 4 — Two-view geometry and stereo

Source: `3dcvMid/lectures/wk4_cs532s26_TwoViewGeometry.pdf`.

- [x] Select slide examples that make distortion, epipolar geometry, and stereo constraints visually concrete. Include labeled two-camera geometry and image-space epipolar lines.
- [x] Integrate `olderquizzes/cs532f15_quiz4.pdf` and `olderquizzes/cs532s19_quiz4.pdf`: fundamental matrix to line and expansion of the epipolar constraint. Preserve both source entries; use the duplicate for retesting.
- [x] Integrate **Fall 2025 Quiz 2**, `quizzesf25sol/cs532f25_quiz_2_solution.pdf`: intersect epipolar lines in a third view and find points satisfying a constraint. Correct the line/point confusion, check matrix rank, and explain degenerate intersections.
- [x] Integrate **Fall 2025 Quiz 3**, `quizzesf25sol/cs532f25_quiz_3_solution.pdf`: depth, first-order versus exact error, and disparity-search bounds with consistent units.
- [x] Integrate **Spring 2019 Quiz 5**, `olderquizzes/cs532s19_quiz5-2.pdf`: exact ±1-pixel disparity errors and their asymmetry. Use `olderquizzes/cs532s20_quiz5.pdf` as the duplicate retest.
- [x] Fill quiz gaps with worked examples of fundamental-matrix estimation/normalized eight-point estimation, essential-matrix constraints and four candidate poses, and cheirality, to the depth supported by the lecture. Label extra context explicitly.
- [x] Explain triangulation and stereo costs where introduced; connect to Lecture 6's full triangulation derivation. Include a depth-sensitivity plot and static equivalents of any interactive demonstration.
- [x] Complete every item in the repeated lecture checklist; verify all high-priority formulas and errata.

- [x] Incorporate L4 feedback: prominent epipolar example navigation; ray/plane/line intuition; guided matrix, transpose, nullspace and residual calculations; fully expanded quiz arithmetic; stereo sensitivity, signed exact errors, derivative and bounded-error examples. Rebuild web and printable LaTeX/PDF.
- [ ] Review the revised Lecture 4 with the user before Lecture 5.

## 5. Lecture 5 — Corners, tracking, descriptors, and matching

Source: `3dcvMid/lectures/wk5_cs532_Corners.pdf`.

- [ ] Select actual slide examples of feature detection/matching, including panorama or rover imagery if useful after inspection. Preserve image credits and show what the reader should notice.
- [x] Integrate **Spring 2019 Quiz 6**, `olderquizzes/cs532s19_quiz6-2.pdf`: intersections, corners versus edges, slanted-edge ambiguity, and isolated pixels. Explain the structure tensor rather than relying only on intuition.
- [x] Integrate **Fall 2025 Quiz 4**, `quizzesf25sol/cs532f25_quiz_4_solution.pdf`: exposure changes, brightness constancy, patch normalization, assumptions, and zero/low-variance limitations.
- [x] Supply the booklet’s fully worked numerical Harris and Lucas–Kanade problems in the Lecture 5 quiz workbook.
- [ ] Develop the main chapter’s complete Harris example: gradients, weighted sums, tensor, eigenvalues, determinant/trace response, thresholding, and non-maximum suppression.
- [ ] Add a complete Lucas–Kanade example: Taylor approximation, displacement sign convention, `A`, `b`, normal equations, solvability, and interpreted motion. Illustrate the aperture problem.
- [ ] Cover the slide-supported descriptors, invariance properties, matching metrics, and ambiguity with an illustrated matching example.
- [ ] Complete every item in the repeated lecture checklist.

## 6. Lecture 6 — Structure from motion

Source: `3dcvMid/lectures/wk6_cs532s24_SFM1.pdf`.

- [ ] Select the lecture's most informative reconstruction and feature-track examples. Use them to connect measurements, camera motion, and recovered structure.
- [x] Integrate **Fall 2025 Quiz 5**, `quizzesf25sol/cs532f25_quiz_5_solution-1.pdf`: facade/floor constraints, reconstruction upgrades, and weak-overlap sequential versus factorization choices. Correct unsupported full-scene metric-upgrade claims and distinguish unknown visibility from zero-valued measurements.
- [x] Integrate **Fall 2025 Quiz 6**, `quizzesf25sol/cs532f25_quiz_6_solution.pdf`: large-scale pipeline choice and contaminated-match verification. Label advanced transfer material and check claims about computational complexity and failure modes.
- [x] Supply the booklet’s complete factorization, linear triangulation and one-variable Gauss–Newton problems in the Lecture 6 workbook.
- [ ] Develop the main chapter’s centered measurement-matrix/SVD factorization example, showing rank-three structure and affine/metric ambiguity.
- [ ] Add a full linear-triangulation example: construct `AX = 0`, solve by SVD, dehomogenize, check cheirality and reprojection error, and explain degeneracy/noise.
- [ ] Add a bundle-adjustment example with residuals, objective, gauge fixing, Jacobian structure, and a manageable Gauss–Newton/LM update. Explain the geometric effect rather than presenting unexplained matrix algebra.
- [ ] Include a reconstruction-pipeline figure and distinguish calibrated, projective, affine, and metric/similarity recovery with explicit assumptions.
- [ ] Complete every item in the repeated lecture checklist.

## 7. Final book-wide completion

- [ ] Reconcile the coverage ledger with all six PDFs: every substantive topic/formula is taught or has an explicit disposition.
- [x] Reconcile the quiz index with the supplied booklet’s 18 in-scope historical sources and every grouped subquestion, including complete duplicate retests and primary/secondary placements. Keep Fall 2025 Quizzes 7 and 8 outside core scope.
- [ ] Verify all seven exam-gap topics and the exam-readiness route in `ExamToDo.md`; retain lecture order for the main reading route.
- [ ] Consolidate notation, formula boxes, glossary, keyword index, bibliography, credits, and errata; remove accidental repetition and fix forward references.
- [ ] Build and visually inspect the complete website and continuous PDF. Resolve references, print solutions, static interaction equivalents, image paths, and layout problems.
- [ ] Compile the portable bundle from documented commands with local relative assets. Supply the complete `.tex`, PDF, images, bibliography/support files, and Overleaf/local build instructions.
- [ ] Report actual checks and remaining limitations; publish the completed updates only when authorized.

## Cross-lecture quiz-format correction

- [x] Audit the supplied lecture-organized booklet: 18 historical quizzes, 39 problem groups with all subparts, plus seven original supplemental problems.
- [x] Preserve full problem wording/givens, source identity, header discrepancies and separate duplicate retests.
- [x] Supply six clearly named quiz workbooks; route existing concept/example links to the complete treatments.
- [x] Expand matrix/vector products, substitutions and intermediate arithmetic; give every step a short reason, a red numbered heading and blue math in web and LaTeX. Also expand all 32 original end-of-chapter quiz answers in Lectures 1–4 using this format.
- [x] Keep a question-level coverage register and update the authoring prompts/template to require this format.
- [x] Complete independent math, original-question fidelity, web/mobile/color/navigation and continuous PDF/portable-bundle checks. See `authoring/QUIZ_WORKBOOK_STATUS.md`: 78 complete statements, 290 styled steps, 214-page current PDF, all bundled figures verified.
- [ ] Review the new quiz format with the user; keep full Lecture 5–6 completion separate.
