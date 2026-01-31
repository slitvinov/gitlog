import math

import matplotlib.pyplot as plt
import numpy as np
import scipy


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
    rhs.append(f0 * h2)
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
    rhs.append(f(i, j) * h2)
    add(i, j, -4)
    add(i - 1, j, 1)
    add(i + 1, j, 1)
    add(i, j - 1, 1)
    add(i, j + 1, 1)


scheme = five
m = 10
h2 = 1 / m**2
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
fi = np.empty((m, m))
ue = np.empty((m, m))
fi.fill(None)
ue.fill(None)
l2 = 0
for s, t in zip(sol, ik):
    fi[t] = s
    ue[t] = u(*t)
    l2 += (fi[t] - ue[t])**2
plt.imshow(fi.T, origin="lower")
plt.axis("off")
plt.tight_layout()
plt.savefig("9points.png")
plt.close()

plt.imshow(ue.T, origin="lower")
plt.axis("off")
plt.tight_layout()
plt.savefig("9points.exact.png")
print("l2: %.2e" % (math.sqrt(l2 / m**2)))
