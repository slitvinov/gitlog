import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
import itertools

def boundaryp(i, j):
    return i <= 0 or j <= 0 or i >= m or j >= m


def f(i, j, d):
    return d * h


def add(f, c, i, j, d=None):
    if not boundaryp(i, j):
        if (i, j) not in ik:
            ik[i, j] = len(ik)
        data.append(c)
        col.append(nf * ik[i, j] + FIELDS[f, d])
        row.append(len(rhs) - 1)
    else:
        assert f == "u"
        val = 0
        # val = 1 / h if j == m and d == 0 else 0
        rhs[-1] -= c * val


plt.rcParams["image.cmap"] = "jet"
FIELDS = {("u", 0): 0, ("u", 1): 1, ("p", None): 2}
nf = len(FIELDS)
m = 20
ik = {}
data = []
col = []
row = []
rhs = []
h = 1 / m
for i, j in itertools.product(range(-1, m + 1), range(-1, m + 1)):
    if not boundaryp(i - 1, j) and not boundaryp(i, j):
        rhs.append(0)
        add("u", 1, i - 1, j, 0)
        add("u", 1, i, j - 1, 0)
        add("u", -4, i, j, 0)
        add("u", 1, i, j + 1, 0)
        add("u", 1, i + 1, j, 0)
        add("p", -1, i - 1, j)
        add("p", 1, i, j)
        rhs[-1] += f(i, j, 0)
    if not boundaryp(i, j - 1) and not boundaryp(i, j):
        rhs.append(0)
        add("u", 1, i - 1, j, 1)
        add("u", 1, i, j - 1, 1)
        add("u", -4, i, j, 1)
        add("u", 1, i, j + 1, 1)
        add("u", 1, i + 1, j, 1)
        add("p", -1, i, j - 1)
        add("p", 1, i, j)
        rhs[-1] += f(i, j, 1)
    if not boundaryp(i, j) or not boundaryp(i, j + 1) or not boundaryp(
            i + 1, j):
        rhs.append(0)
        add("u", -1, i, j, 0)
        add("u", -1, i, j, 1)
        add("u", 1, i, j + 1, 1)
        add("u", 1, i + 1, j, 0)
for i, j in itertools.product(range(-1, m + 1), range(-1, m + 1)):
    if not boundaryp(i, j):
        rhs.append(0)
        add("p", 0, i, j)
        break
# sol = scipy.sparse.linalg.spsolve(A, rhs)
A = scipy.sparse.csr_matrix((data, (row, col)), dtype=float)
sol, istop, itn, r1norm, r2norm, acond, *rest = scipy.sparse.linalg.lsqr(
    A, rhs)
print(f"{acond=} {r1norm=}")
print("unknown:", nf * len(ik))
print("equations:", len(rhs))

field = np.empty((nf, m + 1, m + 1))
field.fill(None)
for (i, j), k in ik.items():
    l = nf * k
    field[:, i, j] = sol[l:l + nf]
for name, scale, f in zip(("ux", "uy", "p"), (h, h, 1), field):
    plt.imshow(f.T * scale, origin="lower")
    plt.colorbar()
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("stokes.%s.png" % name)
    plt.close()
