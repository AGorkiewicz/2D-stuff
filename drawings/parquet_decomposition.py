import math
import random
from dataclasses import dataclass

res = '\\documentclass{standalone}\n\\usepackage{tikz}\n\\begin{document}\n\\begin{tikzpicture}'


phi_x = 10 / 2
phi_y = -3 / 2
psi_x = 5 / 2
psi_y = 6 / 2

@dataclass
class Point:
    x: float
    y: float
    def __add__(self, a):   return Point(self.x + a.x, self.y + a.y)
    def __mul__(self, a):   return Point(a * self.x, a * self.y)
    @property
    def h(self):    return phi_x * self.y - phi_y * self.x
    @property
    def s(self):    return psi_x * self.y - psi_y * self.x

phi = Point(phi_x, phi_y)
psi = Point(psi_x, psi_y)

def dot(u, v):      return u.x * v.x + u.y * v.y
def cross(u, v):    return u.x * v.y - u.y * v.x

def x_hs(h, s): return (h * psi_x - s * phi_x) / (phi_x * psi_y - phi_y * psi_x)
def y_hs(h, s): return (h * psi_y - s * phi_y) / (phi_x * psi_y - phi_y * psi_x)

def xy(h, s): return Point(x_hs(h, s), y_hs(h, s))

def x_hy(h, y): return (phi_x * y - h) / phi_y
def y_hx(h, x): return (phi_y * x + h) / phi_x
def x_sy(h, y): return (psi_x * y - h) / psi_y
def y_sx(h, x): return (psi_y * x + h) / psi_x


s = 7
t = 9

ax = 0
bx = phi_x * (s - 1) + psi_x * (t - 1)
ay = phi_y * (s - 1)
by = psi_y * (t - 1)

res += f'\\draw [white, fill=white] ({ax - 1}, {ay}) rectangle ({bx + 1}, {by});'


def draw_point(p, color = 'black'):
    global res
    res += f'\\draw[{color}, fill={color}] ({p.x}, {p.y}) circle (4pt);'


def draw_line(p, q, color = 'black'):
    global res
    res += f'\\draw[{color}] ({p.x}, {p.y}) -- ({q.x}, {q.y});'


def color(ax, bx, ay, by, color):
    for i in range(ax, bx + 1):
        for j in range(ay, by + 1):
            draw_point(phi * i + psi * j, color)


draw_line(phi * 0.5 + psi * (-1), phi * 0.5 + psi * (t), 'loosely dashed, red, ultra thick')
draw_line(phi * 3.5 + psi * (-1), phi * 3.5 + psi * (t), 'loosely dashed, red, ultra thick')
draw_line(phi * 4.5 + psi * (-1), phi * 4.5 + psi * (t), 'loosely dashed, red, ultra thick')

draw_line(phi * (0.5) + psi * (3.5), phi * 3.5 + psi * (3.5), 'loosely dashed, blue, ultra thick')
draw_line(phi * (0.5) + psi * (5.5), phi * 3.5 + psi * (5.5), 'loosely dashed, blue, ultra thick')
draw_line(phi * (3.5) + psi * (5.5), phi * 4.5 + psi * (5.5), 'loosely dashed, blue, ultra thick')
draw_line(phi * (3.5) + psi * (4.5), phi * 4.5 + psi * (4.5), 'loosely dashed, blue, ultra thick')
draw_line(phi * (4.5) + psi * (3.5), phi * 6.5 + psi * (3.5), 'loosely dashed, blue, ultra thick')
draw_line(phi * (-0.5) + psi * (2.5), phi * (0.5) + psi * (2.5), 'loosely dashed, blue, ultra thick')

draw_line(phi * (-0.5) + psi * (6.5), phi * (0.5) + psi * (6.5), 'loosely dashed, blue, ultra thick')

color(0, 0, 0, 2, 'black')
color(0, 0, 3, 6, 'red')
color(0, 0, 7, 8, 'green')

color(1, 3, 0, 3, 'black')
color(1, 3, 4, 5, 'red')
color(1, 3, 6, 8, 'green')

color(4, 4, 0, 4, 'black')
color(4, 4, 5, 5, 'red')
color(4, 4, 6, 8, 'green')

color(5, 6, 0, 3, 'black')
color(5, 6, 4, 8, 'green')

res += '\\end{tikzpicture}\n\\end{document}'
print(res)

