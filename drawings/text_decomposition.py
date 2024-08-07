import math
import random
from dataclasses import dataclass

res = '\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n\\begin{tikzpicture}'
res += '\\usetikzlibrary{decorations.pathreplacing}'
res += '\\usetikzlibrary{decorations.pathmorphing}'

phi_x = 10
phi_y = -3
psi_x = 5
psi_y = 6
m = 40
n = 3 * m // 2
assert n % 2 == 0
L = -0.5
R = n - 0.5
z = (n - 1) / 2

random.seed(8)

@dataclass
class Point:
    x: float
    y: float
    def __add__(self, a):   return Point(self.x + a.x, self.y + a.y)
    @property
    def h(self):    return phi_x * self.y - phi_y * self.x
    @property
    def s(self):    return psi_x * self.y - psi_y * self.x


S = [[0 for i in range(n)] for j in range(n)]
T = [Point(i, j) for i in range(n) for j in range(n)]
P = [Point(i, j) for i in range(m) for j in range(m)]
Q = []

def dot(u, v):      return u.x * v.x + u.y * v.y
def cross(u, v):    return u.x * v.y - u.y * v.x

def x_hs(h, s): return (h * psi_x - s * phi_x) / (phi_x * psi_y - phi_y * psi_x)
def y_hs(h, s): return (h * psi_y - s * phi_y) / (phi_x * psi_y - phi_y * psi_x)

def xy(h, s): return Point(x_hs(h, s), y_hs(h, s))

def x_hy(h, y): return (phi_x * y - h) / phi_y
def y_hx(h, x): return (phi_y * x + h) / phi_x
def x_sy(h, y): return (psi_x * y - h) / psi_y
def y_sx(h, x): return (psi_y * x + h) / psi_x

def min_x(points): return min(p.x for p in points)
def max_x(points): return max(p.x for p in points)
def min_y(points): return min(p.y for p in points)
def max_y(points): return max(p.y for p in points)

def draw_poly(vertices, settings = 'black'):
    global res
    vertices = [(v.x, v.y) if type(v) == Point else v for v in vertices]
    vertices = [f'{(v[0], v[1])}' for v in vertices] + ['cycle;'];
    vertices = ' -- '.join(vertices)
    vertices = f'\\draw[{settings}] ' + vertices
    res += vertices + '\n'

def draw_rect(u, v, settings = ''):
    global res
    res += f'\\draw [{settings}] ({min(u[0], v[0])}, {min(u[1], v[1])}) rectangle ({max(u[0], v[0])}, {max(u[1], v[1])});'

def draw_dots(s):
    global res
    res += f'\\foreach \\x in {{0,...,{s - 1}}} \\foreach \\y in {{0,...,{s - 1}}} \\draw[opacity=0.9] (\\x, \\y) circle (0.6pt);'

for i in range(10):
    x = random.randint(1, n - m - 1)
    y = random.randint(1, n - m - 1)
    Q.append((x, y))
    for u in P:
        S[x + u.x][y + u.y] = 1

space = 0
res +=  f'\\clip ({L - space}, {L - space}) rectangle ({R + space},{R + space});'

draw_rect((L, L), (R, R), 'rounded corners=10, lightgray, fill=lightgray, opacity=0.7')

PA = []
PB = []
PC = []
PD = []

for i in reversed(range(n - 1)):
    for j in range(n - 1):
        a, b, c, d = S[i][j], S[i + 1][j], S[i][j + 1], S[i + 1][j + 1]
        if a == 0 and b == 1 and c == 1 and d == 1: PA.append((i, j))
        if a == 0 and b == 0 and c == 0 and d == 1: PA.append((i, j))
        if a == 1 and b == 1 and c == 1 and d == 0: PD.append((i, j))
        if a == 1 and b == 0 and c == 0 and d == 0: PD.append((i, j))

for i in range(n - 1):
    for j in range(n - 1):
        a, b, c, d = S[i][j], S[i + 1][j], S[i][j + 1], S[i + 1][j + 1]
        if a == 1 and b == 0 and c == 1 and d == 1: PB.append((i, j))
        if a == 0 and b == 0 and c == 1 and d == 0: PB.append((i, j))
        if a == 1 and b == 1 and c == 0 and d == 1: PC.append((i, j))
        if a == 0 and b == 1 and c == 0 and d == 0: PC.append((i, j))

P = PA[::-1] + PB + PD + PC[::-1]
P = [Point(i + 0.5, j + 0.5) for (i, j) in P]

draw_poly(P, 'rounded corners=10, lightgray, fill=white')

l = 40

h_min = Point(L, L).h
h_max = Point(R, R).h
s_min = Point(R, L).s
s_max = Point(L, R).s

#h_min = min([u.h for u in T])
#h_max = max([u.h for u in T])
#s_min = min([u.s for u in T])
#s_max = max([u.s for u in T])
h_delta = (h_max - h_min) / l
s_delta = (s_max - s_min) / l

h = [h_min + i * h_delta for i in range(l + 1)]
s = [s_min + i * s_delta for i in range(l + 1)]

def coverable(points):
    ax = math.ceil(min_x(points))
    ay = math.ceil(min_y(points))
    bx = math.floor(max_x(points))
    by = math.floor(max_y(points))
    assert ax <= bx
    assert ay <= by
    if ax < 0 or bx >= n: return False
    if ay < 0 or by >= n: return False
    for x in range(ax, bx + 1):
        for y in range(ay, by + 1):
            if S[x][y] == 0:
                return False
    return True

def inside_text(points):
    #ax = math.ceil(min_x(points))
    #ay = math.ceil(min_y(points))
    #bx = math.floor(max_x(points))
    #by = math.floor(max_y(points))
    #assert ax <= bx
    #assert ay <= by
    #if 0 <= ax <= n     
    #return False
    for point in points:
        if 0 <= point.x < n and 0 <= point.y < n:
            return True
    return False

w = [[xy(h[i], s[j]) for j in range(l + 1)] for i in range(l + 1)]
P = [[[w[i][j], w[i][j + 1], w[i + 1][j + 1], w[i + 1][j]] for j in range(l)] for i in range(l)]

C = []
I = []
I_periph = []
K1 = []
K1_periph = []
K2 = []
K2_periph = []
K3 = []
K3_periph = []
K4 = []
K4_periph = []

for i in range(l):
    for j in range(l):
        if coverable(P[i][j]):
            C.append((i, j))


for i in range(l):
    for j in range(l):
        ax = min_x(P[i][j])
        bx = max_x(P[i][j])
        ay = min_y(P[i][j])
        by = max_y(P[i][j])
        if (i, j) not in C:
            if inside_text(P[i][j]):
                if ax > z and ay > z: K1_periph.append((i, j))
                if bx < z and ay > z: K2_periph.append((i, j))
                if bx < z and by < z: K3_periph.append((i, j))
                if ax > z and by < z: K4_periph.append((i, j))
                if ax <= z and bx >= z or ay <= z and by >= z: I_periph.append((i, j))
        else: 
            if ax > z and ay > z: K1.append((i, j))
            if bx < z and ay > z: K2.append((i, j))
            if bx < z and by < z: K3.append((i, j))
            if ax > z and by < z: K4.append((i, j))
            if ax <= z and bx >= z or ay <= z and by >= z: I.append((i, j))

res += '\\tikzset{internal border/.style = {postaction = {clip, postaction = {draw = #1, solid, line width = 10pt, opacity=0.7},postaction = {draw}}}}'

# I
for (i, j) in I:
    draw_poly(P[i][j], 'very thick, internal border=teal, fill=teal, fill opacity=0.2')


# K1 and K3
for j in range(l):
    for t in [[i for (i, k) in K1 if k == j], [i for (i, jj) in K3 if jj == j]]: 
        if len(t) > 0:
            a, b = min(t), max(t) + 1
            draw_poly([w[a][j], w[a][j + 1], w[b][j + 1], w[b][j]], 'very thick, internal border=cyan, fill=cyan, fill opacity=0.2')


#K2 and K4
for i in range(l):
    for t in [[j for (k, j) in K2 if k == i], [j for (k, j) in K4 if k == i]]: 
        if len(t) > 0:
            a, b = min(t), max(t) + 1
            draw_poly([w[i][a], w[i][b], w[i + 1][b], w[i + 1][a]], 'very thick, internal border=cyan, fill=cyan, fill opacity=0.2')


#for (i, j) in I_periph:
#    draw_poly(P[i][j], 'very thick, internal border=red, fill=red, fill opacity=0.2')
#for j in range(l):
#    for t in [[i for (i, k) in K1_periph if k == j], [i for (i, jj) in K3_periph if jj == j]]: 
#        if len(t) > 0:
#            a, b = min(t), max(t) + 1
#            draw_poly([w[a][j], w[a][j + 1], w[b][j + 1], w[b][j]], 'very thick, internal border=red, fill=red, fill opacity=0.2')
#for i in range(l):
#    for t in [[j for (k, j) in K2_periph if k == i], [j for (k, j) in K4_periph if k == i]]: 
#        if len(t) > 0:
#            a, b = min(t), max(t) + 1
#            draw_poly([w[i][a], w[i][b], w[i + 1][b], w[i + 1][a]], 'very thick, internal border=red, fill=red, fill opacity=0.2')


for h in h:
    #a = (x_hy(h, L), L) if x_hy(h, L) <= R else (R, y_hx(h, R))
    #b = (x_hy(h, R), R) if x_hy(h, R) >= L else (L, y_hx(h, L))
    a = xy(h, s_min)
    b = xy(h, s_max)
    draw_poly([a, b], 'opacity=0.2')

for s in s:
    #a = (x_sy(s, L), L) if x_sy(s, L) >= L else (L, y_sx(s, L))
    #b = (x_sy(s, R), R) if x_sy(s, R) <= R else (R, y_sx(s, R))
    a = xy(h_min, s)
    b = xy(h_max, s)
    draw_poly([a, b], 'opacity=0.2')

draw_dots(n)

res += '\\end{tikzpicture}\n\\end{document}'
print(res)

