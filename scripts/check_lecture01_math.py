#!/usr/bin/env python3
"""Independent numerical checks of the chapter's worked geometric examples."""
import numpy as np
from numpy.testing import assert_allclose as same


def R(axis,angle):
    a=np.zeros(3);a[axis]=1
    cross=np.array([[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]])
    return np.eye(3)*np.cos(angle)+(1-np.cos(angle))*np.outer(a,a)+np.sin(angle)*cross


def quatmul(a,b):
    w,v=a[0],a[1:]; z,u=b[0],b[1:]
    return np.r_[w*z-v@u,w*u+z*v+np.cross(v,u)]


def transform(r,t):
    a=np.eye(4);a[:3,:3]=r;a[:3,3]=t
    return a


def main():
    same(np.cross([0,1,-1],[0,1,-2]),[-1,0,0])
    same(np.cross([1,0,-2],[0,1,-3]),[2,3,1])
    p=np.array([3.,1.]);c=np.array([2.,1.]);r=R(2,np.pi/2)[:2,:2]
    same(c+r@(p-c),[2,2],atol=1e-12)
    h=np.array([[1.,0,2],[0,1,0],[0,0,1]])
    same(np.linalg.solve(h.T,[1,0,0]),[1,0,-2])
    pts=np.array([[1.,0,0,1],[0,1,0,1],[0,0,1,1]])
    _,_,vh=np.linalg.svd(pts,full_matrices=True)
    pi=vh[-1];same(pts@pi,0,atol=1e-12);same(pi/pi[0],[1,1,1,-1])
    cols=pts.T
    cofactors=np.array([(-1)**i*np.linalg.det(np.delete(cols,i,axis=0)) for i in range(4)])
    same(cofactors,[1,1,1,-1])
    p1=np.array([0,1,0]);d1=np.array([1,0,0]);p2=np.array([0,0,2]);d2=np.array([0,1,0])
    m1=np.cross(p1,d1);m2=np.cross(p2,d2)
    distance=abs(d1@m2+d2@m1)/np.linalg.norm(np.cross(d1,d2))
    # Independent closest-points least-squares calculation.
    alpha=np.linalg.lstsq(np.column_stack([d1,-d2]),p2-p1,rcond=None)[0]
    same(distance,np.linalg.norm((p1+alpha[0]*d1)-(p2+alpha[1]*d2)))
    same(distance,2.)
    same(np.cross(d1,m1)/(d1@d1),p1)
    rx,rz=R(0,np.pi/2),R(2,np.pi/2);v=np.array([1.,0,0])
    same(rx@rz@v,[0,0,1],atol=1e-12);same(rz@rx@v,[0,1,0],atol=1e-12)
    # Verify the expanded body-xyz matrix against independently built rotations.
    a,b,c=.2,-.4,.7;ca,cb,cc=np.cos([a,b,c]);sa,sb,sc=np.sin([a,b,c])
    expanded=np.array([[cb*cc,-cb*sc,sb],[sa*sb*cc+ca*sc,-sa*sb*sc+ca*cc,-sa*cb],[-ca*sb*cc+sa*sc,ca*sb*sc+sa*cc,ca*cb]])
    same(expanded,R(0,a)@R(1,b)@R(2,c),atol=1e-12)
    q=np.array([2**-.5,0,0,2**-.5]);qi=q*np.array([1,-1,-1,-1]);pure=np.array([0.,1,0,0])
    same(quatmul(quatmul(q,pure),qi),[0,0,1,0],atol=1e-12)
    same(quatmul(quatmul(qi,pure),q),[0,0,-1,0],atol=1e-12)
    t1=transform(np.eye(3),[1,1,4]);t2=transform(np.eye(3),[-1,1,4]);rel=t1@np.linalg.inv(t2)
    same(rel[:3,3],[2,0,0]);same(rel@np.r_[t2[:3,3],1],np.r_[t1[:3,3],1])
    # A non-identity pose check catches accidentally commuting rotations/translations.
    a1=transform(R(0,.3),[1,2,4]);a2=transform(R(2,-.7),[-1,3,2]);test=np.array([2.,-1,4,1])
    same((a1@np.linalg.inv(a2))@(a2@test),a1@test)
    same(np.cross([1,1,4],[2,0,0]),[0,8,-2])
    vertices=np.array([[1.,1,0],[1,2,0],[1,1,1],[2,1,0]])
    faces=[(0,1,2),(0,1,3),(0,2,3),(1,2,3)]
    expected=np.array([[-1,0,0],[0,0,-1],[0,-1,0],np.ones(3)/np.sqrt(3)])
    for ids,want in zip(faces,expected):
        A,B,C=vertices[list(ids)];n=np.cross(B-A,C-A);other=next(i for i in range(4) if i not in ids)
        if n@(vertices[other]-A)>0:n=-n
        n/=np.linalg.norm(n);same(n,want);same(n@(B-A),0,atol=1e-12)
        rotated=(rz@vertices.T).T;Ar,Br,Cr=rotated[list(ids)];nr=np.cross(Br-Ar,Cr-Ar)
        if nr@(rotated[other]-Ar)>0:nr=-nr
        same(nr/np.linalg.norm(nr),rz@want,atol=1e-12)
    def pixel(x):return 250+500*np.asarray(x[:2])/x[2]
    point=np.array([1.,.5,10]);same(pixel(point),[300,275]);same(pixel(point-[0,0,2]),[312.5,281.25])
    branch=R(2,np.pi/4)@point+[0,0,5];same(pixel(branch),[261.7851130197758,285.3553390593274])
    cumulative=R(2,np.pi/4)@(point-[0,0,2])+[0,0,5]
    same(pixel(cumulative),[263.5982073305105,290.7946219915316])
    K=np.array([[500.,0,250],[0,500,250],[0,0,1]])
    X1=10*np.linalg.solve(K,[300,250,1]);X2=10*np.linalg.solve(K,[200,250,1])+[2,0,0];same(X1,X2)
    same(np.cross([1,0,2],[2,1,6]),[-2,-2,1])
    print('Lecture 1 numerical checks passed: intersections, dual transforms, SVD/cofactors, line distance, rotations/quaternions, frame composition, quiz normals, projection and backprojection.')


if __name__=='__main__':main()
