"""Generate figures/whitney.tex, the Whitney decomposition figure.

Run from the directory 2D-new:  python3 figures/whitney.py > figures/whitney.tex

The active text A is the union of the occurrences [m]^2 + q for q in Q.
Cells are the tilted squares aligned with phi and psi; a level-j cell is good
if all of its points have depth larger than D_j (for readability, the figure
uses this smaller threshold instead of 2 D_j), and the selected cells are the
maximal good cells.
"""
import math
from collections import deque

n, m = 60, 40
Q = [(0, 20), (4, 13), (9, 8), (15, 4), (20, 0), (0, 0), (20, 12), (11, 20), (17, 16)]
phi, psi = (2, -1), (1, 2)
DELTA = phi[0] * psi[1] - phi[1] * psi[0]          # det(phi, psi) = 5
SIDES = [2 * 2 ** j for j in range(4)]             # cell side lengths D_j
COLORS = ["orange!60", "yellow!60", "green!30", "blue!20"]
SCALE = 0.085                                      # cm per unit

A = {(q[0] + x, q[1] + y) for q in Q for x in range(m) for y in range(m)}

# depth = maximum-norm distance to the complement of A (BFS in the king's graph)
depth = {}
queue = deque()
for x in range(-1, n + 1):
    for y in range(-1, n + 1):
        if (x, y) not in A:
            depth[(x, y)] = 0
            queue.append((x, y))
while queue:
    u = queue.popleft()
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            v = (u[0] + dx, u[1] + dy)
            if v in A and v not in depth:
                depth[v] = depth[u] + 1
                queue.append(v)

norm_phi, norm_psi = math.hypot(*phi), math.hypot(*psi)


def coords(u):
    """Coordinates (s, t) of u with u = s * phi/|phi| + t * psi/|psi|."""
    k1 = u[0] * psi[1] - u[1] * psi[0]
    k2 = phi[0] * u[1] - phi[1] * u[0]
    return k1 * norm_phi / DELTA, k2 * norm_psi / DELTA


def cell_of(u, j):
    s, t = coords(u)
    return math.floor(s / SIDES[j]), math.floor(t / SIDES[j])


points = [(x, y) for x in range(-2, n + 2) for y in range(-2, n + 2)]
cells = [dict() for _ in SIDES]
for u in points:
    for j in range(len(SIDES)):
        cells[j].setdefault(cell_of(u, j), []).append(u)


def good(j, c):
    pts = cells[j].get(c, [])
    return len(pts) > 0 and all(depth.get(u, 0) > SIDES[j] for u in pts)


top = len(SIDES) - 1
selected = [(j, c) for j in range(len(SIDES)) for c in cells[j]
            if good(j, c) and (j == top or not good(j + 1, (c[0] // 2, c[1] // 2)))]

unit_phi = (phi[0] / norm_phi, phi[1] / norm_phi)
unit_psi = (psi[0] / norm_psi, psi[1] / norm_psi)


def corner(s, t):
    return (s * unit_phi[0] + t * unit_psi[0], s * unit_phi[1] + t * unit_psi[1])


def pt(x, y, shift=0.5):
    return "(%.3f,%.3f)" % ((x + shift) * SCALE, (y + shift) * SCALE)


out = [r"\begin{scope}", r"\clip (0,0) rectangle (%.3f,%.3f);" % (n * SCALE, n * SCALE)]
for j, (a, b) in sorted(selected, key=lambda z: -z[0]):
    d = SIDES[j]
    poly = [corner(a * d, b * d), corner((a + 1) * d, b * d),
            corner((a + 1) * d, (b + 1) * d), corner(a * d, (b + 1) * d)]
    out.append(r"\filldraw[fill=%s, draw=black!60, line width=0.3pt] " % COLORS[j]
               + " -- ".join(pt(x, y) for x, y in poly) + " -- cycle;")
out.append(r"\end{scope}")

# boundary of A, with collinear unit edges merged
horizontal, vertical = {}, {}
for (x, y) in A:
    if (x, y - 1) not in A:
        horizontal.setdefault(y, []).append(x)
    if (x, y + 1) not in A:
        horizontal.setdefault(y + 1, []).append(x)
    if (x - 1, y) not in A:
        vertical.setdefault(x, []).append(y)
    if (x + 1, y) not in A:
        vertical.setdefault(x + 1, []).append(y)


def runs(values):
    values = sorted(values)
    result, start, prev = [], values[0], values[0]
    for v in values[1:]:
        if v != prev + 1:
            result.append((start, prev + 1))
            start = v
        prev = v
    result.append((start, prev + 1))
    return result


for y, xs in horizontal.items():
    for a, b in runs(xs):
        out.append(r"\draw[black, thick] %s -- %s;" % (pt(a, y, 0), pt(b, y, 0)))
for x, ys in vertical.items():
    for a, b in runs(ys):
        out.append(r"\draw[black, thick] %s -- %s;" % (pt(x, a, 0), pt(x, b, 0)))

print("\n".join(out))
