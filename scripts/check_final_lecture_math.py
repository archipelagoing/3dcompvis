#!/usr/bin/env python3
"""Independent L5/L6 checks: model identities, updates, gauges, and derivatives."""
import numpy as np
from pathlib import Path

def close(a,b,**kwargs):np.testing.assert_allclose(a,b,rtol=1e-7,atol=1e-8,**kwargs)
# Derive tensors from actual gradient samples, independently of UI tensor constants.
for gradients,target,eigen in [([[0,0],[0,0]],[[0,0],[0,0]],[0,0]),([[2,2],[2,2]],[[8,8],[8,8]],[0,16]),([[2,0],[0,3]],[[4,0],[0,9]],[4,9])]:
 g=np.array(gradients,dtype=float);M=g.T@g;close(M,target);close(np.linalg.eigvalsh(M),eigen)
 for d in [[1,0],[1,-1],[.3,.7]]:close(np.sum((g@d)**2),np.array(d)@M@d)
close(np.linalg.det(np.diag([4,9]))-.04*13**2,29.24)
R=np.array([[1,2,1,0,0],[2,9,8,0,1],[1,7,3,1,2],[0,0,1,6,1],[0,0,0,1,0]])
kept=[]
for i,j in zip(*np.where(R>5)):
 if R[i,j]==R[max(0,i-1):i+2,max(0,j-1):j+2].max():kept.append((i+1,j+1))
assert kept==[(2,2),(4,4)]
A=np.array([[1,0],[0,1],[1,1]]);b=np.array([2,1,3]);close(np.linalg.lstsq(A,b,rcond=None)[0],[2,1])
assert (int('10110010',2)^int('01001100',2)).bit_count()==7
# Centered low-rank factorization and ambiguity.
rng=np.random.default_rng(532);M=rng.normal(size=(8,3));S=rng.normal(size=(3,10));S-=S.mean(axis=1,keepdims=True);D=M@S
u,s,vt=np.linalg.svd(D,full_matrices=False);Mh=u[:,:3]*np.sqrt(s[:3]);Sh=np.sqrt(s[:3])[:,None]*vt[:3];close(Mh@Sh,D);assert np.linalg.matrix_rank(D)==3
C=np.array([[2,.1,0],[0,1,.2],[0,0,.5]]);close((Mh@C)@np.linalg.solve(C,Sh),D)
Mt=np.array([[2,0,0],[0,1,0],[0,1,0],[0,0,.5],[2,0,0],[0,0,.5]])
metric=np.diag([.25,1,4]);corrected=Mt@np.linalg.cholesky(metric)
for i in range(0,6,2):close(corrected[i:i+2]@corrected[i:i+2].T,np.eye(2))
# Canonical cameras induce the original F up to scale.
def skew(v):x,y,z=v;return np.array([[0,-z,y],[z,0,-x],[-y,x,0]])
e=np.array([2.,-1,1]);F=skew(e)@rng.normal(size=(3,3));close(skew(e)@(-skew(e)@F),(e@e)*F)
# Triangulation recovers a nontrivial finite point.
P=np.c_[np.eye(3),np.zeros(3)];Q=np.c_[np.eye(3),[-.2,0,0]];X=np.array([1.3,.6,4,1]);rows=[]
for camera in [P,Q]:
 x=camera@X;x/=x[2];rows.extend([x[0]*camera[2]-camera[0],x[1]*camera[2]-camera[1]])
_,_,v=np.linalg.svd(rows);xh=v[-1]/v[-1,-1];close(xh,X)
# Full 2-variable GN point update, actual nonlinear objective.
res=lambda x:np.array([800*x[0]/x[1]-260,800*(x[0]-.2)/x[1]-219])
x=np.array([1.3,4.]);J=np.array([[200,-65],[200,-55.]])
eps=1e-6;fd=np.column_stack([(res(x+eps*np.eye(2)[k])-res(x-eps*np.eye(2)[k]))/(2*eps) for k in range(2)]);close(J,fd)
close(J.T@J,[[80000,-24000],[-24000,7250]]);delta=np.linalg.solve(J.T@J,-J.T@res(x));close(delta,[-.0325,-.1]);assert .5*sum(res(x+delta)**2)<.000329
# Projection and left-pose Jacobian finite differences.
q=np.array([1.3,.6,4]);proj=lambda q:np.array([800*q[0]/q[2],750*q[1]/q[2]])
B=np.array([[200,0,-65],[0,187.5,-28.125]])
fd=np.column_stack([(proj(q+eps*np.eye(3)[k])-proj(q-eps*np.eye(3)[k]))/(2*eps) for k in range(3)]);close(B,fd)
pose=B@np.c_[-skew(q),np.eye(3)]
fd=[]
for k in range(6):
 d=eps*np.eye(6)[k];shift=np.cross(d[:3],q)+d[3:];fd.append((proj(q+shift)-proj(q-shift))/(2*eps))
close(pose,np.column_stack(fd))
# Schur elimination equals the full coupled solve.
J=rng.normal(size=(20,9));H=J.T@J+np.eye(9);g=rng.normal(size=9);U,V,W=H[:6,:6],H[:6,6:],H[6:,6:];gc,gp=g[:6],g[6:]
dc=np.linalg.solve(U-V@np.linalg.solve(W,V.T),-gc+V@np.linalg.solve(W,gp));dp=np.linalg.solve(W,-gp-V.T@dc);close(np.r_[dc,dp],np.linalg.solve(H,-g))
# Exactly one interactive and a final TLDR per completed chapter.
for lec,kind in [(5,'corner'),(6,'refinement')]:
 base=Path(f'book/lectures/lecture{lec:02d}');texts=[p.read_text() for p in base.glob('*.md')];assert sum(t.count('{interactive-demo}') for t in texts)==1;assert '{interactive-demo} '+kind in '\n'.join(texts);assert (base/'tldr.md').exists()
print('PASS: L5 tensors/NMS/LK/descriptors; L6 factorization/metric/gauge/triangulation/GN/Jacobians/Schur; one interactive each.')
