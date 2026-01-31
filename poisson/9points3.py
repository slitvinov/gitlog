import itertools
from math import cos, pi, sin, sqrt
import statistics

import scipy


def u(i, j):
    x = i / m * pi
    y = j / m * pi
    return cos(x**2) * sin(y)


def f(i, j):
    x = i / m * pi
    y = j / m * pi
    z = x * x
    s, c = sin(z), cos(z)
    return -((2 * s + 4 * z * c + c) * sin(y)) * pi**2


def boundary(i, j):
    cond = i == 0 or j == 0 or j == m or i == m
    return u(i, j) if cond else None


def add(i, j, c):
    val = boundary(i, j)
    if val is None:
        if (i, j) not in ik:
            ik[i, j] = len(ik)
        data.append(c)
        col.append(ik[i, j])
        row.append(len(rhs) - 1)
    else:
        rhs[-1] -= c * val


def nine():
    f0 = 1 / 12 * f(i - 1, j)
    f0 += 1 / 12 * f(i, j - 1)
    f0 += 2 / 3 * f(i, j)
    f0 += 1 / 12 * f(i, j + 1)
    f0 += 1 / 12 * f(i + 1, j)
    rhs.append(f0 * h**2)
    add(i - 1, j - 1, 1 / 6)
    add(i - 1, j, 2 / 3)
    add(i - 1, j + 1, 1 / 6)
    add(i, j - 1, 2 / 3)
    add(i, j, -10 / 3)
    add(i, j + 1, 2 / 3)
    add(i + 1, j - 1, 1 / 6)
    add(i + 1, j, 2 / 3)
    add(i + 1, j + 1, 1 / 6)


def five():
    rhs.append(f(i, j) * h**2)
    add(i, j, -4)
    add(i - 1, j, 1)
    add(i + 1, j, 1)
    add(i, j - 1, 1)
    add(i, j + 1, 1)


print("scheme      m      error")
for scheme, m in itertools.product((five, nine),
                                   (10, 20, 40, 80, 120, 160, 320)):
    h = 1 / m
    ik = {}
    data = []
    col = []
    row = []
    rhs = []
    for i in range(m):
        for j in range(m):
            if boundary(i, j) is None:
                scheme()
    A = scipy.sparse.csr_matrix((data, (row, col)), dtype=float)
    sol = scipy.sparse.linalg.spsolve(A, rhs)
    err = []
    for s, t in zip(sol, ik):
        e = (s - u(*t))**2
        err.append(e)
    print(f"{scheme.__name__} {m:8} {sqrt(statistics.mean(err)):10.2e}")
