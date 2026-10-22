#!/usr/bin/env python3
"""Reproducible Lecture 4 diagrams and a credited pair of extracted slide photos."""
from pathlib import Path
import math
from concurrent.futures import ThreadPoolExecutor
import build_lecture01_figures as tikz
OUT=Path(__file__).resolve().parents[1]/'book/images/lecture04'
DIAGRAMS={
 'third-view':r'''
\draw[arr] (0,0)--(6,0) node[right]{$u_C$};\draw[arr] (0,0)--(0,5) node[above]{$v_C$};
\draw[thick,blue!70!black] (2,-.1)--(2,4.5) node[above]{$u_C=1/2$};
\draw[thick,orange!85!black] (0,4)--(4,0) node[below right]{$u_C+v_C=1$};
\fill (2,2) circle(3pt) node[right]{$x_C=(1/2,1/2,1)^T$};
\node[below] at (2,0){$1/2$};\node[left] at (0,2){$1/2$};
''',
 'stereo-rays':r'''
\coordinate (L) at (0,0);\coordinate (R) at (6,0);\coordinate (P) at (2.5,7);
\fill[blue!8] (-1.1,1.3) rectangle (1.1,1.5);
\fill[blue!8] (4.9,1.3) rectangle (7.1,1.5);
\draw[blue!70!black,thick] (-1.1,1.4)--(1.1,1.4) (4.9,1.4)--(7.1,1.4);
\draw[dashed] (L)--(0,7.8) (R)--(6,7.8);
\draw[very thick,orange!85!black] (L)--(P);
\draw[very thick,blue!70!black] (R)--(P);
\fill (L) circle(2pt) node[below]{$C_L=(0,0,0)$};
\fill (R) circle(2pt) node[below]{$C_R=(b,0,0)$};
\fill[orange!85!black] (P) circle(3pt) node[above]{$(X,Y,Z)$};
\fill (0.5,1.4) circle(2pt) node[above right]{$u_L-c_x$};
\fill (5.3,1.4) circle(2pt) node[above left]{$u_R-c_x$};
\draw[<->] (0,-1)--(6,-1) node[midway,below]{baseline $b$};
\draw[<->] (-1.7,0)--(-1.7,1.4) node[midway,left]{$f$};
\draw[<->] (8,0)--(8,7) node[midway,right]{depth $Z$};
\node at (3,8.4){$d=fX/Z-f(X-b)/Z=fb/Z$};
''',
 'stereo-pair':r'''
\node at (0,0){\includegraphics[height=4cm]{book/images/lecture04/sources/plant-left.jpg}};
\node at (6,0){\includegraphics[height=4cm]{book/images/lecture04/sources/plant-right.jpg}};
\node at (0,2.5){Reference image};\node at (6,2.5){Matching image};
\node[align=center] at (3,-2.8){Find the same visible surface, not just the same color.\\Depth changes its location between views.};
''',
 'support-boundary':r'''
\fill[blue!10] (0,0) rectangle (3,3);\fill[orange!12] (3,0) rectangle (6,3);
\draw[thick] (3,0)--(3,3);
\node at (1.4,3.5){Foreground};\node at (4.6,3.5){Background};
\draw[very thick] (1.7,.5) rectangle (4.3,2.5);
\fill (2.8,1.5) circle(3pt) node[left]{$p$};
\draw[dashed,thick,blue!70!black] (.2,.5) rectangle (2.9,2.5);
\node[align=left] at (8.7,2){Solid window mixes depths.\\Shift or reweight support\\to favor the same surface.};
''',
}

def depth_curve():
 body=[r'\draw[arr] (0,0)--(10.5,0) node[right]{$d$ pixels};',r'\draw[arr] (0,0)--(0,6.7) node[above]{$Z$ cm};']
 for z in [20,50,100,150]:body.append(rf'\draw[gray!30] (0,{z/25})--(10,{z/25});\node[left] at (0,{z/25}) {{{z}}};')
 for d in [5,10,20,25,30]:body.append(rf'\node[below] at ({d/3},0) {{{d}}};')
 coords=' '.join(f'({d/3:.5f},{20/d:.5f})' for d in [3.2+i*.1 for i in range(269)])
 body.append(r'\draw[very thick,blue!70!black] plot coordinates {'+coords+'};')
 for d in [5,25]:
  zl=500/(d+1)/25;zh=500/(d-1)/25
  body.append(rf'\fill[orange!15] ({(d-1)/3},{zl}) rectangle ({(d+1)/3},{zh});')
  body.append(rf'\draw[orange!85!black,thick] ({(d-1)/3},{zl}) rectangle ({(d+1)/3},{zh});')
  body.append(rf'\fill[blue!70!black] ({d/3},{20/d}) circle(2.5pt);')
 body.append(r'\node[align=left] at (6,5.1){$b=10$ cm, $f=50$ px\\$Z=500/d$\\Boxes: $d\pm1$ pixel};')
 return '\n'.join(body)

def main():
 tikz.OUT=OUT
 diagrams={**DIAGRAMS,'depth-sensitivity':depth_curve()}
 with ThreadPoolExecutor(max_workers=3) as pool:
  for name in pool.map(tikz.compile_one,diagrams.items()):print('Built',name,flush=True)
if __name__=='__main__':main()
