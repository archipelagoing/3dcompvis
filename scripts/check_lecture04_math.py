#!/usr/bin/env python3
"""Independent checks of Lecture 4 quiz answers, noisy fit, pose and stereo costs."""
from pathlib import Path
import math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def normalize(points):
    center=points.mean(axis=0)
    scale=np.sqrt(2)/np.linalg.norm(points-center,axis=1).mean()
    T=np.array([[scale,0,-scale*center[0]],[0,scale,-scale*center[1]],[0,0,1]])
    return T,(T@np.column_stack((points,np.ones(len(points)))).T).T

def fit_f(left,right):
    T,x=normalize(left);Tp,y=normalize(right)
    A=np.array([np.outer(b,a).ravel() for a,b in zip(x,y)])
    _,_,vt=np.linalg.svd(A,full_matrices=True)
    raw=vt[-1].reshape(3,3);u,s,v=np.linalg.svd(raw)
    ranktwo=u@np.diag([s[0],s[1],0])@v
    return Tp.T@ranktwo@T,(T,Tp,A,raw,s)

def symmetric_rms(F,left,right):
    x=np.column_stack((left,np.ones(len(left))));y=np.column_stack((right,np.ones(len(right))))
    lp=x@F.T;l=y@F;r=np.einsum('ij,ij->i',y,lp)
    return np.sqrt(np.mean(r*r*(1/np.sum(lp[:,:2]**2,axis=1)+1/np.sum(l[:,:2]**2,axis=1))))

def synthetic_data():
    rng=np.random.default_rng(5324)
    X=np.column_stack((rng.uniform(-2,2,16),rng.uniform(-1.5,1.5,16),rng.uniform(4,9,16)))
    a=np.deg2rad(9);R=np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])
    t=np.array([-.8,.12,.05]);K=np.array([[800,0,320],[0,780,240],[0,0,1]]);Kp=np.array([[820,0,300],[0,790,250],[0,0,1]])
    def project(k,points):
        homogeneous=(k@points.T).T
        return homogeneous[:,:2]/homogeneous[:,2,None]
    left=project(K,X);right=project(Kp,X@R.T+t)
    train_left=np.round(left[:12]+rng.normal(0,.25,(12,2)),2)
    train_right=np.round(right[:12]+rng.normal(0,.25,(12,2)),2)
    return train_left,train_right,left[12:],right[12:],R,t,K,Kp

def skew(t):
    x,y,z=t
    return np.array([[0,-z,y],[z,0,-x],[-y,x,0]])

def ncc(a,b):
    a=np.array(a,float);b=np.array(b,float);a-=a.mean();b-=b.mean()
    norm=np.linalg.norm(a)*np.linalg.norm(b)
    return np.dot(a,b)/norm if norm else np.nan

def run():
    F=np.arange(1,10).reshape(3,3);xa=np.array([1,0,1]);xb=np.array([0,1,1])
    assert xb@F@xa==F[1,0]+F[1,2]+F[2,0]+F[2,2]
    fac=skew([0,-1,0]);fbc=skew([1,-1,0]);la=fac@np.array([.5,.75,1]);lb=fbc@np.array([.25,.75,1])
    intersection=np.cross(la,lb);intersection/=intersection[2]
    np.testing.assert_allclose(intersection,[.5,.5,1]);np.testing.assert_allclose([la@intersection,lb@intersection],0)
    np.testing.assert_allclose(np.cross(la,2*la),0)
    assert np.cross([1,0,-2],[1,0,-3])[2]==0
    invalid=np.array([[1,2,1],[0,1,2],[1,0,1]])
    np.testing.assert_allclose(np.linalg.det(invalid),4);assert np.linalg.matrix_rank(invalid)==3
    np.testing.assert_allclose(np.array([1,2,1])@invalid,[2,4,6])
    for point in [[-3,0,1],[-5,1,1]]:assert np.array([1,2,1])@invalid@point==0
    l,r,hl,hr,R,t,K,Kp=synthetic_data()
    supplied=np.loadtxt(ROOT/'authoring/lecture04-matches.csv',delimiter=',',skiprows=1)
    np.testing.assert_array_equal(supplied,np.column_stack((l,r)))
    fitted,details=fit_f(l,r);T,Tp,A,raw,s=details
    assert A.shape==(12,9) and np.linalg.matrix_rank(A)==9
    np.testing.assert_allclose(s,[.718384553,.695645968,.000567882545],rtol=1e-7)
    assert np.linalg.matrix_rank(fitted)==2
    np.testing.assert_allclose(symmetric_rms(fitted,l,r),.4901356443,atol=1e-8)
    np.testing.assert_allclose(symmetric_rms(fitted,hl,hr),.3301035797,atol=1e-8)
    E=skew(t)@R;trueF=np.linalg.inv(Kp).T@E@np.linalg.inv(K)
    np.testing.assert_allclose(Kp.T@trueF@K,E,atol=1e-14)
    singular=np.linalg.svd(E,compute_uv=False)
    np.testing.assert_allclose(singular[:2],np.linalg.norm(t));assert singular[2]<1e-14
    # Pose construction itself, including proper determinant signs.
    E=np.array([[0,0,0],[0,0,1],[0,-1,0]],float)
    U,s,Vt=np.linalg.svd(E)
    if np.linalg.det(U)<0:U[:,-1]*=-1
    if np.linalg.det(Vt)<0:Vt[-1,:]*=-1
    W=np.array([[0,-1,0],[1,0,0],[0,0,1]])
    x=np.array([.2,.1,1]);xp=np.array([0,.1,1]);visible=[]
    for rotation in [U@W@Vt,U@W.T@Vt]:
        np.testing.assert_allclose(rotation.T@rotation,np.eye(3),atol=1e-14)
        np.testing.assert_allclose(np.linalg.det(rotation),1)
        for translation in [U[:,2],-U[:,2]]:
            depths=np.linalg.lstsq(np.column_stack((-rotation@x,xp)),translation,rcond=None)[0]
            np.testing.assert_allclose(depths[1]*xp,rotation@(depths[0]*x)+translation,atol=1e-14)
            if np.all(depths>0):visible.append((rotation,translation,depths))
    assert len(visible)==1
    np.testing.assert_allclose(visible[0][0],np.eye(3),atol=1e-14)
    np.testing.assert_allclose(visible[0][1],[-1,0,0]);np.testing.assert_allclose(visible[0][2],[5,5])
    for b,f,d,delta in [(10,50,25,-1),(10,50,25,1),(10,5,3,-1),(10,5,3,1)]:
        z=f*b/d;zhat=f*b/(d+delta)
        np.testing.assert_allclose(zhat-z,-f*b*delta/(d*(d+delta)))
    np.testing.assert_allclose([500/24-20,500/26-20],[5/6,-10/13])
    np.testing.assert_allclose([50/2-50/3,50/4-50/3],[25/3,-25/6])
    assert math.ceil(math.log(.01)/math.log1p(-.8**7))==20
    assert math.ceil(math.log(.01)/math.log1p(-.8**8))==26
    assert [math.ceil(math.log(.05)/math.log1p(-w**7)) for w in [.9,.8,.7,.6,.5]]==[5,13,35,106,382]
    np.testing.assert_allclose([50*.1/5,50*.1/1],[1,5])
    L=np.array([10,20,30]);good=np.array([30,40,50]);bad=np.array([10,20,10])
    assert [np.abs(L-good).sum(),np.abs(L-bad).sum()]==[60,20]
    assert [((L-good)**2).sum(),((L-bad)**2).sum()]==[1200,400]
    np.testing.assert_allclose([ncc(L,good),ncc(L,bad)],[1,0],atol=1e-14);assert np.isnan(ncc(L,[20]*3))
    bits=np.array([10,30,15,25])<20;other=np.array([5,10,30,40])<20
    assert bits.sum()==other.sum()==2 and np.count_nonzero(bits!=other)==2
    weights=np.exp(-np.array([0,40])/10-.5)
    np.testing.assert_allclose([np.dot(weights,[0,10])/weights.sum(),np.dot(weights,[10,0])/weights.sum()],[.1798620996,9.8201379004],atol=1e-8)
    for scale in [1e-8,-2,1e7]:
        ell=scale*np.array([0,-2,6]);np.testing.assert_allclose(abs(ell@np.array([5,4,1]))/np.linalg.norm(ell[:2]),1)
    print('PASS: all quiz subparts, rank-three source erratum, noisy normalized fit/held-out errors, essential constraints/four poses, signed stereo errors/ranges, RANSAC sizes, patch scores/Census/adaptive support.')

if __name__=='__main__':run()
