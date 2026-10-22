#!/usr/bin/env python3
"""Generate print/no-JavaScript views of the textbook's interactive explorers."""
from pathlib import Path
import build_lecture01_figures as tikz

OUT = Path(__file__).resolve().parents[1] / "book/images/lecture02"


def main():
    tikz.OUT = Path(__file__).resolve().parents[1] / "book/images/lecture01"
    print("Built", tikz.compile_one(("projection-explorer", r'''
\begin{scope}[x={(1.25cm,.15cm)},y={(.15cm,-1.2cm)},z={(.65cm,.35cm)}]
\coordinate (C) at (0,0,0);\coordinate (P) at (1,.5,10);\coordinate (Q) at (.2,.1,2);
\fill[blue!12,opacity=.65] (-1,-1,2)--(1,-1,2)--(1,1,2)--(-1,1,2)--cycle;
\draw[blue!70!black,thick] (-1,-1,2)--(1,-1,2)--(1,1,2)--(-1,1,2)--cycle;
\draw[blue!30] (C)--(-1,-1,2) (C)--(1,-1,2) (C)--(1,1,2) (C)--(-1,1,2);
\draw[dashed,blue!60!black] (C)--(0,0,11);
\draw[orange!85!black,very thick] (C)--(P);
\draw[arr,red!70!black] (C)--(1.5,0,0) node[right]{$+X_c$};
\draw[arr,green!50!black] (C)--(0,1.4,0) node[below]{$+Y_c$};
\draw[arr,blue!70!black] (C)--(0,0,3.5) node[above]{$+Z_c$};
\fill[blue!70!black] (C) circle(2.5pt) node[above left]{$C=(0,0,0)$};
\fill[orange!85!black] (P) circle(3pt) node[above right]{$P=(1,0.5,10)$};
\fill[orange!85!black] (Q) circle(2.5pt) node[above left=5pt]{$q=(0.2,0.1,2)$};
\node[align=center] at (-.6,-1.8,2){Virtual image plane\\$Z_c=f_{\rm plane}=2$};
\end{scope}
''')))
    body = []
    for index, (title, perspective) in enumerate([
        ("Source plane", 0), ("Destination: $p=0.5$", .5)
    ]):
        offset = index * 5.5
        scale = 1.5 if index == 0 else .75

        def point(x, y):
            return f"({offset+scale*x/(1+perspective*x):.6f},{scale*y/(1+perspective*x):.6f})"

        body.append(rf"\node at ({offset},2.2) {{{title}}};")
        for t in [-1, -.5, 0, .5, 1]:
            body.append(rf"\draw[gray!65] {point(-1,t)}--{point(1,t)};")
            body.append(rf"\draw[gray!65] {point(t,-1)}--{point(t,1)};")
        corners = [(-1,-1),(1,-1),(1,1),(-1,1)]
        body.append(r"\draw[thick,blue!70!black] " + "--".join(point(*p) for p in corners) + "--cycle;")
        body.append(rf"\draw[thick,orange!80!black] {point(-1,.3)}--{point(1,.3)};")
        for number, x in enumerate([-.75,-.25,.25,.75], 1):
            body.append(rf"\fill[orange!80!black] {point(x,.3)} circle(2pt) node[above=3pt]{{{number}}};")
        body.append(rf"\node at ({offset},-2) {{Cross-ratio $=4/3$}};")
    tikz.OUT = OUT
    print("Built", tikz.compile_one(("perspective-explorer", "\n".join(body))))


if __name__ == "__main__":
    main()
