import math
import random
from dataclasses import dataclass

res = '\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n\\begin{tikzpicture}'
res += '\\usetikzlibrary{decorations.pathreplacing}'
res += '\\usetikzlibrary{decorations.pathmorphing}'
res += '\\usetikzlibrary{arrows.meta}'


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

random.seed(1)

@dataclass
class Point:
    x: float
    y: float
    def __add__(self, a):   return Point(self.x + a.x, self.y + a.y)
    @property
    def h(self):    return phi_x * self.y - phi_y * self.x
    @property
    def s(self):    return psi_x * self.y - psi_y * self.x


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


def fill_rect(u, v, settings = ''):
    global res
    res += f'\\fill [{settings}] ({min(u[0], v[0])}, {min(u[1], v[1])}) rectangle ({max(u[0], v[0])}, {max(u[1], v[1])});'


def draw_dots(s):
    global res
    res += f'\\foreach \\x in {{0,...,{s - 1}}} \\foreach \\y in {{0,...,{s - 1}}} \\draw[opacity=0.8] (\\x, \\y) circle (0.5pt);'


fill_rect((L, L), (R, R), 'lightgray, opacity=0.7')


def draw_occurrence(qx, qy, settings):
    global res
    res += f'\\draw [{settings}] ({qx - 0.5}, {qy - 0.5}) rectangle ({qx + m - 0.5}, {qy + m - 0.5});'


ax = 2
ay = 19
bx = 6
by = 1

Q = [
    (ax, ay),
    (bx, by),
    (ax + phi_x, ay + phi_y),
    (bx + psi_x, by + psi_y),
    (1, 11),
    (19, 8),
]

colors = [
    'red',
    'blue',
    'green',
    'teal',
    'cyan',
    'orange',
]

for (i, j) in Q: draw_occurrence(i, j, 'rounded corners=10, white, fill=white')

for i in range(len(Q)): draw_occurrence(Q[i][0], Q[i][1], f'rounded corners=10, opacity=0.5, {colors[i]}')

draw_dots(n)

for (i, j) in Q:
    res += f'\\draw[fill=red, red] ({i}, {j}) circle (5pt);'

#for j in range(len(Q)):
#    for i in range(j):
#        dis = (Q[i][0] - Q[j][0])**2 + (Q[i][1] - Q[j][1])**2
#        if dis > 120: continue
#        res += f'\\draw [dotted] ({Q[i][0]}, {Q[i][1]}) -- node [scale = 2] {{{dis}}} ({Q[j][0]}, {Q[j][1]});'

res += f'\\draw [-{{Stealth[length=20pt]}}] ({ax}, {ay}) -- node [below left, scale = 5] {{$\\varphi$}} ++({phi_x}, {phi_y});'
res += f'\\draw [-{{Stealth[length=20pt]}}] ({bx}, {by}) -- node [above left, scale = 5] {{$\\psi$}} ++({psi_x}, {psi_y});'

res += '\\end{tikzpicture}\n\\end{document}'

print(res)

