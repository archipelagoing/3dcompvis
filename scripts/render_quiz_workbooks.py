#!/usr/bin/env python3
"""Render the reviewed quiz inventory into editable MyST workbook pages.

Explicit maintenance command, not a build hook. Edit authoring/quiz-worked-content.json
for synchronized quiz revisions, then run this script. The rest of book/ remains MyST.
Problem wording is imported from the supplied lecture-organized quiz booklet.
"""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]

def balanced(text,start):
    assert text[start]=='{'
    depth=1;i=start+1
    while depth:
        if text[i]=='{' and text[i-1]!='\\':depth+=1
        elif text[i]=='}' and text[i-1]!='\\':depth-=1
        i+=1
    return text[start+1:i-1],i

def prose(text):
    # Preserve math exactly while converting the booklet's few prose macros.
    saved=[]
    def hold(match):
        saved.append(match.group());return f'@@MATH{len(saved)-1}@@'
    text=re.sub(r'\\\[.*?\\\]|\$(?:\\.|[^$])*\$',hold,text,flags=re.S)
    for macro,delim in [('emph','*'),('textbf','**'),('textit','*')]:
        while (m:=re.search(r'\\'+macro+r'\{',text)):
            content,end=balanced(text,m.end()-1)
            text=text[:m.start()]+delim+content+delim+text[end:]
    text=text.replace('---','—').replace('--','–').replace('``','“').replace("''",'”')
    text=text.replace(r'\%', '%').replace(r'\_', '_').replace(r'\emph','')
    for i,math in enumerate(saved):
        if math.startswith(r'\['):
            math='\n\n$$\n'+math[2:-2].strip()+'\n$$\n\n'
        elif '\\begin{' in math or len(math)>160:
            math='\n\n$$\n'+math[1:-1]+'\n$$\n\n'
        text=text.replace(f'@@MATH{i}@@',math)
    text=text.replace('\n\n; homogeneous line ', '\n\nA homogeneous line is ')
    return re.sub(r'\n{3,}','\n\n',text).strip()

ALIASES={
('17',2):['ex-lec01-relative-pose'],('17',3):['ex-lec01-object-plane'],
('18',0):['ex-lec01-depth'],('18',1):['ex-lec01-tetrahedron'],('18',2):['ex-lec01-rotated-normals'],
('8',0):['ex-lec02-collinear'],('8',1):['ex-lec02-projection'],('8',2):['ex-lec02-intersections'],
('7',0):['ex-lec03-pentagon','ex-lec03-symmetry'],('10',0):['ex-lec03-calibration'],('10',2):['ex-lec03-principal'],
('14',0):['ex-lec03-ray'],('1',0):['ex-lec04-symbolic'],('3',0):['ex-lec04-third-view'],('3',1):['ex-lec04-invalid-f'],
('4',0):['ex-lec04-stereo-fall'],('4',1):['ex-lec04-search'],('5',0):['ex-lec04-stereo-spring'],
('17',0):['ex-lec03-probability'],
}
DIAGRAMS={
('17',3):('quizzes/camera-plane','The two camera centers and object origin determine a plane when noncollinear. Schematic from the supplied quiz booklet.'),
('18',0):('lecture01/depth-rays','Two camera rays meet at the same point after both depth maps are transformed into one frame.'),
('18',1):('lecture01/tetrahedron','The tetrahedron from the problem, with all four given vertices.'),
('8',2):('lecture02/quiz-lines','Two finite intersections and one vertical point at infinity.'),
('10',0):('lecture03/fov','The half-width and half field of view determine pixel focal length.'),
('11',0):('lecture03/fov','The same half-angle construction applies to this separate retest.'),
('1',0):('quizzes/epipolar-plane','The supplied booklet’s schematic shows the two cameras, corresponding rays and epipolar plane. The line’s slant is illustrative; in 3D it is the intersection of that plane with image plane B.'),
('2',0):('quizzes/epipolar-plane','The same schematic is reproduced beside this separate retest. The camera rays and baseline lie in one epipolar plane.'),
('3',0):('lecture04/third-view','The two numerical companion lines intersect at the predicted third-image point.'),
('4',0):('lecture04/depth-sensitivity','The same pixel error produces much larger depth errors at smaller disparity.'),
('14',0):('lecture01/pinhole','Pinhole viewing-ray sketch, shown as a side view. In this quiz the image-plane point is one tenth of the scene vector; the schematic is not drawn to that scale.'),
('15',0):('lecture03/ray-plane','A ray–plane illustration. Its numerical labels belong to the separate Example 3.4 companion in the teaching section.'),
}

def render_problem(quiz,i,p):
    out=[];qid=quiz['booklet_id'];aliases=ALIASES.get((qid,i),[])
    out.extend(f'({label})=' for label in aliases)
    out += [f'({p["key"]})=',f'### {prose(p["part"])}','',
            '````{original-question}',prose(p['question']),'````','']
    for given in p['given']:out+=['**Given / relevant facts:**','',prose(given),'']
    out+=['**Fully worked solution** — red labels explain the step; blue mathematics shows the calculation.','']
    for n,step in enumerate(p['worked_steps'],1):
        out += [f'````{{solution-step}} {n} — {step["title"]}',
                '**Why:** '+step['why'],'',prose(step['body']),'````','']
    for note in p['notes']:out+=['**Source check / assumptions:** '+prose(note),'']
    diagram=DIAGRAMS.get((qid,i))
    if diagram:
        path,caption=diagram
        out += [f'```{{figure}} ../../images/{path}.*',':width: 70%',':alt: '+caption,'',caption,'```','']
    return '\n'.join(out)

def main():
    quizzes=json.loads((ROOT/'authoring/quiz-worked-content.json').read_text())
    sources=list((ROOT/'3dcvMid').rglob('*.pdf'))
    for lecture in range(1,7):
        selected=[q for q in quizzes if q['lecture']==lecture]
        out=[f'(lec{lecture:02d}-quiz-workbook)=',f'# Original quiz questions and worked solutions','',
             '**Read the problem in black. Follow the numbered red steps. Work through the blue mathematics.** Every step explains why it is needed. Matrix calculations show the inputs and intermediate results; written-reasoning questions explain the decision instead of inventing numerical data.','',
             '**Source:** the supplied lecture-organized quiz booklet. Full problems follow its wording and givens, with typography normalized; the historical PDF filenames appear below. Source-key corrections and added numerical companions are marked.','',
             '**Retests have their own questions and full solutions.** Problems labeled **Original practice** are the booklet’s seven supplemental examples, separate from the 18 historical quizzes. Colored steps remain numbered and readable in grayscale.','',
             '## Jump to a quiz','']
        for q in selected:
            title=prose(q['title']);label=f'quiz-source-{q["booklet_id"].lower()}'
            out.append(f'- {{ref}}`{title} <{label}>`')
        out+=['','---','']
        for q in selected:
            qid=q['booklet_id'];out += [f'(quiz-source-{qid.lower()})=',f'## {prose(q["title"])}','']
            if q.get('original_supplement'):
                out+=['**Original practice from the supplied booklet; not a historical quiz question.**','']
            else:
                source=next(p for p in sources if p.name==q['source'])
                relative=source.relative_to(ROOT).as_posix()
                out+=['**Historical source:** `'+relative+'`.','']
                if qid in ['1','15']:out+=['**Header note:** this filename contains “2015”; the PDF is printed Spring 2019.','']
                if qid in ['6','11']:out+=['**Header note:** the supplied PDF contains mixed/overprinted year labels. The filename and separate retest entry are retained.','']
            for i,p in enumerate(q['questions']):out += [render_problem(q,i,p),'']
        path=ROOT/f'book/lectures/lecture{lecture:02d}/quiz-workbook.md'
        path.write_text('\n'.join(out).rstrip()+'\n')
        print('Rendered',path.relative_to(ROOT))
if __name__=='__main__':main()
