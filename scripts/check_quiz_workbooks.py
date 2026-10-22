#!/usr/bin/env python3
"""Check full question fidelity/coverage and independently solve new workbook math."""
from pathlib import Path
from itertools import combinations
import json,re,math
import numpy as np
from numpy.testing import assert_allclose as same
from render_quiz_workbooks import prose,balanced
ROOT=Path(__file__).resolve().parents[1]

def main():
    quizzes=json.loads((ROOT/'authoring/quiz-worked-content.json').read_text())
    booklet=(ROOT/'3dcvMid/lectures/CS532_18_Quizzes_By_Lecture.tex').read_text()
    # Parse the supplied problem statements independently of the importer/renderer.
    originals=[]
    for m in re.finditer(r'\\Q\{',booklet[booklet.index('% QUIZ 17'):]):
        section=booklet[booklet.index('% QUIZ 17'):]
        part,pos=balanced(section,m.end()-1)
        while section[pos].isspace():pos+=1
        prompt,_=balanced(section,pos);originals.append((part,prompt))
    problems=[p for q in quizzes for p in q['questions']]
    assert len(quizzes)==25 and sum(not q.get('original_supplement',False) for q in quizzes)==18
    assert len(problems)==46 and len(originals)==46
    assert sorted(originals)==sorted((p['part'],p['question']) for p in problems)
    assert sum(len(p['worked_steps']) for p in problems)==225
    toc=(ROOT/'book/_toc.yml').read_text()
    labels=[]
    for q in quizzes:
        page=ROOT/f'book/lectures/lecture{q["lecture"]:02d}/quiz-workbook.md';text=page.read_text()
        assert str(page.relative_to(ROOT/'book')).removesuffix('.md') in toc
        for p in q['questions']:
            assert prose(p['question']) in text,p['key']
            assert f'({p["key"]})=' in text
            labels.append(p['key'])
            for step in p['worked_steps']:assert step['why'] and step['title'] and step['body']
    assert len(set(labels))==46
    for n in range(1,7):
        text=(ROOT/f'book/lectures/lecture{n:02d}/quiz-workbook.md').read_text()
        assert text.count('{original-question}')==sum(len(q['questions']) for q in quizzes if q['lecture']==n)
        assert text.count('{solution-step}')==sum(len(p['worked_steps']) for q in quizzes if q['lecture']==n for p in q['questions'])
    # Harris: independently sum outer products and solve the characteristic polynomial.
    gradients=np.array([[2.,0],[0,3]])
    tensor=gradients.T@gradients
    same(tensor,[[4,0],[0,9]]);same(np.linalg.eigvalsh(tensor),[4,9])
    same(np.linalg.det(tensor)-.04*np.trace(tensor)**2,29.24)
    # LK: solve original equations directly, then check the expanded normal system.
    target=np.array([4.,3]);motion=np.linalg.lstsq(gradients,target,rcond=None)[0]
    same(motion,[2,1]);same(tensor@motion,[8,9])
    edge=np.tile([1.,1],(8,1));same(np.linalg.eigvalsh(edge.T@edge),[0,16])
    # Affine exposure: normalized correspondence is invariant for nonflat patches.
    a=np.array([10.,20,30]);b=np.array([30.,50,70])
    same((a-a.mean())/a.std(),(b-b.mean())/b.std())
    same((a-a.mean())/a.std(),[-math.sqrt(1.5),0,math.sqrt(1.5)])
    # A1: construct every DLT row from its original matches, not the displayed matrix.
    src=np.array([[0.,0],[1,0],[0,1],[1,1]])
    dst=np.array([[0.,0],[.5,0],[0,1],[.5,.5]])
    rows=[]
    for (x,y),(u,v) in zip(src,dst):
        rows.extend([[x,y,1,0,0,0,-u*x,-u*y,-u],[0,0,0,x,y,1,-v*x,-v*y,-v]])
    A=np.array(rows);_,_,vt=np.linalg.svd(A,full_matrices=True)
    assert vt.shape==(9,9) and np.linalg.matrix_rank(A)==8
    h=vt[-1].reshape(3,3);h/=h[2,2]
    same(h,[[1,0,0],[0,1,0],[1,0,1]],atol=1e-14)
    same(A@h.ravel(),0,atol=1e-14)
    # A4: essential matrix derived from translation; exact equal-pair singular values.
    t=np.array([1.,0,0]);cross=np.array([[0,0,0],[0,0,-1],[0,1,0]])
    same(cross@np.array([2.,3,4]),np.cross(t,[2.,3,4]))
    same(cross.T@cross,np.diag([0,1,1]));same(np.linalg.svd(cross,compute_uv=False),[1,1,0])
    # A5: build triangulation constraints from original camera rows.
    left=np.array([[800.,0,0,0],[0,800,0,0],[0,0,1,0]])
    right=left.copy();right[0,3]=-160
    tri=np.stack([260*left[2]-left[0],120*left[2]-left[1],220*right[2]-right[0],120*right[2]-right[1]])
    _,_,vt=np.linalg.svd(tri);point=vt[-1]/vt[-1,-1]
    same(point,[1.3,.6,4,1],atol=1e-14);same(tri@point,0,atol=1e-12)
    same(np.sqrt(point@point),np.sqrt(19.05))
    for camera,pixel in [(left,[260,120]),(right,[220,120])]:
        projected=camera@point;same(projected[:2]/projected[2],pixel)
    # A6: finite differences check the Jacobian independently of the analytic derivative.
    residual=lambda z:41-160/z
    step=1e-5;j=(residual(4+step)-residual(4-step))/(2*step)
    same(j,10,rtol=1e-9);update=-residual(4)/j;same(update,-.1)
    same(residual(3.9)**2,.0006574621959,rtol=1e-8);assert residual(3.9)**2<residual(4)**2
    same(160/41,3.90243902439,rtol=1e-11)
    # A7: project raw 3D data, center each view, and factor the actual observations.
    points=np.array([[0.,0,0],[2,0,0],[0,2,0],[0,0,2]]).T
    motion=np.array([[1.,0,0],[0,1,0],[0,1,0],[0,0,1]])
    raw=motion@points;D=raw-raw.mean(axis=1,keepdims=True)
    expected=np.array([[-.5,1.5,-.5,-.5],[-.5,-.5,1.5,-.5],[-.5,-.5,1.5,-.5],[-.5,-.5,-.5,1.5]])
    same(D,expected);assert np.linalg.matrix_rank(D)==3;same(motion@(points-points.mean(axis=1,keepdims=True)),D)
    u,s,vt=np.linalg.svd(D);M=u[:,:3]*np.sqrt(s[:3]);S=np.sqrt(s[:3,None])*vt[:3]
    same(M@S,D,atol=1e-14)
    gauge=np.array([[2.,0,.2],[0,1,0],[0,0,3]])
    same((M@gauge)@np.linalg.solve(gauge,S),D,atol=1e-14)
    # SfM ambiguity: two ideal points leave a family of candidate infinity planes.
    ideal=np.array([[1.,0,0,0],[0,1,0,0]])
    assert np.linalg.matrix_rank(ideal)==2
    for plane in [[0,0,1,0],[0,0,0,1]]:same(ideal@plane,0)
    print('PASS: all 46 complete booklet statements match; 18 historical + 7 original entries; 225 meaningful steps; full retests; Harris/LK/exposure/rank, DLT, essential constraints, triangulation/nullspace, finite-difference GN, affine factorization/gauge checks.')
if __name__=='__main__':main()
