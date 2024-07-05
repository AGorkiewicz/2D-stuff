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
m = 20
n = 3 * m // 2
assert n % 2 == 0

D = 11
U = 11
L = 13
R = 13

L = -L
D = -D
U = n - 1 + U
R = n - 1 + R

l = 10

@dataclass
class Point:
    x: float
    y: float
    def __add__(self, a):   return Point(self.x + a.x, self.y + a.y)
    @property
    def h(self):    return phi_x * self.y - phi_y * self.x
    @property
    def s(self):    return psi_x * self.y - psi_y * self.x
    def rotate(self):   return Point(-self.y, self.x)
    def __mul__(self, a): return Point(self.x * a, self.y * a)
    def len2(self): return self.x * self.x + self.y * self.y
    def len(self): return sqrt(self.len2())

phi = Point(phi_x, phi_y)
psi = Point(psi_x, psi_y)

T = [Point(i, j) for i in range(n) for j in range(n)]

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

def draw_line(a, b, settings = 'black'):
    global res
    a = (a.x, a.y) if type(a) == Point else a
    b = (b.x, b.y) if type(b) == Point else b
    res += f'\\draw[{settings}] ({a[0]}, {a[1]}) -- ({b[0]}, {b[1]});'

def fill_rect(u, v, settings = ''):
    global res
    res += f'\\fill [{settings}] ({min(u[0], v[0])}, {min(u[1], v[1])}) rectangle ({max(u[0], v[0])}, {max(u[1], v[1])});'

def draw_dots(s):
    global res
    res += f'\\foreach \\x in {{0,...,{s - 1}}} \\foreach \\y in {{0,...,{s - 1}}} \\draw[gray, fill=gray, opacity=0.75] (\\x, \\y) circle (1.5pt);'

draw_dots(n)

h_min = min([u.h for u in T])
h_max = max([u.h for u in T])
s_min = min([u.s for u in T])
s_max = max([u.s for u in T])

h_delta = (h_max - h_min) / l
s_delta = (s_max - s_min) / l

h_min -= h_delta / 8
h_max += h_delta / 8
s_min -= s_delta / 8
s_max += s_delta / 8

h_delta = (h_max - h_min) / l
s_delta = (s_max - s_min) / l

H = [h_min + i * h_delta for i in range(l + 1)]
S = [s_min + i * s_delta for i in range(l + 1)]

ss_min = s_min - 0.70 * s_delta
ss_max = s_max + 0.70 * s_delta
for i, h in enumerate(H):
    a = (x_hy(h, D), D) if x_hy(h, D) <= R else (R, y_hx(h, R))
    b = (x_hy(h, U), U) if x_hy(h, U) >= L else (L, y_hx(h, L))
    if Point(b[0], b[1]).s > ss_max: b = xy(h, ss_max)
    if Point(a[0], a[1]).s < ss_min: a = xy(h, ss_min)
    draw_line(a, b, 'opacity=0.8')


hh_min = h_min - 0.70 * h_delta
hh_max = h_max + 0.70 * h_delta
for i, s in enumerate(S):
    a = (x_sy(s, D), D) if x_sy(s, D) >= L else (L, y_sx(s, L))
    b = (x_sy(s, U), U) if x_sy(s, U) <= R else (R, y_sx(s, R))
    if Point(b[0], b[1]).h > hh_max: b = xy(hh_max, s)
    if Point(a[0], a[1]).h < hh_min: a = xy(hh_min, s)
    draw_line(a, b, 'opacity=0.8')

hp = [xy(H[i], s_min - s_delta) for i in range(l + 1)]
sp = [xy(h_min - h_delta, S[i]) for i in range(l + 1)]

hb1 = xy(H[1], s_min - 1.8 * s_delta)
hb2 = hb1 + phi.rotate() * (h_delta / phi.len2())
sb4 = xy(h_min - 1.95 * h_delta, S[4])
sb5 = sb4 + psi.rotate() * (s_delta / psi.len2())
draw_line(hb1, hp[1], 'loosely dashed, opacity=0.8')
draw_line(hb2, hp[2], 'loosely dashed, opacity=0.8')
draw_line(sb4, sp[4], 'loosely dashed, opacity=0.8')
draw_line(sb5, sp[5], 'loosely dashed, opacity=0.8')
res += f'\draw[decorate, decoration={{brace, amplitude=20pt, raise=5, mirror}}] ({hb1.x}, {hb1.y}) -- ({hb2.x}, {hb2.y}) node [midway, xshift=85, yshift=-15, scale=3.5]{{$\\mathcal{{O}}(n / \\ell)$}};'
res += f'\draw[decorate, decoration={{brace, amplitude=20pt, raise=5, mirror}}] ({sb5.x}, {sb5.y}) -- ({sb4.x}, {sb4.y}) node [midway, xshift=-50, yshift=-50, scale=3.5]{{$\\mathcal{{O}}(n / \\ell)$}};'

for i, p in enumerate(hp[ : 6]):
    res += f'\\node (hp{i}) at ({p.x}, {p.y}) [circle, fill=white, scale=3.5] {{$h_{{{i}}}$}};'
    
for i, p in enumerate(sp[ : 7]):
    res += f'\\node (sp{i}) at ({p.x}, {p.y}) [circle, fill=white, scale=3.5] {{$v_{{{i}}}$}};'

hp = [xy(H[i], s_max + s_delta) for i in range(l + 1)]
sp = [xy(h_max + h_delta, S[i]) for i in range(l + 1)]

hp.reverse()
sp.reverse()

for i, p in enumerate(hp[ : 3]):
    if i == 0:
        res += f'\\node (hp{i}) at ({p.x}, {p.y}) [circle, fill=white, scale=3.5] {{$h_{{\\ell}}$}};'
    else:
        res += f'\\node (hp{i}) at ({p.x}, {p.y}) [circle, fill=white, scale=3.5] {{$h_{{\\ell - {i}}}$}};'

for i, p in enumerate(sp[ : 3]):
    if i == 0:
        res += f'\\node (sp{i}) at ({p.x}, {p.y}) [circle, fill=white, scale=3.5] {{$v_{{\\ell}}$}};'
    else:
        res += f'\\node (sp{i}) at ({p.x}, {p.y}) [circle, fill=white, scale=3.5] {{$v_{{\\ell - {i}}}$}};'

w = [[xy(H[i] + h_delta / 2, S[j] + s_delta / 2) for j in range(l + 1)] for i in range(l + 1)]

P_coords = [
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 0),
    (1, 1),
    (1, 2),
    (2, 0),
    (3, 0),
]

for (i, j) in P_coords:
    res += f'\\node at ({w[i][j].x}, {w[i][j].y}) [scale=3.5] {{$p_{{{i},{j}}}$}};'

S_coords = [
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 1),
]

for (i, j) in S_coords:
    res += f'\\node at ({w[l - i][l - j].x}, {w[l - i][l - j].y}) [scale=3.5] {{$p_{{\\ell - {i}, \\ell - {j}}}$}};'

res += '\\end{tikzpicture}\n\\end{document}'
print(res)

