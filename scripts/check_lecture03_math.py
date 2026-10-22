#!/usr/bin/env python3
"""Independent numerical checks for Lecture 3's new applications."""
from itertools import combinations
from math import comb, ceil, log, log1p, tan, pi
import numpy as np


def normalized(points):
    centroid = points.mean(axis=0)
    scale = np.sqrt(2) / np.linalg.norm(points-centroid, axis=1).mean()
    transform = np.array([[scale,0,-scale*centroid[0]],[0,scale,-scale*centroid[1]],[0,0,1]])
    return transform, (transform @ np.column_stack((points,np.ones(len(points)))).T).T


def run():
    np.testing.assert_allclose(640/(2*tan(pi/4)),320)
    np.testing.assert_allclose(320*.005,1.6)
    scene = np.array([2,1,20]); image = scene/10
    np.testing.assert_allclose(image,[.2,.1,2])
    np.testing.assert_allclose(np.cross(scene,image),0,atol=1e-14)
    q = np.array([.25,.125,1]); plane = np.array([1,0,1,-10])
    depth = -plane[3]/(plane[:3]@q); point = depth*q
    np.testing.assert_allclose(point,[2,1,8]); assert plane@np.r_[point,1] == 0
    for scale in [1e-8,-3,1e8]:
        scaled=plane*scale
        np.testing.assert_allclose(-scaled[3]/(scaled[:3]@q),depth)
    np.testing.assert_allclose(2*point[:2]/point[2],[.5,.25])
    assert np.array([1,0,0])@np.array([0,0,1]) == 0 # parallel plane X=1
    assert -1/(np.array([0,0,1])@q) < 0 # plane Z=-1 behind camera
    np.testing.assert_allclose(-0/(np.array([0,0,1])@q),0)
    src = np.array([[0,0],[1,0],[1,1],[0,1]],dtype=float)
    dst = np.array([[0,0],[2,0],[2,1],[0,2]],dtype=float)
    t,x = normalized(src); tp,y = normalized(dst)
    rows=[]
    for (u,v,_),(a,b,_) in zip(x,y):
        rows.extend([[u,v,1,0,0,0,-a*u,-a*v,-a],[0,0,0,u,v,1,-b*u,-b*v,-b]])
    matrix=np.array(rows); _,singular,vt=np.linalg.svd(matrix,full_matrices=True)
    assert matrix.shape==(8,9) and vt.shape==(9,9) and np.linalg.matrix_rank(matrix)==8
    null=vt[-1]; np.testing.assert_allclose(matrix@null,0,atol=1e-14)
    expectednull=np.array([.627537813,0,.209179271,-.156884453,.418358542,-.0522948177,.189754836,0,.569264507])
    np.testing.assert_allclose(null*np.sign(null[-1]),expectednull,atol=1e-8)
    ht=null.reshape(3,3); h=np.linalg.inv(tp)@ht@t;h/=h[2,2]
    np.testing.assert_allclose(h,[[4,0,0],[0,2,0],[1,0,1]],atol=1e-13)
    projected=(h@np.column_stack((src,np.ones(4))).T).T
    np.testing.assert_allclose(projected[:,:2]/projected[:,2,None],dst,atol=1e-13)
    center=h@np.array([.5,.5,1]); np.testing.assert_allclose(center[:2]/center[2],[4/3,2/3])
    assert not np.allclose(center[:2]/center[2],dst.mean(axis=0))
    assert len(singular)==8
    # Exhaustively count raw and valid four-pair samples; no independence approximation.
    raw=valid=correct=0
    for sample in combinations([(a,b) for a in range(5) for b in range(5)],4):
        raw+=1
        if len({a for a,b in sample})==4 and len({b for a,b in sample})==4:valid+=1
        if all(a==b for a,b in sample):correct+=1
    assert (raw,valid,correct)==(12650,600,5)
    assert raw==comb(25,4) and correct==comb(5,4)
    for probability,budget in [(.2**4,2876),(correct/raw,11649),(correct/valid,551),(.5**4,72)]:
        assert ceil(log(.01)/log1p(-probability))==budget
        assert -np.expm1(budget*log1p(-probability)) >= .99
        assert -np.expm1((budget-1)*log1p(-probability)) < .99
    np.testing.assert_allclose(1-(7/8)**7,.6073040962219238)
    # Every dihedral ordering preserves the regular pentagon's pairwise distances.
    angles=pi/2+np.arange(5)*2*pi/5; pentagon=np.column_stack((np.cos(angles),np.sin(angles)))
    distances=np.linalg.norm(pentagon[:,None]-pentagon[None,:],axis=2)
    permutations={tuple((sign*np.arange(5)+k)%5) for sign in [-1,1] for k in range(5)}
    assert len(permutations)==10
    for permutation in permutations:
        p=pentagon[list(permutation)]
        np.testing.assert_allclose(np.linalg.norm(p[:,None]-p[None,:],axis=2),distances,atol=1e-14)
    print('PASS: FOV/units; ray/plane and degeneracies; normalized projective DLT/nullspace/reprojection; exact sample enumeration and minimal budgets; coin probabilities; ten pentagon symmetries.')

if __name__=='__main__':run()
