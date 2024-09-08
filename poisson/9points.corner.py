import math
import matplotlib.pyplot as plt
import numpy as np
import scipy


def u(i, j):
    x = i / m
    y = j / m
    th = math.atan2(y, x)
    r2 = x**2 + y**2
    return r2**(1 / 3) * math.sin(2 * th / 3)


def boundary(i, j):
    cond0 = i <= 0 or j <= 0 or i >= m or j >= m
    cond1 = 2 * i >= m and 2 * j <= m
    return u(i, j) if cond0 or cond1 else None


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
    rhs.append(0)
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
    rhs.append(0)
    add(i, j, -4)
    add(i - 1, j, 1)
    add(i + 1, j, 1)
    add(i, j - 1, 1)
    add(i, j + 1, 1)


plt.rcParams["image.cmap"] = "jet"
scheme = nine
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
error = np.empty((m, m))
error.fill(None)
for t, s in zip(ik, sol):
    error[t] = (s - u(*t))**2
plt.imshow(error.T, origin="lower")
plt.colorbar()
plt.axis("off")
plt.tight_layout()
plt.savefig("9points.corner.png")
plt.close()
