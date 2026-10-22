# Authoring conventions

Follow [the simplification prompt](../TEXTBOOK_SIMPLIFICATION_PROMPT.md) for reading level, brevity, and presentation. Use only the teaching elements a topic needs; preserve required mathematics and quiz coverage.

`book/` MyST Markdown is the single content source for HTML and LaTeX. Edit those pages, not generated files under `print/`. Follow `TEXTBOOK_PROMPT.md` and `todo.md`; use `quizByLec.md` for primary quiz placement, with explicit secondary cross-references.

## Structure and labels

- One navigation chapter per lecture, with topic pages added as `sections` in `book/_toc.yml` when written. Preserve lecture order.
- Use `(lec01-topic)=` for section labels, `eq-lec01-topic` for equations, `fig-lec01-topic` for figures, and `ex-lec01-topic` for examples. Reference with MyST `{ref}`, `{eq}`, `{numref}`, and `{term}` roles. Do not hard-code generated equation/page numbers.
- Number worked examples and exercises as lecture number plus within-lecture ordinal (for example, Worked example 1.1). Keep their stable labels separate from their displayed numbers; update the quiz index when ordering changes. Number mathematical equations through labeled math directives, not by typing numbers into the equation.
- For standalone example labels, use explicit link text in the MyST ref role: a title followed by the target label in angle brackets. Unlike a section, an example has no automatically discoverable heading.
- Keep first-use keywords bold and define them immediately. Add `{index}` entries at their teaching location and a `{glossary}` definition with references. Sphinx generates the alphabetical PDF index and page references.
- Use short paragraphs, descriptive subheadings, bullets for parallel facts, and numbers for ordered work. Explain assumptions, units, and intermediate algebra.

## Teaching boxes

Use the registered `formula-box`, `application`, `worked-example`, and `understanding-check` directives, shown in `templates/section.md`. Each formula box contains a labeled math directive. Its companion application explains inputs, steps, output, interpretation, and a sanity check. Constraints get an interpretation/checking procedure rather than an invented algorithm.

The same directives become accessible HTML admonitions and breakable, grayscale-safe LaTeX boxes. Use a normal `admonition` with `:class: dropdown` for online solutions: its content is printed openly in LaTeX. Never put essential content only in raw HTML or JavaScript.

## Figures

Keep web assets in `book/images/lectureNN/` and editable sources in a `sources/` subfolder. Prefer SVG for web diagrams, PDF for vector print diagrams, and high-resolution PNG/JPEG for photos. Supply paired formats with matching basenames, reference `name.*` in a MyST figure directive, and verify the builder's chosen format in both outputs.

The print exporter copies selected assets into `print/images/` and rewrites their generated LaTeX paths. Its bundle includes all required local assets. Record provenance, original/adapted status, caption, source slide/page, author, license/permission status, and web/print paths in `figure-credits.csv`.

## Registers and completeness

- `coverage.csv`: initial page-level inventory, expanded into topic/formula rows during each lecture audit. Extracted headings are navigation aids, not verified interpretations. PDF page numbers do not imply printed slide numbers.
- `quiz-index.csv`: all 20 source files, including 18 in-scope entries and two excluded quizzes. Add subquestion rows during the relevant lecture audit; verify answers independently. Duplicate retests retain their own source IDs.
- `figure-credits.csv`: starts empty until figures are selected.
- `errata.csv`: suspected source issues and verification state.
- `lecture-boundaries.md`: inspected overlap decisions and provisional teaching ownership.

Update public reference pages and registers together. Source provenance belongs beside adapted material, including filename, verified printed slide/PDF page, and quiz question. Keep supplementary material labeled.
