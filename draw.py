import math
import random

res = '\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n\\begin{tikzpicture}'


phi = (10, 3)
psi = (-2, 3)
n = 80
n2 = 3 * n // 2
L = -0.5
R = n2 - 0.5
mid = (n2 - 1) / 2

random.seed(4)

S = [[0 for i in range(n2)] for j in range(n2)]
T = [(i, j) for i in range(n2) for j in range(n2)]
P = [(i, j) for i in range(n) for j in range(n)]
Q = []


def dot(u, v): return u[0] * v[0] + u[1] * v[1]

def u_xy(x, y): return dot((x, y), phi)
def v_xy(x, y): return dot((x, y), psi)
def x_uv(u, v): return (u * psi[1] - v * phi[1]) / (phi[0] * psi[1] - psi[0] * phi[1])
def y_uv(u, v): return (u * psi[0] - v * phi[0]) / (phi[1] * psi[0] - psi[1] * phi[0])
def x_uy(u, y): return (u - y * phi[1]) / phi[0]
def x_vy(v, y): return (v - y * psi[1]) / psi[0]
def y_xu(x, v): return (v - x * phi[0]) / phi[1]
def y_xv(x, v): return (v - x * psi[0]) / psi[1]

def xy(u, v): return (x_uv(u, v), y_uv(u, v))
def uv(x, y): return (u_xy(x, y), v_xy(x, y))

def min_x(points): return min(p[0] for p in points)
def max_x(points): return max(p[0] for p in points)
def min_y(points): return min(p[1] for p in points)
def max_y(points): return max(p[1] for p in points)


def draw_poly(vertices, settings = 'black'):
    global res
    vertices = [f'{(v[0], v[1])}' for v in vertices] + ['cycle;'];
    vertices = ' -- '.join(vertices)
    vertices = f'\\draw[{settings}] ' + vertices
    res += vertices + '\n'


def fill_rect(u, v, settings = ''):
    global res
    res += f'\\fill [{settings}] ({min(u[0], v[0])}, {min(u[1], v[1])}) rectangle ({max(u[0], v[0])}, {max(u[1], v[1])});'


def draw_dots(s):
    global res
    res += f'\\draw[line width=4pt, line cap=round, dash pattern=on 0pt off 1cm] (0.0, 0.0) grid ({s - 1}, {s - 1});'


def draw_grid(a, b, settings = ''):
    global res
    res += f'\\draw[{settings}] (0, 0) grid ({a}, {b});'


for i in range(25):
    x = random.randint(1, n2 - n - 1)
    y = random.randint(1, n2 - n - 1)
    Q.append((x, y))
    for dx, dy in P:
        S[x + dx][y + dy] = 1


fill_rect((L, L), (R, R), 'lightgray')


for i in range(n2):
    for j in range(n2):
        if S[i][j] == 0: continue
        cnt = 0
        if i == 0 or S[i - 1][j] == 0: cnt += 1
        if j == 0 or S[i][j - 1] == 0: cnt += 1
        if i == n2 - 1 or S[i + 1][j] == 0: cnt += 1
        if j == n2 - 1 or S[i][j + 1] == 0: cnt += 1
        assert cnt <= 2
        if cnt < 2: continue
        r = 0.5
        if i < n and j < n:     fill_rect((i - r, j - r), (mid, mid), 'white')
        if i < n and j >= n:    fill_rect((i - r, j + r), (mid, mid), 'white')
        if i >= n and j < n:    fill_rect((i + r, j - r), (mid, mid), 'white')
        if i >= n and j >= n:   fill_rect((i + r, j + r), (mid, mid), 'white')


l = 40
u_min = min([u_xy(x, y) for (x, y) in T])
u_max = max([u_xy(x, y) for (x, y) in T])
v_min = min([v_xy(x, y) for (x, y) in T])
v_max = max([v_xy(x, y) for (x, y) in T])
u_delta = (u_max - u_min) / l
v_delta = (v_max - v_min) / l

U = [u_min + i * u_delta for i in range(l + 1)]
V = [v_min + i * v_delta for i in range(l + 1)]

P = [[[] for i in range(l)] for j in range(l)]
A = [[[] for i in range(l)] for j in range(l)]

for (x, y) in T:
    u, v = uv(x, y)
    for i in range(l):
        if U[i] < u and u <= U[i + 1]:
            for j in range(l):
                if V[j] < v and v <= V[j + 1]:
                    if S[x][y] == 1:
                        A[i][j].append((x, y))
                    P[i][j].append((x, y))                


def active(p):
    ax = min_x(p)
    bx = max_x(p)
    ay = min_y(p)
    by = max_y(p)
    for (x, y) in T:
        if x >= ax and x <= bx and y >= ay and y <= by and S[x][y] == 0:
            return False
    return True


B = [[False for i in range(l)] for j in range(l)]
for i in range(l):
    for j in range(l):
        if len(A[i][j]) == 0 or active(P[i][j]) == False:
            B[i][j] = True


def G1(i, j): return min_y(P[i][j]) > mid and max_x(P[i][j]) >= mid
def G2(i, j): return max_x(P[i][j]) < mid and max_y(P[i][j]) >= mid
def G3(i, j): return max_y(P[i][j]) < mid and min_x(P[i][j]) <= mid
def G4(i, j): return min_x(P[i][j]) > mid and min_y(P[i][j]) <= mid


for i in range(l):
    u1, u2 = U[i], U[i + 1]
    j1, j2 = None, None
    for j in range(l):
        if B[i][j] == True: continue
        if G2(i, j) == False: continue
        if j1 is None or j1 > j: j1 = j
        if j2 is None or j2 < j: j2 = j
    if j1 is None and j2 is None: continue
    v1, v2 = V[j1], V[j2 + 1]
    p = [xy(u1, v1), xy(u1, v2), xy(u2, v2), xy(u2, v1)]
    draw_poly(p, 'fill=teal, opacity=0.5')


for i in range(l):
    u1, u2 = U[i], U[i + 1]
    j1, j2 = None, None
    for j in range(l):
        if B[i][j] == True: continue
        if G4(i, j) == False: continue
        if j1 is None or j1 > j: j1 = j
        if j2 is None or j2 < j: j2 = j
    if j1 is None and j2 is None: continue
    v1, v2 = V[j1], V[j2 + 1]
    p = [xy(u1, v1), xy(u1, v2), xy(u2, v2), xy(u2, v1)]
    draw_poly(p, 'fill=teal, opacity=0.5')


for j in range(l):
    v1, v2 = V[j], V[j + 1]
    i1, i2 = None, None
    for i in range(l):
        if B[i][j] == True: continue
        if G1(i, j) == False: continue
        if i1 is None or i1 > i: i1 = i
        if i2 is None or i2 < i: i2 = i
    if i1 is None and i2 is None: continue
    u1, u2 = U[i1], U[i2 + 1]
    p = [xy(u1, v1), xy(u1, v2), xy(u2, v2), xy(u2, v1)]
    draw_poly(p, 'fill=cyan, opacity=0.5')


for j in range(l):
    v1, v2 = V[j], V[j + 1]
    i1, i2 = None, None
    for i in range(l):
        if B[i][j] == True: continue
        if G3(i, j) == False: continue
        if i1 is None or i1 > i: i1 = i
        if i2 is None or i2 < i: i2 = i
    if i1 is None and i2 is None: continue
    u1, u2 = U[i1], U[i2 + 1]
    p = [xy(u1, v1), xy(u1, v2), xy(u2, v2), xy(u2, v1)]
    draw_poly(p, 'fill=cyan, opacity=0.5')


for u in U:
    a = (x_uy(u, L), L) if x_uy(u, L) <= R else (R, y_xu(R, u))
    b = (x_uy(u, R), R) if x_uy(u, R) >= L else (L, y_xu(L, u))
    draw_poly([a, b], 'opacity=0.1')
        

for v in V:
    a = (x_vy(v, L), L) if x_vy(v, L) >= L else (L, y_xv(L, v))
    b = (x_vy(v, R), R) if x_vy(v, R) <= R else (R, y_xv(R, v))
    draw_poly([a, b], 'opacity=0.1')


draw_dots(n2)

draw_poly([(mid, L), (mid, R)], 'opacity=0.5')
draw_poly([(L, mid), (R, mid)], 'opacity=0.5')

res += '\\end{tikzpicture}\n\\end{document}'
print(res)

