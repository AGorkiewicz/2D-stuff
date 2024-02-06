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
D = [[1e9 for i in range(n)] for j in range(n)]

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


for i in range(10):
    x = random.randint(1, n - m - 1)
    y = random.randint(1, n - m - 1)
    Q.append((x, y))
    for u in P:
        S[x + u.x][y + u.y] = 1


fill_rect((L, L), (R, R), 'lightgray, opacity=0.7')

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

draw_poly(P, 'rounded corners=10, fill=white, white')

dom = []

for a in range(n):
    for b in range(n):
        if S[a][b] == 1: continue
        ok = False
        ok |= a > 0 and S[a - 1][b] == 1
        ok |= b > 0 and S[a][b - 1] == 1
        ok |= a < n - 1 and S[a + 1][b] == 1
        ok |= b < n - 1 and S[a][b + 1] == 1
        if ok == False: continue
        for i in range(n):
            for j in range(n):
                if S[i][j] == 0: continue
                dis = (i - a)**2 + (j - b)**2
                D[i][j] = min(D[i][j], dis)

d = 7

for i in range(n):
    for j in range(n):
        if S[i][j] == 0: continue
        if D[i][j] <= d * d:
            if random.randint(0, 2) == 0:
                dom.append((i, j))


draw_dots(n)


for (i, j) in dom:
    res += f'\\draw[fill=red, red] ({i}, {j}) circle (4pt);'


c = 13

res += f'\\draw ({z + c}, {z + c}) node [scale=10]{{$S_1$}};'
res += f'\\draw ({z - c}, {z + c}) node [scale=10]{{$S_2$}};'
res += f'\\draw ({z - c}, {z - c}) node [scale=10]{{$S_3$}};'
res += f'\\draw ({z + c}, {z - c}) node [scale=10]{{$S_4$}};'

res += f'\\draw [] ({z}, {L}) -- ({z}, {R});'
res += f'\\draw [] ({L}, {z}) -- ({R}, {z});'


res += '\\end{tikzpicture}\n\\end{document}'
print(res)

