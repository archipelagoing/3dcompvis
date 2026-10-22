#!/usr/bin/env python3
"""Original Lecture 3 vector diagrams, reproducible as PDF and SVG."""
from pathlib import Path
import math
import build_lecture01_figures as tikz

OUT = Path(__file__).resolve().parents[1] / 'book/images/lecture03'
DIAGRAMS = {
'fov': r'''
\coordinate (C) at (0,0);
\fill[blue!8] (3.2,-3.2) rectangle (3.4,3.2);
\draw[arr] (-.4,0)--(5,0) node[below right]{optical axis};
\draw[thick,blue!70!black] (C)--(3.2,3.2) (C)--(3.2,-3.2);
\draw[thick] (3.2,-3.2)--(3.2,3.2);
\draw[<->] (3.8,-3.2)--(3.8,3.2) node[pos=.75,right]{$W=640$};
\draw[<->] (0,-3.8)--(3.2,-3.8) node[midway,below]{$f_x=320$};
\draw (1,0) arc(0:45:1) node[midway,right]{$45^\circ$};
\fill (C) circle(2pt) node[left]{camera};
\node[align=left] at (8.5,1.7){Top view: horizontal angle\\$\theta=90^\circ$\\Lengths in pixel-scaled units};
\node[align=left] at (8.5,-1){Half-angle triangle:\\$\tan45^\circ=320/320=1$};
''',
'ray-plane': r'''
\draw[arr] (0,0)--(10.6,0) node[right]{$Z$};
\draw[arr] (0,0)--(0,4) node[above]{$X$};
\draw[blue!70!black,thick] (2,-.2)--(2,3.5) node[above]{image plane $Z=f=2$};
\draw[orange!85!black,very thick] (0,0)--(9,2.25);
\draw[green!40!black,very thick] (6.5,3.5)--(10,0);
\node[green!40!black] at (8.5,3.7){$X+Z=10$};
\fill (0,0) circle(2pt) node[below left]{$C$};
\fill[blue!70!black] (2,.5) circle(2.5pt) node[above left]{$a:(Z,X)=(2,0.5)$};
\fill[orange!85!black] (8,2) circle(3pt) node[above right]{$P:(Z,X)=(8,2)$};
\draw[dashed] (8,2)--(8,0) node[below]{$Z=8$};
\node at (5,-1.2){Side view; $Y$ is suppressed. Scene plane fixes the depth.};
''',
}


def projective():
    body = []
    src = [(0,0),(1,0),(1,1),(0,1)]
    dst = [(0,0),(2,0),(2,1),(0,2)]
    for offset, title, points, center in [(0,'Source square',src,(.5,.5)),(6,'Destination trapezoid',dst,(4/3,2/3))]:
        def p(x,y): return f'({offset+2*x},{2*y})'
        body.append(rf'\node at ({offset+1.8},4.7) {{{title}}};')
        body.append(r'\draw[thick,blue!70!black,fill=blue!5] '+'--'.join(p(*v) for v in points)+'--cycle;')
        for i, (x,y) in enumerate(points):
            body.append(rf'\fill {p(x,y)} circle(2pt) node[below right]{{{i+1}}};')
        body.append(rf'\fill[orange!85!black] {p(*center)} circle(3pt);')
    body.append(r'\draw[thick] (7.9,1.5)--(8.1,1.5) (8,1.4)--(8,1.6);')
    body.append(r'\node[align=left] at (8,-1){Orange: mapped center $(4/3,2/3)$\\Cross: vertex average $(1,3/4)$};')
    body.append(r'\node at (1,-1){Orange: source center $(1/2,1/2)$};')
    return '\n'.join(body)


def pentagon():
    body = []
    for panel, numbers, title in [(0,[1,2,3,4,5],'One alignment'),(1,[5,1,2,3,4],'Rotated ordering'),(2,[1,5,4,3,2],'Reflected ordering')]:
        points = [(panel*4.2+1.4*math.cos(math.pi/2+i*2*math.pi/5),1.4*math.sin(math.pi/2+i*2*math.pi/5)) for i in range(5)]
        path = '--'.join(f'({x},{y})' for x,y in points)
        body.append(r'\draw[thick,blue!70!black,fill=blue!5] '+path+'--cycle;')
        body.append(rf'\node at ({panel*4.2},2.1) {{{title}}};')
        for (x,y),number in zip(points,numbers):
            body.append(rf'\node at ({panel*4.2+1.25*(x-panel*4.2)},{y*1.25}) {{{number}}};')
    body.append(r'\node at (4.2,-2.3){Same visible outline; labels are explanatory only.};')
    return '\n'.join(body)


def probability():
    body = [r'\draw[arr] (0,0)--(10.5,0) node[right]{$N$ trials};',r'\draw[arr] (0,0)--(0,5.6) node[above]{Success probability};']
    for n in [0,1000,2000,3000]:
        body.append(rf'\node[below] at ({n/300},0) {{{n}}};')
    for p in [0,.5,.99]:
        body.append(rf'\draw[gray!40,dashed] (0,{p*5})--(10,{p*5});\node[left] at (0,{p*5}) {{{p*100:g}\%}};')
    for w, color in [(.2,'blue!70!black'),(.5,'orange!85!black')]:
        coords = ' '.join(f'({n/300},{-math.expm1(n*math.log1p(-w**4))*5})' for n in range(0,3001,10))
        body.append(rf'\draw[very thick,{color}] plot coordinates {{{coords}}};')
    body.append(r'\node[blue!70!black,fill=white] at (5,4.1){$w=20\%$};')
    body.append(r'\node[orange!85!black,fill=white] at (2.5,5.35){$w=50\%$};')
    body.append(r'\node at (5,-1){Four independent match statuses per hypothesis: $q=w^4$.};')
    return '\n'.join(body)


def main():
    tikz.OUT = OUT
    figures = {**DIAGRAMS,'projective-dlt':projective(),'pentagon-symmetry':pentagon(),'ransac-probability':probability()}
    for name, body in figures.items():
        print('Built',tikz.compile_one((name,body)))

if __name__ == '__main__':
    main()
