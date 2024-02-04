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

random.seed(4)
#random.seed(10)

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

for (x, y) in Q:
    assert x < n - m and y < n - m
    for u in P:
        S[x + u.x][y + u.y] = 1


fill_rect((z, z), (R, R), 'lightgray, opacity=0.7')

P = [Point(z, z)]
for (i, j) in Q:
    P.append(Point(P[-1].x, j + m - 0.5))
    P.append(Point(i + m - 0.5, j + m - 0.5))

P += [Point(P[-1].x, z)]
draw_poly(P, 'rounded corners=10, fill=white, white')

fill_rect((z, z), (z + 1, Q[0][1] + m - 0.5), 'fill=white')
fill_rect((z, z), (Q[-1][0] + m - 0.5, z + 1), 'fill=white')

draw_dots(n // 2, n - 1)

for a in range(n):
    for b in range(n):
        if a < z or b < z: continue
        if S[a - 1][b] == 0 and S[a][b - 1] == 0: continue
        if S[a][b] == 1: continue
        for i in range(n):
            for j in range(n):
                if i < z or j < z: continue
                if S[i][j] == 0: continue
                dis = (i - a)**2 + (j - b)**2
                D[i][j] = min(D[i][j], dis)


for i in range(n):
    for j in range(n):
        if i < z or j < z: continue
        if S[i][j] == 0: continue
        if D[i][j] <= d * d:
            if random.randint(0, 2) == 0:
                dom.append((i, j))

for (i, j) in dom:
    res += f'\\draw[fill=red, red] ({i}, {j}) circle (4pt);'


U = [[] for i in range(0, n // d + 1)]

for (i, j) in dom:
    U[i // d].append((i, j))

for i in range(1, len(U)):
    if len(U[i - 1]) > 0 and len(U[i]) > 0:
        res += f'\\draw ({i * d - 0.5}, {z}) -- ({i * d - 0.5}, {R});'


for (i, j) in U[10]:
    res += f'\\draw[fill=green, green] ({i}, {j}) circle (4pt);'


max_y = 0

for (i, j) in U[10]:
    for k in range(j, n):
        if S[i][k] == 0:
            if k > max_y:
                max_y = k
            break

min_y = min([j for (i, j) in U[10]])

ax = 10 * d
bx = 11 * d - 1

h = max_y - min_y

#res += f'\\draw ({ax - 0.5}, {max_y - 0.5}) -- ({bx - 0.5}, {max_y - 0.5});'
res += f'\\draw [dashed] ({ax - 0.5}, {min_y - 0.5}) -- ({bx + 0.5}, {min_y - 0.5});'

res += f'\\draw ({(ax + bx) / 2}, {82}) node [scale=10]{{$V_i$}};'

res += f'\\draw[decorate, decoration={{brace, amplitude=80pt, raise=2ex, mirror}}] ({ax}, {max_y}) -- ({ax}, {min_y}) node [midway, scale=10, xshift=-1.4em]{{$h_i$}};'

res += f'\\draw[decorate, decoration={{brace, amplitude=50pt, raise=2ex, mirror}}] ({10 * d}, {60}) -- ({11 * d - 1}, {60}) node [midway, scale=10, yshift=-1em]{{$d - 1$}};'

res += '\\end{tikzpicture}\n\\end{document}'

print(res)

