#!/usr/bin/env python3
"""Extract credited source illustrations and compile original L5/L6 vector diagrams."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json
from PIL import Image,ImageDraw,ImageFont
import build_lecture01_figures as tikz
ROOT=Path(__file__).resolve().parents[1]
# Crop rectangles use fractions of the source page, recorded for reproducibility.
PANELS={
 (5,'panorama'):([4,5,6],(.03,.23,.98,.96),['Two photographs','Matched features','Aligned panorama']),
 (5,'mars'):([10],(.03,.22,.97,.94),['Mars Rover feature matches']),
 (5,'patch-types'):([11],(.04,.25,.97,.96),['Flat, edge, and corner windows']),
 (5,'harris-stages'):([28,29,31,32,33],(.03,.25,.97,.96),['Input','Response','Threshold','Local maxima','Selected corners']),
 (5,'motion-pairs'):([36,37],(.03,.23,.97,.98),['Camera motion','Object motion']),
 (5,'aperture'):([42,43,54,55],(.04,.23,.98,.99),['Actual motion','Perceived motion','One direction','Independent directions']),
 (5,'tracking-sign'):([59],(.03,.21,.97,.96),['Street-sign tracking and registration']),
 (5,'descriptor-patterns'):([65,72,77],(.03,.26,.97,.95),['BRIEF comparisons','ORB steering','BRISK rings']),
 (5,'matching-choice'):([90],(.03,.23,.97,.96),['Radius, nearest neighbor, and ratio selection']),
 (6,'tracks'):([5],(.06,.18,.97,.73),['Tracks across facade views']),
 (6,'house-ambiguity'):([15,17,19],(.04,.2,.97,.96),['Projective ambiguity','Affine ambiguity','Similarity ambiguity']),
 (6,'factorization-house'):([38],(.04,.17,.97,.95),['House-model sequence and recovered structure']),
 (6,'visibility'):([45],(.54,.27,.91,.75),['Observed image–point entries']),
}
DECK={5:'wk5_cs532_Corners.pdf',6:'wk6_cs532s24_SFM1.pdf'}
def panel(item):
 (lecture,name),(pages,crop,labels)=item
 out=ROOT/f'book/images/lecture{lecture:02d}';src=out/'sources';src.mkdir(parents=True,exist_ok=True)
 pieces=[]
 for page,label in zip(pages,labels):
  target=src/f'{name}-p{page}'
  subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-singlefile','-r','160','-png',str(ROOT/'3dcvMid/lectures'/DECK[lecture]),str(target)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  im=Image.open(target.with_suffix('.png')).convert('RGB');w,h=im.size
  im=im.crop(tuple(round(v*s) for v,s in zip(crop,(w,h,w,h))))
  pieces.append((im,label))
 # Rows preserve readable diagrams, rather than shrinking five panels across a page.
 cols=2 if len(pieces)>3 else (3 if len(pieces)==3 else 1)
 width=1050 if cols==1 else 700
 scaled=[]
 for im,label in pieces:
  im=im.resize((width,round(im.height*width/im.width)))
  scaled.append((im,label))
 cellh=max(im.height for im,_ in scaled)+52
 sheet=Image.new('RGB',(cols*width,((len(scaled)+cols-1)//cols)*cellh),'white');draw=ImageDraw.Draw(sheet)
 try:font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',25)
 except OSError:font=ImageFont.load_default()
 for j,(im,label) in enumerate(scaled):
  x=j%cols*width;y=j//cols*cellh;draw.text((x+12,y+8),label,fill='#182b49',font=font);sheet.paste(im,(x,y+48))
 sheet.save(out/f'{name}.png',optimize=True);sheet.save(out/f'{name}.pdf',resolution=160)
 (src/f'{name}-extraction.json').write_text(json.dumps({'source':str(Path('3dcvMid/lectures')/DECK[lecture]),'pdf_pages':pages,'fractional_crop':crop,'labels':labels,'rights':'Original supplied teaching material; source captions retain known credits; reuse terms not independently identified.'},indent=2)+'\n')
 return f'L{lecture} {name}'
def surfaces():
 body=[]
 for panel,(title,a,c,b) in enumerate([('Flat',0,0,0),('Edge',8,8,8),('Corner',4,0,9)]):
  ox=panel*5.2
  def point(u,v):return (ox+.75*u+.55*v,.28*v+(a*u*u+2*c*u*v+b*v*v)/24)
  body.append(rf'\node at ({ox},-1.1) {{{title}}};')
  for fixed in [i/4 for i in range(-4,5)]:
   for swap in [False,True]:
    coords=[]
    for j in range(-20,21):
     u,v=(fixed,j/20) if swap else(j/20,fixed)
     x,y=point(u,v);coords.append(f'({x:.4f},{y:.4f})')
    body.append(r'\draw[blue!65!black,thin] plot coordinates {'+' '.join(coords)+'};')
  body.append(rf'\node[align=center] at ({ox},-1.8) {{$M=\left(\begin{{smallmatrix}}{a}&{c}\\{c}&{b}\end{{smallmatrix}}\right)$}};')
 body.append(r'\node at (5.2,3.1) {Quadratic costs $E(u,v)=(u,v)M(u,v)^T$; common vertical scale};')
 return '\n'.join(body)
RAYS=r'''
\coordinate (L) at (0,0);\coordinate (R) at (5,0);\coordinate (T) at (3.25,6.5);\coordinate (Q) at (2.7,5.4);
\draw[thick,blue!70!black] (L)--(4,8) node[above]{fixed left ray};
\draw[thick,orange!80!black] (R)--(T) node[midway,right]{measured right ray};
\draw[dashed,red!75!black,thick] (R)--(Q);
\fill (L) circle(2pt) node[below]{$C_L$};\fill (R) circle(2pt) node[below]{$C_R$};
\fill[blue!70!black] (Q) circle(3pt) node[left]{initial point};
\fill[orange!80!black] (T) circle(3pt) node[right]{consistent point};
\draw[arr,very thick] (2.9,5.8)--(3.15,6.3);
\node[align=left] at (8.8,4){Adjust depth along the left ray.\\Check the right reprojection.\\Cameras stay fixed in this example.};
\draw[<->] (0,-.7)--(5,-.7) node[midway,below]{$b=0.2$ m (schematic)};
'''
PIPELINE=r"""
\node[box] (pair) at (0,0) {Verify tracks\\initialize two cameras};
\node[box] (pose) at (4.5,0) {Register another camera\\from known 3D points};
\node[box] (points) at (9,0) {Triangulate new tracks\\check depth and error};
\node[box] (ba) at (6.7,-2) {Bundle-adjust cameras + points\\fix gauge; filter bad tracks};
\draw[arr] (pair)--(pose);\draw[arr] (pose)--(points);\draw[arr] (points)--(ba);
\draw[arr] (ba.west)--(3,-2)--(3,-.8)--(pose.south);
\node[align=center] at (0,-2) {Continue while new views\\connect to the model.};
"""
def main():
 with ThreadPoolExecutor(max_workers=4) as pool:
  for result in pool.map(panel,PANELS.items()):print(result,flush=True)
 for lecture,items in [(5,{'error-surfaces':surfaces()}),(6,{'refinement-rays':RAYS,'sfm-pipeline':PIPELINE})]:
  tikz.OUT=ROOT/f'book/images/lecture{lecture:02d}'
  for item in items.items():print(tikz.compile_one(item),flush=True)
if __name__=='__main__':main()
