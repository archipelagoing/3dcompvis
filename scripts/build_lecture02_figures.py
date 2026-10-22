#!/usr/bin/env python3
"""Rebuild mathematical diagrams and the supplied court's computed image warp."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import build_lecture01_figures as tikz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'book/images/lecture02'
COURT_POINTS=np.array([[24,194],[250,45],[410,70],[280,278]],float)
COURT_TARGET=np.array([[0,0],[279,0],[279,149],[0,149]],float)

def normalization(points):
    center=points.mean(axis=0)
    scale=np.sqrt(2)/np.linalg.norm(points-center,axis=1).mean()
    T=np.array([[scale,0,-scale*center[0]],[0,scale,-scale*center[1]],[0,0,1]])
    return T

def fit_homography(source,target):
    T=normalization(source); Tp=normalization(target)
    a=(T@np.column_stack((source,np.ones(len(source)))).T).T
    b=(Tp@np.column_stack((target,np.ones(len(target)))).T).T
    rows=[]
    for (u,v,_),(up,vp,_) in zip(a,b):
        rows.extend([[u,v,1,0,0,0,-up*u,-up*v,-up],
                     [0,0,0,u,v,1,-vp*u,-vp*v,-vp]])
    _,_,vt=np.linalg.svd(rows,full_matrices=True)
    H=np.linalg.inv(Tp)@vt[-1].reshape(3,3)@T
    return H/np.linalg.norm(H)

def court_demo():
    image=Image.open(OUT/'sources/court-source.png').convert('RGB')
    H=fit_homography(COURT_POINTS,COURT_TARGET)
    inverse=np.linalg.inv(H);inverse/=inverse[2,2]
    warped=image.transform((280,150),Image.Transform.PERSPECTIVE,
        tuple(inverse.flatten()[:8]),resample=Image.Resampling.BILINEAR)
    marked=image.copy();draw=ImageDraw.Draw(marked)
    colors=['#b00000','#006400','#0000af','#7a007a']
    for k,((x,y),color) in enumerate(zip(COURT_POINTS,colors)):
        draw.ellipse((x-5,y-5,x+5,y+5),fill=color,outline='white',width=2)
        draw.text((x+7,y-12),str(k+1),fill=color,stroke_width=1,stroke_fill='white')
    canvas=Image.new('RGB',(800,405),'white');d=ImageDraw.Draw(canvas)
    d.text((12,10),'Source photo: numbered floor corners',fill='black')
    d.text((510,10),'Computed rectangular floor warp',fill='black')
    canvas.paste(marked,(0,35));canvas.paste(warped,(510,125))
    canvas.save(OUT/'court-demo.png')
    np.savetxt(OUT/'sources/court-homography.txt',H,header='Source to destination, matrix scale arbitrary')

DIAGRAMS={
'quiz-lines':r'''
\draw[arr] (-3,0)--(3,0) node[right]{$\ell_3:y=0$};
\draw[arr] (0,-.8)--(0,3.3) node[above]{$y$};
\draw[very thick,blue!70!black] (-2,-.5)--(-2,3) node[above left]{$x=-d$};
\draw[very thick,orange!85!black] (2,-.5)--(2,3) node[above right]{$x=d$};
\fill (-2,0) circle(2pt) node[below left]{$(-d,0,1)^T$};
\fill (2,0) circle(2pt) node[below right]{$(d,0,1)^T$};
\node[align=center] at (0,-1.6){The vertical lines share ideal point $(0,1,0)^T$.\\It is not a finite location above this drawing.};
''',
'warp-grids':r'''
\node at (1.5,2.4){Forward: source $\to$ output};
\foreach \x in {0,1,2,3}{\fill[blue!75!black] (\x,1.5) circle(2pt);\draw[arr] (\x,1.3)--({1.4*\x},.2);}
\foreach \x in {0,1,2,3,4}{\draw[gray] (\x,-.15)--(\x,.15);}
\node[align=center] at (2,-.8){Rounded placement can\\skip output pixels.};
\begin{scope}[shift={(7,0)}]
\node at (1.5,2.4){Inverse: output $\to$ source};
\foreach \x in {0,1,2,3}{\fill[orange!85!black] (\x,0) circle(2pt);\draw[arr] (\x,.2)--({\x/1.4},1.3);}
\foreach \x in {0,1,2,3}{\draw[gray] (\x,1.35)--(\x,1.65);}
\node[align=center] at (1.5,-.8){Every output pixel\\asks for a sample.};
\end{scope}
''',
'ransac':r'''
\draw[arr] (0,0)--(8,0);\draw[arr] (0,0)--(0,4);
\draw[very thick,blue!70!black] (.3,.6)--(7.6,3.2);
\foreach \x/\y in {.6/.75,1/1,1.7/1.15,2.4/1.4,3/1.65,3.6/1.73,4.3/2.05,5/2.22,5.8/2.6,6.5/2.78,7.2/3.05}{\fill[blue!70!black] (\x,\y) circle(2.5pt);}
\foreach \x/\y in {1/3.4,2/2.9,3/.4,4/3.7,5.2/.8,6/1,7/1.2}{\draw[orange!90!black,thick] (\x-.06,\y-.06)--(\x+.06,\y+.06) (\x-.06,\y+.06)--(\x+.06,\y-.06);}
\node[align=left] at (3.4,4.2){Dots: model consensus. Crosses: outliers.};
''',
'epipolar':r'''
\foreach \offset/\name in {0/left,6/right}{
\draw[thick] (\offset,0) rectangle (\offset+4,3);
\foreach \y in {.6,1.5,2.4}{\draw[gray,dashed] (\offset,\y)--(\offset+4,\y);}
\node at (\offset+2,-.5){\name\ image};}
\fill[blue!70!black] (1.8,1.5) circle(3pt) node[above]{$x$};
\draw[very thick,orange!85!black] (6,1.5)--(10,1.5) node[right]{$\ell'=Fx$};
\fill[orange!85!black] (7.3,1.5) circle(3pt) node[above]{$x'$};
\draw[arr] (4.2,2.5)--(5.8,2.5);
\node[align=center] at (5,4){Rectified special case: equal rows;\\horizontal position still depends on depth.};
'''
}

if __name__=='__main__':
    tikz.OUT=OUT
    with ThreadPoolExecutor(max_workers=3) as pool:
        for name in pool.map(tikz.compile_one,DIAGRAMS.items()):print('Built',name,flush=True)
    court_demo();print('Built court-demo',flush=True)
