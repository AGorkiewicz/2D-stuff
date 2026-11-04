import math
n,m=60,40
Q=[(0,20),(4,13),(9,8),(15,4),(20,0),(0,0),(20,12),(11,20),(17,16)]
A=set()
for q in Q:
    for x in range(m):
        for y in range(m):
            A.add((q[0]+x,q[1]+y))
# depth via BFS in king graph
from collections import deque
INF=10**9
dep={}
dq=deque()
for x in range(-1,n+1):
    for y in range(-1,n+1):
        if (x,y) not in A:
            dep[(x,y)]=0; dq.append((x,y))
while dq:
    u=dq.popleft()
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            v=(u[0]+dx,u[1]+dy)
            if v in A and v not in dep:
                dep[v]=dep[u]+1; dq.append(v)
phi=(2,-1); psi=(1,2); D=5
nphi=math.sqrt(5); npsi=math.sqrt(5)
def st(u):
    k1=u[0]*psi[1]-u[1]*psi[0]
    k2=phi[0]*u[1]-phi[1]*u[0]
    return k1*nphi/D, k2*npsi/D
Ds=[2*2**j for j in range(4)]
J=len(Ds)-1
def cellof(u,j):
    s,t=st(u); return (math.floor(s/Ds[j]), math.floor(t/Ds[j]))
cells=[{} for _ in Ds]
for u in A:
    for j in range(len(Ds)):
        cells[j].setdefault(cellof(u,j),[]).append(u)
# cells may contain points outside A: need all integer points of the cell; compute for points in [-1,n]^2
allpts=[(x,y) for x in range(-2,n+2) for y in range(-2,n+2)]
full=[{} for _ in Ds]
for u in allpts:
    for j in range(len(Ds)):
        full[j].setdefault(cellof(u,j),[]).append(u)
def good(j,c):
    pts=full[j].get(c,[])
    return len(pts)>0 and all(dep.get(u,0)>Ds[j] for u in pts)
sel=[]
for j in range(len(Ds)):
    for c in cells[j]:
        if good(j,c) and (j==J or not good(j+1,(math.floor(c[0]/2),math.floor(c[1]/2)))):
            sel.append((j,c))
covered=set()
for j,c in sel: covered|=set(full[j][c])
res=[u for u in A if u not in covered]
ph=(phi[0]/nphi,phi[1]/nphi); ps=(psi[0]/npsi,psi[1]/npsi)
def corner(s,t): return (s*ph[0]+t*ps[0], s*ph[1]+t*ps[1])
cols=["orange!60","yellow!60","green!30","blue!20"]
sc=0.085
out=[]
out.append(r"\begin{scope}") 
out.append(r"\clip (0,0) rectangle (%.3f,%.3f);"%(n*sc,n*sc))
for j,c in sorted(sel, key=lambda z:-z[0]):
    a,b=c; d=Ds[j]
    pts=[corner(a*d,b*d),corner((a+1)*d,b*d),corner((a+1)*d,(b+1)*d),corner(a*d,(b+1)*d)]
    out.append(r"\filldraw[fill=%s, draw=black!60, line width=0.3pt] "%cols[j] + " -- ".join("(%.3f,%.3f)"%(x*sc+0.5*sc,y*sc+0.5*sc) for x,y in pts)+" -- cycle;")
out.append(r"\end{scope}")

# boundary of A: draw outline cells? draw A outline via unit squares edges
edges=[]
for (x,y) in A:
    for dx,dy,seg in [(1,0,((x+1,y),(x+1,y+1))),(-1,0,((x,y),(x,y+1))),(0,1,((x,y+1),(x+1,y+1))),(0,-1,((x,y),(x+1,y)))]:
        if (x+dx,y+dy) not in A: edges.append(seg)
segs=set(edges)
hor={};ver={}
for (p,q) in segs:
    if p[1]==q[1]: hor.setdefault(p[1],[]).append(min(p[0],q[0]))
    else: ver.setdefault(p[0],[]).append(min(p[1],q[1]))
def runs(xs):
    xs=sorted(xs); r=[]; st=xs[0]; pr=xs[0]
    for x in xs[1:]:
        if x==pr+1: pr=x
        else: r.append((st,pr+1)); st=pr=x
    r.append((st,pr+1)); return r
for y,xs in hor.items():
    for a,b in runs(xs): out.append(r"\draw[black, thick] (%.3f,%.3f) -- (%.3f,%.3f);"%(a*sc,y*sc,b*sc,y*sc))
for x,ys in ver.items():
    for a,b in runs(ys): out.append(r"\draw[black, thick] (%.3f,%.3f) -- (%.3f,%.3f);"%(x*sc,a*sc,x*sc,b*sc))
print("\n".join(out))
import sys
print("% sel per level", [sum(1 for j,c in sel if j==jj) for jj in range(len(Ds))], "res", len(res), file=sys.stderr)
