import matplotlib.pyplot as plt
import scipy
import numpy as np
import math
import itertools
def u(i, j):
    x = i / m
    y = j / m
    return math.cos(x) * math.sin(y)
def f(i, j):
    x = i / m
    y = j / m
    return -2 * math.cos(x) * math.sin(y)
def boundary(i, j):
    cond = i == 0 or j == 0 or j == m or i == m
    return u(i, j) if cond else None
def add(i, j, c):
    val = boundary(i, j)
    if boundary(i, j) is None:
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
for scheme, m in itertools.product((five, nine), (10, 20, 40)):
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
    err = 0
    for s, t in zip(sol, ik):
        err += (s - u(*t))**2
    print(f"{scheme.__name__} {h:.3f} {math.sqrt(err / m**2):.2e}")
