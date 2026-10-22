#!/usr/bin/env python3
"""Generate a small, ordinary XeLaTeX PDF from the compact study edition."""
from pathlib import Path
import re,subprocess
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'For_Dummies.md';out=ROOT/'print';name='CS532_For_Dummies'
def inline(s):
 # The source deliberately uses only bold spans and ordinary text outside display math.
 s=s.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_').replace('#',r'\#')
 s=re.sub(r'\*\*(.+?)\*\*',lambda m:r'\textbf{'+m.group(1)+'}',s)
 if s.startswith(r'\textbf{Step '):s=r'\textcolor{StepRed}{'+s+'}'
 return s
preamble=r'''\documentclass[11pt,letterpaper]{article}
\usepackage[margin=.85in]{geometry}
\usepackage{fontspec}\setmainfont{FreeSerif}\setsansfont{FreeSans}
\usepackage{amsmath,amssymb,xcolor,tcolorbox,enumitem,needspace}
\usepackage[unicode,colorlinks=true,linkcolor=blue!45!black]{hyperref}
\definecolor{StepRed}{HTML}{A71930}\definecolor{MathBlue}{HTML}{124FAD}
\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\setlist[itemize]{nosep,leftmargin=*}
\tcbset{colback=blue!2,colframe=blue!35!black,boxrule=.4pt,arc=2pt,left=5pt,right=5pt,top=3pt,bottom=3pt}
\title{3D Computer Vision\\\large The For Dummies Study Edition}
\author{CS 532 · Lectures 1–6}\date{}
\begin{document}\maketitle
'''
lines=[];listed=False
for line in source.read_text().splitlines():
 if not line.startswith('- ') and listed:lines.append(r'\end{itemize}');listed=False
 if line.startswith('# '):continue
 if line.startswith('## '):
  title=inline(line[3:]);lines.append(r'\Needspace{7\baselineskip}\section*{'+title+'}');continue
 if line.startswith('### '):lines.append(r'\Needspace{6\baselineskip}\subsection*{'+inline(line[4:])+'}');continue
 if line.startswith('$$ '):
  math=line.removeprefix('$$ ').removesuffix(' $$');lines.append(r'\begin{tcolorbox}\color{MathBlue}\['+math+r'\]\end{tcolorbox}');continue
 if line.startswith('- '):
  if not listed:lines.append(r'\begin{itemize}');listed=True
  lines.append(r'\item '+inline(line[2:]));continue
 lines.append(inline(line)+'\n')
if listed:lines.append(r'\end{itemize}')
(out/f'{name}.tex').write_text(preamble+'\n'.join(lines)+'\n'+r'\end{document}'+'\n')
with (out/f'{name}.log-build').open('w') as log:
 subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',f'{name}.tex'],cwd=out,check=True,stdout=log,stderr=subprocess.STDOUT)
print('Generated:',out/f'{name}.pdf')
