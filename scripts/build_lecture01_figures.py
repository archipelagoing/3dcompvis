#!/usr/bin/env python3
"""Compile original lecture diagrams to paired PDF/SVG assets (XeLaTeX + Poppler)."""
from pathlib import Path
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'book/images/lecture01'
DIAGRAMS = {
'pipeline': r'''
\node[box] (a) at (0,0) {Photographs\\different viewpoints};
\node[box] (b) at (4,0) {Associate\\same scene feature};
\node[box] (c) at (8,0) {Register\\cameras + sparse points};
\node[box] (d) at (4,-2) {Dense depth\\many image pixels};
\node[box] (e) at (8,-2) {Represent\\point cloud / surface};
\draw[arr] (a)--(b);\draw[arr] (b)--(c);\draw[arr] (c)--(d);\draw[arr] (d)--(e);
''',
'ambiguity': r'''
\coordinate (C) at (0,0);\coordinate (X) at (5,2.5);\coordinate (Y) at (8,4);
\fill[blue!5] (2,-.5) rectangle (2.15,3);
\draw[arr] (-.3,0)--(8.8,0) node[right]{$Z$};
\draw[thick,blue!70!black] (C)--(Y);
\fill (C) circle(2pt) node[below]{$C$};
\fill[blue!70!black] (2,1) circle(2.5pt) node[left]{$x$};
\fill (X) circle(2.5pt) node[above left]{$X$};
\fill (Y) circle(2.5pt) node[above left]{$\lambda X$};
\node[below,align=center] at (2,-.7){image plane};
\node[align=center] at (5.6,.5){Different depths,\\same viewing ray.};
''',
'projective-lines': r'''
\draw[arr] (0,0)--(4.3,0) node[right]{$x$};\draw[arr] (0,0)--(0,3.4) node[above]{$y$};
\draw[very thick,blue!65!black] (0,1)--(4,1) node[right]{$y=1$};
\draw[very thick,orange!80!black] (0,2)--(4,2) node[right]{$y=2$};
\node[align=center] at (2,-.8){World: parallel lines\\meet at $(1,0,0)^T$ in $\mathbb P^2$.};
\begin{scope}[shift={(7,0)}]
\coordinate (v) at (2.5,3);\draw[very thick,blue!65!black] (0,0)--(v);
\draw[very thick,orange!80!black] (5,0)--(v);
\foreach \y in {.3,.75,1.25,1.8,2.3} {\draw[gray] ({\y/3*2.5},\y)--({5-\y/3*2.5},\y);}
\fill (v) circle(2pt) node[above]{vanishing point};
\node[align=center] at (2.5,-.8){Perspective image: the projected\\lines can meet at a finite pixel.};
\end{scope}
''',
'rotation-center': r'''
\draw[arr] (-.5,0)--(5,0) node[right]{$x$};\draw[arr] (0,-.5)--(0,4) node[above]{$y$};
\coordinate (c) at (2,1);\coordinate (p) at (3,1);\coordinate (q) at (2,2);
\fill (c) circle(2pt) node[below]{$c=(2,1)$};
\draw[arr,blue!70!black] (c)--(p) node[right]{$p=(3,1)$};
\draw[arr,orange!90!black] (c)--(q) node[above]{$p'=(2,2)$};
\draw[arr] (2.6,1) arc (0:90:.6) node[midway,above right]{$90^\circ$};
\node[align=left] at (7,2){Subtract $c$;\\rotate the offset;\\add $c$ back.};
''',
'planes': r'''
\coordinate (A) at (0,0);\coordinate (B) at (4,0);\coordinate (D) at (1.5,2.5);
\fill[blue!8] (-.8,-.5)--(4.7,-.5)--(6,2.8)--(.5,2.8)--cycle;
\draw[arr,thick,blue!70!black] (A)--(B) node[midway,below]{$B-A$};
\draw[arr,thick,orange!90!black] (A)--(D) node[midway,left]{$D-A$};
\draw[arr,very thick] (A)--(-.6,2) node[above]{$n=(B-A)\times(D-A)$};
\fill (A) circle(2pt) node[below]{$A$};\fill (B) circle(2pt) node[right]{$B$};\fill (D) circle(2pt) node[right]{$D$};
\node[align=center] at (7,1){Schematic 3D view.\\The normal is perpendicular\\to both in-plane directions.};
''',
'plucker': r'''
\coordinate (O) at (0,0);\coordinate (p) at (1.6,2.3);\coordinate (q) at (4.6,2.3);
\draw[arr] (O)--(6,0) node[right]{$x$};\draw[arr] (O)--(0,3.4) node[above]{$y$};
\draw[very thick,blue!70!black] (.6,2.3)--(6,2.3) node[right]{line};
\draw[arr,thick] (O)--(p) node[midway,left]{$p$};\draw[arr,thick] (p)--(q) node[midway,above]{$d$};
\draw[arr,dashed] (O)--(q) node[midway,below]{$p+\alpha d$};
\fill (p) circle(2pt);\fill (q) circle(2pt);
\node[align=center] at (3,-1){Changing the chosen point along the line does not change\\$m=p\times d$, because $d\times d=0$.};
''',
'rotation-order': r'''
\node[box] (v) at (0,0) {Start\\$(1,0,0)^T$};
\node[box] (z) at (4,1) {$R_z(90^\circ)$\\$(0,1,0)^T$};
\node[box] (x) at (8,1) {$R_x(90^\circ)$\\$(0,0,1)^T$};
\node[box] (x2) at (4,-1.5) {$R_x(90^\circ)$\\$(1,0,0)^T$};
\node[box] (z2) at (8,-1.5) {$R_z(90^\circ)$\\$(0,1,0)^T$};
\draw[arr] (v)--(z);\draw[arr] (z)--(x);\draw[arr] (v)--(x2);\draw[arr] (x2)--(z2);
''',
'shared-object': r'''
\node[draw,circle,minimum size=1cm] (a) at (0,0) {$C_1$};
\node[draw,circle,minimum size=1cm] (b) at (7,0) {$C_2$};
\node[draw,circle,minimum size=1cm] (o) at (3.5,3) {$O$};
\draw[arr,blue!70!black] (o)--(a) node[midway,above left]{$T_{C_1\leftarrow O}$};
\draw[arr,orange!90!black] (b)--(o) node[midway,above right]{$T_{O\leftarrow C_2}$};
\draw[arr,very thick] (b)--(a) node[midway,below]{$T_{C_1\leftarrow C_2}$};
\node[align=center] at (3.5,-1){Follow the coordinate path: $C_2\to O\to C_1$.\\The rightmost transform acts first.};
''',
'pinhole': r'''
\coordinate (C) at (0,0);\coordinate (x) at (2,1);\coordinate (X) at (6,3);
\draw[arr] (-.4,0)--(7.2,0) node[right]{$Z_c$};
\draw[blue!65!black,very thick] (2,-.5)--(2,2.2) node[above]{virtual image};
\draw[arr,thick] (6,0)--(X) node[midway,right]{$Y_c$};
\draw[thick,orange!90!black] (C)--(X);
\draw[<->] (0,-.7)--(2,-.7) node[midway,below]{$f$};
\draw[<->] (0,-1.4)--(6,-1.4) node[midway,below]{$Z_c$};
\fill (C) circle(2pt) node[above left]{$C$};\fill (x) circle(2pt) node[left]{$y$};\fill (X) circle(2pt) node[above]{$(Y_c,Z_c)$};
\node[align=center] at (4,4){Side view: $y/f=Y_c/Z_c$.\\The physical sensor behind the pinhole has inverted signs.};
''',
'camera-motion': r'''
\draw[arr] (-.4,0)--(8,0) node[right]{$Z$};
\coordinate (A) at (0,0);\coordinate (B) at (2,0);\coordinate (X) at (6,2);
\fill (A) circle(2pt) node[below]{$C=(0,0,0)$};\fill (B) circle(2pt) node[below right]{$C'=(0,0,2)$};
\fill (X) circle(2pt) node[above]{$X=(X_c,Y_c,Z_c)$};
\draw[blue!70!black,thick] (A)--(X);\draw[orange!90!black,thick] (B)--(X);
\draw[arr] (0,-1)--(2,-1) node[midway,below]{camera moves forward};
\node[align=center] at (4,3.5){The point stays fixed. Its camera-relative depth\\changes from $Z_c$ to $Z_c-2$.};
''',
}

DIAGRAMS['tetrahedron'] = '\\begin{scope}[x={(1.2cm,0cm)},y={(-.65cm,-.6cm)},z={(0cm,1.25cm)}]\n\\coordinate (a) at (0,0,0);\\coordinate (b) at (0,2,0);\\coordinate (c) at (0,0,2);\\coordinate (d) at (2,0,0);\n\\fill[blue!10] (b)--(c)--(d)--cycle;\n\\draw[thick] (a)--(b)--(c)--(a)--(d)--(b);\\draw[thick] (c)--(d);\n\\fill (a) circle(1.5pt) node[left]{$v_1=(1,1,0)$};\n\\fill (b) circle(1.5pt) node[below]{$v_2=(1,2,0)$};\n\\fill (c) circle(1.5pt) node[above]{$v_3=(1,1,1)$};\n\\fill (d) circle(1.5pt) node[right]{$v_4=(2,1,0)$};\n\\end{scope}\n'
DIAGRAMS['depth-rays'] = '\\coordinate (a) at (0,0);\\coordinate (b) at (4,0);\\coordinate (p) at (2,4);\n\\draw[arr] (-.5,0)--(5.2,0) node[right]{$X_w$};\\draw[arr] (0,-.4)--(0,4.8) node[above]{$Z_w$};\n\\draw[thick,blue!70!black] (a)--(p);\\draw[thick,orange!90!black] (b)--(p);\n\\fill (a) circle(2pt) node[below]{$C_1=(0,0,0)$};\n\\fill (b) circle(2pt) node[below]{$C_2=(2,0,0)$};\n\\fill (p) circle(2pt) node[above right]{$X_w=(1,0,10)$};\n\\node[align=center] at (2,-1.2){World $x$--$z$ section; not equal axis scales.\\\\Both cameras use the same world frame.};\n'

def compile_one(item):
    name,body=item
    source=OUT/'sources'/f'{name}.tex';source.parent.mkdir(parents=True,exist_ok=True)
    source.write_text(r'''\documentclass[tikz,border=9pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta,positioning,calc}
\begin{document}
\begin{tikzpicture}[font=\small,arr/.style={-{Stealth},thick},box/.style={draw=blue!55!black,rounded corners,fill=blue!4,align=center,text width=2.9cm,minimum height=1.05cm}]
'''+body+'\n\\end{tikzpicture}\n\\end{document}\n')
    with tempfile.TemporaryDirectory(prefix='cs532-fig-') as temp:
        log=Path(temp)/'compile.log'
        with log.open('w') as stream:
            result=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={temp}',str(source)],stdout=stream,stderr=subprocess.STDOUT)
        if result.returncode:raise RuntimeError(log.read_text()[-1800:])
        (OUT/f'{name}.pdf').write_bytes((Path(temp)/f'{name}.pdf').read_bytes())
    subprocess.run(['pdftocairo','-svg',str(OUT/f'{name}.pdf'),str(OUT/f'{name}.svg')],check=True)
    return name

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=3) as pool:
        for name in pool.map(compile_one,DIAGRAMS.items()):print('Built',name,flush=True)
