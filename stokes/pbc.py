import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
import itertools


def boundaryp(i, j):
    return (i <= 0 or j <= 0 or i >= m or j >= m) and not (j in pbc)


def domainp(i, j):
    return (0 < i < m and 0 < j < m) or j in pbc


def realp(i, j):
    return (0 < i < m and 0 < j < m) or (j in pbc and i == 0)


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
pbc = [m - 2]
scales = {"u": h, "v": h, "p": 1, "f": 1 / h}
for i, j in itertools.product(range(-1, m + 1), range(-1, m + 1)):
    if domainp(i, j):
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
    if realp(i, j) or realp(i, j + 1) or realp(i + 1, j):
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

for j in pbc:
    for f in "u", "v":
        for i in -2, -1, 0, 1:
            rhs.append(0)
            add(1, f, i, j)
            add(-1, f, i + m, j)

A = scipy.sparse.csr_matrix((data, (row, col)), dtype=float)
print("unknown:", len(ik))
print("equations:", len(rhs))
sol = scipy.sparse.linalg.spsolve(A, rhs)
print("sigma:", sol[ik[
    "sigma",
]])
names = "u", "v", "p"
fields = {name: np.empty((m + 2, m + 2)) for name in names}
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
    plt.savefig("pbc.%s.png" % name)
    plt.close()
