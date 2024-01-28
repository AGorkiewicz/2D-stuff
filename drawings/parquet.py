import math
import random
from dataclasses import dataclass

res = '\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n\\begin{tikzpicture}'

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


def draw_dots(ax, bx, ay, by):
    global res
    res += f'\\foreach \\x in {{{ax},...,{bx}}} \\foreach \\y in {{{ay},...,{by}}} \\draw (\\x, \\y) circle (0.1pt);'


h0 = -123
h1 = 156
s0 = -111
s1 = 144

x0 = -20.5
x1 = 18.5
y0 = -10.5
y1 = 14.5

#parquet = [
#    xy(h0, s0),
#    xy(h0, s1),
#    xy(h1, s1),
#    xy(h1, s0),
#]


parquet = [
    Point(x0, y_hx(h0, x0)),
    Point(x_hy(h0, y0), y0),
    Point(x_sy(s0, y0), y0),
    Point(x1, y_sx(s0, x1)),
    Point(x1, y_hx(h1, x1)),
    Point(x_hy(h1, y1), y1),
    Point(x_sy(s1, y1), y1),
    Point(x0, y_sx(s1, x0)),
]

ax = math.floor(min_x(parquet)) - 1
bx = math.ceil(max_x(parquet)) + 1
ay = math.floor(min_y(parquet)) - 1
by = math.ceil(max_y(parquet)) + 1



vis = []

def dfs(x, y):
    if x < ax or x > bx: return
    if y < ay or y > by: return
    if (x, y) in vis: return
    vis.append((x, y))
    dfs(x + phi_x, y + phi_y)
    dfs(x - phi_x, y - phi_y)
    dfs(x + psi_x, y + psi_y)
    dfs(x - psi_x, y - psi_y)

sx = -6
sy = -2
dfs(sx, sy)

res += f'\\draw [white, fill=white] ({ax - 0.5}, {ay - 0.5}) rectangle ({bx + 0.5}, {by + 0.5});'

res += f'\\draw [-{{Stealth[length=20pt]}}] ({sx}, {sy}) -- node [below left, scale = 3] {{$\\varphi$}} ++({phi_x}, {phi_y});'
res += f'\\draw [-{{Stealth[length=20pt]}}] ({sx}, {sy}) -- node [above left, scale = 3] {{$\\psi$}} ++({psi_x}, {psi_y});'

def inside(p):
    if p.x < x0 or p.x > x1: return False
    if p.y < y0 or p.y > y1: return False
    if p.h < h0 or p.h > h1: return False
    if p.s < s0 or p.s > s1: return False
    return True


for x in range(ax, bx + 1):
    for y in range(ay, by + 1):
        if inside(Point(x, y)):
            res += f'\\draw[fill=black] ({x},{y}) circle (1.5pt);'
        else:
            res += f'\\draw[fill=black] ({x},{y}) circle (0.5pt);'

for (x, y) in vis:
    if inside(Point(x, y)):
        res += f'\\draw[red, fill=red] ({x},{y}) circle (4pt);'
    #else:
     #   res += f'\\draw[red, fill=red] ({x},{y}) circle (0.5pt);'

draw_poly(parquet)



res += '\\end{tikzpicture}\n\\end{document}'
print(res)

