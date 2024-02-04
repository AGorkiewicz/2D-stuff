import math
import random
from dataclasses import dataclass

res = '\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n\\begin{tikzpicture}'
res += '\\usetikzlibrary{decorations.pathreplacing}'
res += '\\usetikzlibrary{decorations.pathmorphing}'
 

m = 80
n = 3 * m // 2
assert n % 2 == 0
L = -0.5
R = n - 0.5
z = (n - 1) / 2
d = 9

random.seed(1)

@dataclass
class Point:
    x: float
    y: float
    def __add__(self, a):   return Point(self.x + a.x, self.y + a.y)


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


def draw_dots(s, t):
    global res
    res += f'\\foreach \\x in {{{s},...,{t}}} \\foreach \\y in {{{s},...,{t}}} \\draw [fill=black](\\x, \\y) circle (0.5pt);'


S = [[0 for i in range(n)] for j in range(n)]
P = [Point(i, j) for i in range(m) for j in range(m)]
Q = []
D = [[1e9 for i in range(n)] for j in range(n)]
dom = []


Q = [
    (0,  37),
    (3, 34),
    (11, 30),
    (15, 27),
    (18, 20),
    (25, 15),
    (27, 3),
    (39, 1),
]

draw_dots(0, m - 1)

res += f'\\draw (-0.5, -0.5) rectangle ({m - 0.5}, {m - 0.5});'
res += f'\\draw[-, decorate, decoration={{snake, segment length=80pt, amplitude=4pt}}] ({m - 0.5}, {m - 0.5}) -- ({m - d - 0.5}, {m - d - 0.5});'
res += f'\\draw (-0.5, -0.5) rectangle ({m - d - 0.5}, {m - d - 0.5}) node [pos=.5, scale=50]{{$P_0$}};'
res += f'\\node [scale=20] at ({(m - 1) / 2}, {m - (d + 1) / 2}) {{$P_3$}};'
res += f'\\node [scale=20] at ({m - (d + 1) / 2}, {62}) {{$H_i$}};'
res += f'\\node [scale=20] at ({m - (d + 1) / 2}, {25}) {{$L_i$}};'

h = 31
res += f'\\draw ({m - d - 0.5}, {m - h - 0.5}) -- ({m - 0.5}, {m - h - 0.5});'

res += f'\\draw[decorate, decoration={{brace, amplitude=50pt, raise=4ex, mirror}}] ({m - 1}, {m - h}) -- ({m - 1}, {m - 1}) node [midway, scale=10, xshift=2.1em]{{$h_i - 1$}};'

res += f'\\draw[decorate, decoration={{brace, amplitude=50pt, raise=4ex, mirror}}] ({0}, {m - 1}) -- ({0}, {m - d}) node [midway, scale=10, xshift=-2.0em]{{$d - 1$}};'
res += f'\\draw[decorate, decoration={{brace, amplitude=50pt, raise=4ex, mirror}}] ({m - d}, {0}) -- ({m - 1}, {0}) node [midway, scale=10, yshift=-1.2em]{{$d - 1$}};'

res += f'\\draw[decorate, decoration={{brace, amplitude=50pt, raise=4ex, mirror}}] ({0}, {m - d}) -- ({0}, {0}) node [midway, scale=10, xshift=-2.1em]{{$m - d$}};'
res += f'\\draw[decorate, decoration={{brace, amplitude=50pt, raise=4ex, mirror}}] ({0}, {0}) -- ({m - d}, {0}) node [midway, scale=10, yshift=-1.2em]{{$m - d$}};'
res += f'\\draw[decorate, decoration={{brace, amplitude=50pt, raise=4ex, mirror}}] ({m - 1}, {0}) -- ({m - 1}, {m - h}) node [midway, scale=10, xshift=2.3em]{{$m - h_i$}};'

res += '\\end{tikzpicture}\n\\end{document}'

print(res)

