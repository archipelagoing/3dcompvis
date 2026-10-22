"""Shared web/LaTeX presentation for the textbook's teaching boxes."""
from docutils import nodes
from sphinx.util.docutils import SphinxDirective


class TeachingBox(nodes.Admonition, nodes.Element):
    pass


class BoxTitle(nodes.title):
    pass


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


def setup(app):
    app.add_node(BoxTitle,
                 html=(lambda self, node: self.visit_title(node),
                       lambda self, node: self.depart_title(node)),
                 latex=(visit_box_title, depart_box_title))
    app.add_node(TeachingBox, html=(visit_html, depart_html),
                 latex=(visit_latex, depart_latex))
    for name in ("formula-box", "application", "worked-example", "understanding-check"):
        app.add_directive(name, TeachingBoxDirective)
    return {"version": "1.0", "parallel_read_safe": True, "parallel_write_safe": True}
