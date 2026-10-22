"""Shared web/LaTeX presentation for the textbook's teaching boxes."""
from docutils import nodes
from html import escape
import re
from sphinx.errors import SphinxError
from sphinx.util.docutils import SphinxDirective


class TeachingBox(nodes.Admonition, nodes.Element):
    pass


class BoxTitle(nodes.title):
    pass


DEMO_TITLES = {
    "stereo": "Explore stereo depth in 3D",
    "ransac": "Explore RANSAC sampling probability",
    "projection": "Explore camera motion and projection",
    "homography": "Explore a perspective warp",
}


class InteractiveDemo(nodes.General, nodes.Element):
    pass


class InteractiveDemoDirective(SphinxDirective):
    required_arguments = 1
    has_content = True

    def run(self):
        kind = self.arguments[0]
        if kind not in DEMO_TITLES:
            raise self.error(f"Unknown interactive demo: {kind}")
        if not self.content:
            raise self.error("An interactive demo needs a complete printable explanation.")
        node = InteractiveDemo(kind=kind, title=DEMO_TITLES[kind])
        self.set_source_info(node)
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def visit_interactive_html(self, node):
    self.body.append(self.starttag(
        node, "section", CLASS="interactive-demo",
        **{"data-demo": node["kind"], "aria-label": node["title"]}
    ))
    self.body.append(
        f'<h3 class="interactive-title">{escape(node["title"])}</h3>'
        '<div class="interactive-stage"></div><div class="interactive-fallback">'
    )


def depart_interactive_html(self, node):
    self.body.append('</div></section>')


def visit_interactive_latex(self, node):
    self.body.append("\n\\subsubsection*{"
                     + node["title"] + " — print edition}\n")


def depart_interactive_latex(self, node):
    self.body.append("\n\\par\\medskip\n")


def check_demo_count(app, env):
    """Prevent extra widgets accumulating across a lecture's topic pages."""
    counts = {}
    for docname in sorted(env.found_docs):
        match = re.match(r"lectures/lecture(\d+)/", docname)
        if match:
            count = sum(1 for _ in env.get_doctree(docname).findall(InteractiveDemo))
            lecture = match.group(1)
            counts[lecture] = counts.get(lecture, 0) + count
    for lecture, count in counts.items():
        if count > 1:
            raise SphinxError(f"Lecture {lecture} has {count} interactive demos; allow only one.")


class TeachingBoxDirective(SphinxDirective):
    has_content = True
    required_arguments = 1
    final_argument_whitespace = True

    def run(self):
        node = TeachingBox()
        self.set_source_info(node)
        node["classes"] = ["admonition", self.name]
        node += BoxTitle(text=self.arguments[0])
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


def visit_html(self, node):
    self.visit_admonition(node)


def depart_html(self, node):
    self.depart_admonition(node)


def visit_latex(self, node):
    self.body.append("\n\\begin{TextbookBox}\n")


def depart_latex(self, node):
    self.body.append("\n\\end{TextbookBox}\n")


def visit_box_title(self, node):
    self.body.append("\\textbf{")


def depart_box_title(self, node):
    self.body.append("}\\par\\smallskip\n")


def unique_scripts(scripts):
    """Deduplicate scripts, including equivalent inline declarations."""
    unique = []
    seen = set()
    for script in scripts:
        filename = getattr(script, "filename", script)
        attributes = getattr(script, "attributes", {})
        key = (("inline", attributes.get("body", "")) if not filename else
               (str(filename), repr(sorted(attributes.items()))))
        if key not in seen:
            unique.append(script)
            seen.add(key)
    return unique


def deduplicate_scripts(app, pagename, templatename, context, doctree):
    # Preserve the list shared with the builder: later callbacks add per-page JS.
    context["script_files"][:] = unique_scripts(context.get("script_files", []))


def clean_builder_scripts(app):
    if app.builder.format == "html":
        scripts = app.builder._js_files
        scripts[:] = unique_scripts(scripts)


def setup(app):
    # Match TeachBooks' discovered static-file registration so the existing
    # script deduplicator can consolidate both registrations.
    app.add_js_file("textbook-interactives.js")
    app.add_directive("interactive-demo", InteractiveDemoDirective)
    app.add_node(InteractiveDemo,
                 html=(visit_interactive_html, depart_interactive_html),
                 latex=(visit_interactive_latex, depart_interactive_latex))
    app.connect("env-updated", check_demo_count)
    app.connect("builder-inited", clean_builder_scripts, priority=999)
    app.connect("html-page-context", deduplicate_scripts, priority=-1000)
    app.add_node(BoxTitle,
                 html=(lambda self, node: self.visit_title(node),
                       lambda self, node: self.depart_title(node)),
                 latex=(visit_box_title, depart_box_title))
    app.add_node(TeachingBox, html=(visit_html, depart_html),
                 latex=(visit_latex, depart_latex))
    for name in ("formula-box", "application", "worked-example", "understanding-check"):
        app.add_directive(name, TeachingBoxDirective)
    return {"version": "1.6", "env_version": 7,
            "parallel_read_safe": True, "parallel_write_safe": True}
