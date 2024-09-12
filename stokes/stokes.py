import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
import itertools


def boundaryp(i, j):
    return i <= 0 or j <= 0 or i >= m or j >= m


def f(i, j, d):
    return 0


def add(c, f, i, j, d=None):
    if not boundaryp(i, j):
        if (f, i, j) not in ik:
            ik[f, i, j] = len(ik)
        data.append(c)
        col.append(ik[f, i, j])
        row.append(len(rhs) - 1)
    else:
        assert f == "u" or f == "v"
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
for i, j in itertools.product(range(-1, m + 1), range(-1, m + 1)):
    if not boundaryp(i - 1, j) and not boundaryp(i, j):
        rhs.append(0)
        add(1, "u", i - 1, j)
        add(1, "u", i, j - 1)
        add(-4, "u", i, j)
        add(1, "u", i, j + 1)
        add(1, "u", i + 1, j)
        add(-1, "p", i - 1, j)
        add(1, "p", i, j)
        rhs[-1] += f(i, j, 0)
    if not boundaryp(i, j - 1) and not boundaryp(i, j):
        rhs.append(0)
        add(1, "v", i - 1, j)
        add(1, "v", i, j - 1)
        add(-4, "v", i, j)
        add(1, "v", i, j + 1)
        add(1, "v", i + 1, j)
        add(-1, "p", i, j - 1)
        add(1, "p", i, j)
        rhs[-1] += f(i, j, 1)
    if not boundaryp(i, j) or not boundaryp(i, j + 1) or not boundaryp(
            i + 1, j):
        rhs.append(0)
        add(-1, "u", i, j)
        add(-1, "v", i, j)
        add(1, "v", i, j + 1)
        add(1, "u", i + 1, j)
for i, j in itertools.product(range(-1, m + 1), range(-1, m + 1)):
    if not boundaryp(i, j):
        rhs.append(0)
        add(0, "p", i, j)
        break
# sol = scipy.sparse.linalg.spsolve(A, rhs)
A = scipy.sparse.csr_matrix((data, (row, col)), dtype=float)
sol, istop, itn, r1norm, r2norm, acond, *rest = scipy.sparse.linalg.lsqr(
    A, rhs)
print(f"{acond=} {r1norm=}")
print("unknown:", len(ik))
print("equations:", len(rhs))

scales = {"u": h, "v": h, "p": 1}
names = "u", "v", "p"
fields = {name: np.empty((m + 1, m + 1)) for name in names}
for f in fields.values():
    f.fill(None)
for (f, i, j), k in ik.items():
    fields[f][i, j] = sol[k]
for name, scale in scales.items():
    plt.imshow(fields[name].T * scale, origin="lower")
    plt.colorbar()
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("stokes.%s.png" % name)
    plt.close()
