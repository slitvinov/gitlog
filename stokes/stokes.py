import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
import itertools


def boundaryp(i, j):
    cond0 = i <= 0 or j <= 0 or i >= m or j >= m
    cond1 = (8 * i - 2 * m)**2 + (8 * j - 6 * m)**2 < m**2
    return cond0 or cond1


def fu(i, j):
    return 0


def fv(i, j):
    return 0  # - 1 / scales["f"]


def add(c, *idx):
    f, *ij = idx
    if f == "sigma" or f == "p" or not boundaryp(*ij):
        if idx not in ik:
            ik[idx] = len(ik)
        data.append(c)
        col.append(ik[idx])
        row.append(len(rhs) - 1)
    else:
        i, j = ij
        val = 1 / h if f == "u" and j == m else 0
        rhs[-1] -= c * val


plt.rcParams["image.cmap"] = "jet"
m = 50
ik = {}
data = []
col = []
row = []
rhs = []
h = 1 / m
scales = {"u": h, "v": h, "p": 1, "f": 1 / h}
for i, j in itertools.product(range(-1, m + 1), range(-1, m + 1)):
    if not boundaryp(i, j):
        rhs.append(0)
        add(1, "u", i - 1, j)
        add(1, "u", i, j - 1)
        add(-4, "u", i, j)
        add(1, "u", i, j + 1)
        add(1, "u", i + 1, j)
        add(-1, "p", i - 1, j)
        add(1, "p", i, j)
        rhs[-1] += fu(i, j)
        rhs.append(0)
        add(1, "v", i - 1, j)
        add(1, "v", i, j - 1)
        add(-4, "v", i, j)
        add(1, "v", i, j + 1)
        add(1, "v", i + 1, j)
        add(-1, "p", i, j - 1)
        add(1, "p", i, j)
        rhs[-1] += fv(i, j)
    if not boundaryp(i, j) or not boundaryp(i, j + 1) or not boundaryp(
            i + 1, j):
        rhs.append(0)
        add(-h, "sigma")
        add(-1, "u", i, j)
        add(-1, "v", i, j)
        add(1, "v", i, j + 1)
        add(1, "u", i + 1, j)
for i, j in itertools.product(range(-1, m + 1), range(-1, m + 1)):
    if not boundaryp(i, j):
        rhs.append(0)
        add(1, "p", i, j)
        break
A = scipy.sparse.csr_matrix((data, (row, col)), dtype=float)
sol = scipy.sparse.linalg.spsolve(A, rhs)
print("unknown:", len(ik))
print("equations:", len(rhs))
print("sigma:", sol[ik[
    "sigma",
]])
names = "u", "v", "p"
fields = {name: np.empty((m + 1, m + 1)) for name in names}
for f in fields.values():
    f.fill(None)
for (name, *ij), k in ik.items():
    if name in names:
        i, j = ij
        if not boundaryp(i, j):
            fields[name][i, j] = sol[k]
for name, f in fields.items():
    plt.imshow(f.T * scales[name], origin="lower")
    plt.colorbar()
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("stokes.%s.png" % name)
    plt.close()
