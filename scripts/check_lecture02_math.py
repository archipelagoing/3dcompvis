#!/usr/bin/env python3
"""Independent geometric checks of Lecture 2 examples and generated court mapping."""
import math
import numpy as np
from build_lecture02_figures import fit_homography, normalization, COURT_POINTS, COURT_TARGET


def same(a,b):
    np.testing.assert_allclose(a,b,atol=1e-9)


def qmatrix(q):
    w,x,y,z=q
    return np.array([[1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)],
                     [2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)],
                     [2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)]])


def project(H,p):
    y=(H@np.column_stack([p,np.ones(len(p))]).T).T
    return y[:,:-1]/y[:,-1:]


def main():
    a=np.array([0,0,1]);b=np.array([2,0,1]);c=np.array([5,0,1])
    assert c@np.cross(a,b)==0 and np.array([5,1,1])@np.cross(a,b)==2
    same(np.cross(a,2*a),[0,0,0])
    for d in [1,3,7]:
        l1=np.array([1,0,-d]);l2=np.array([1,0,d]);l3=np.array([0,1,0])
        same(np.cross(l1,l3),[d,0,1]);same(np.cross(l2,l3),[-d,0,1])
        same(np.cross(l1,l2),[0,-2*d,0])
    rng=np.random.default_rng(532)
    for _ in range(30):
        axis=rng.normal(size=3);axis/=np.linalg.norm(axis);theta=rng.uniform(.05,3)
        q=np.r_[np.cos(theta/2),axis*np.sin(theta/2)];R=qmatrix(q)
        skew=np.array([[0,-axis[2],axis[1]],[axis[2],0,-axis[0]],[-axis[1],axis[0],0]])
        # Independent Rodrigues construction and known fixed axis.
        rod=np.eye(3)*np.cos(theta)+(1-np.cos(theta))*np.outer(axis,axis)+np.sin(theta)*skew
        same(R,rod);same(R@axis,axis);same(R.T@R,np.eye(3));same(np.linalg.det(R),1)
        w=.5*np.sqrt(1+np.trace(R))
        recovered=np.r_[w,np.array([R[2,1]-R[1,2],R[0,2]-R[2,0],R[1,0]-R[0,1]])/(4*w)]
        same(qmatrix(recovered),R);same(qmatrix(-q),R)
    cycle=qmatrix([.5,.5,.5,.5]);same(cycle,[[0,0,1],[1,0,0],[0,1,0]])
    same(np.trace(cycle),0)
    angle=np.pi/4;rot=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
    affine=rot.T@np.diag([2,1])@rot
    same(affine,[[1.5,-.5],[-.5,1.5]])
    same(affine@np.array([1,-1]),[2,-2]);same(affine@np.array([1,1]),[1,1])
    half=np.diag([1,-1,-1]);x=.5*np.sqrt(1+half[0,0]-half[1,1]-half[2,2])
    same(qmatrix([0,x,0,0]),half)
    qa=np.array([1,0,0,0]);qb=np.array([np.sqrt(.5),0,0,np.sqrt(.5)])
    omega=np.arccos(qa@qb);mid=np.sin(.5*omega)/np.sin(omega)*(qa+qb)
    same(mid,[np.cos(np.pi/8),0,0,np.sin(np.pi/8)])
    H=np.array([[1,0,0],[0,1,0],[.5,0,1]])
    out=project(H,np.array([[0,0],[1,0],[2,0],[3,0]]))[:,0]
    same(out,[0,2/3,1,6/5])
    cr=lambda a,b,c,d:((c-a)*(d-b))/((c-b)*(d-a))
    same(cr(0,1,2,3),cr(*out));same(cr(*out),4/3)
    same(np.dot([3/8,1/8,3/8,1/8],[10,30,50,70]),35)
    src=np.array([[0,0],[1,0],[1,1],[0,1]])
    dst=np.array([[2,1],[4,1],[4,4],[2,4]])
    fitted=fit_homography(src,dst);expected=np.array([[2,0,2],[0,3,1],[0,0,1]])
    same(fitted/fitted[2,2],expected);same(project(fitted,np.array([[.5,.5]])),[[3,2.5]])
    T=normalization(src);norm=project(T,src)
    same(norm.mean(axis=0),[0,0]);same(np.linalg.norm(norm,axis=1).mean(),np.sqrt(2))
    same(project(fit_homography(COURT_POINTS,COURT_TARGET),COURT_POINTS),COURT_TARGET)
    # A genuinely projective held-out recovery, rather than only an affine fit.
    general=np.array([[1.2,.1,3],[-.1,.9,2],[.03,.02,1]])
    observed=project(general,src);fit=fit_homography(src,observed)
    same(project(fit,np.array([[.2,.7],[.8,.4]])),project(general,np.array([[.2,.7],[.8,.4]])))
    counts=[math.ceil(math.log(.01)/math.log(1-w**4)) for w in [.5,.8]]
    assert counts==[72,9]
    print('RANSAC trial budgets:',counts,'(rounded 56%:',math.ceil(math.log(.01)/math.log(1-.56**4)),')')
    F=np.array([[0,0,0],[0,0,-1],[0,1,0]])
    assert np.linalg.matrix_rank(F)==2;same(F@np.array([2,3,1]),[0,-1,3])
    e=np.array([1,0,0]);same(F@e,[0,0,0]);same(F.T@e,[0,0,0])
    P=np.column_stack([np.eye(3),np.zeros(3)]);Pp=np.column_stack([np.eye(3),[-1,0,0]])
    center=np.array([0,0,0,1]);ep=Pp@center
    cross=np.array([[0,-ep[2],ep[1]],[ep[2],0,-ep[0]],[-ep[1],ep[0],0]])
    from_cameras=cross@Pp@np.linalg.pinv(P);same(from_cameras,-F)
    point=np.array([2,3,1,1]);assert (Pp@point)@from_cameras@(P@point)==0
    same(np.dot([10,15,5,6,9,3,2,3,1],F.flatten()),0)
    # Coordinate-change equations for normalized F and rectifying homographies.
    T=np.array([[2,0,-1],[0,2,-1],[0,0,1]])
    Tp=np.array([[3,0,-2],[0,3,-4],[0,0,1]])
    Ft=np.linalg.inv(Tp).T@F@np.linalg.inv(T)
    same(Tp.T@Ft@T,F)
    print('Lecture 2: quiz geometry, conversions, DLT/warp, probability, and epipolar checks passed.')

if __name__=='__main__':main()
