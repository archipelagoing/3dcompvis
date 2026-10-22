#!/usr/bin/env python3
"""Retain the supplied booklet's camera-plane/epipolar sketches as paired vectors."""
from pathlib import Path
import re
import build_lecture01_figures as tikz
from render_quiz_workbooks import balanced
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'3dcvMid/lectures/CS532_18_Quizzes_By_Lecture.tex').read_text()
tikz.OUT=ROOT/'book/images/quizzes'
for macro,name in [('PosePlaneDiagram','camera-plane'),('EpipolarDiagram','epipolar-plane')]:
 start=source.index('\\newcommand{\\'+macro+'}{')+len('\\newcommand{\\'+macro+'}')
 definition,_=balanced(source,start)
 body=re.search(r'\\begin\{tikzpicture\}\[[^\]]*\](.*?)\\end\{tikzpicture\}',definition,re.S)[1]
 colors=r'\definecolor{navy}{RGB}{21,50,78}\definecolor{solveRed}{RGB}{171,26,40}\definecolor{muted}{RGB}{70,79,92}'
 print(tikz.compile_one((name,colors+'\n'+body)))
