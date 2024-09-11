import math
import matplotlib.pyplot as plt
import numpy as np
import scipy

def u(i, j):
    return 0

def boundary(i, j):
    cond0 = i <= 0 or j <= 0 or i >= m or j >= m
    return u(i, j) if cond0 else None

def f(i, j, d):
    return d

FIELDS = {
    ("u", 0) : 0,
    ("u", 1) : 1,
    ("p", None) : 2}

def add(f, c, i, j, d=None):
    val = boundary(i, j)
    if val is None:
        if (i, j) not in ik:
            ik[i, j] = len(ik)
        data.append(c)
        col.append(nf * ik[i, j] + FIELDS[f, d])
        row.append(len(rhs) - 1)
    else:
        rhs[-1] -= c * val


plt.rcParams["image.cmap"] = "jet"
nf = len(FIELDS)
m = 100
ik = {}
data = []
col = []
row = []
rhs = []
for i in range(-1, m + 1):
    for j in range(-1, m + 1):
        if boundary(i, j) is None:
            rhs.append(0)
            add("u", 1, i-1, j, 0)
            add("u", 1, i, j-1, 0)
            add("u", -4, i, j, 0)
            add("u", 1, i, j+1, 0)
            add("u", 1, i+1, j, 0)
            add("p", -1, i-1, j)
            add("p", 1, i, j)
            rhs[-1] += f(i,j,0)
            rhs.append(0)
            add("u", 1, i-1, j, 1)
            add("u", 1, i, j-1, 1)
            add("u", -4, i, j, 1)
            add("u", 1, i, j+1, 1)
            add("u", 1, i+1, j, 1)
            add("p", -1, i, j-1)
            add("p", 1, i, j)
            rhs[-1] += f(i,j,1)
            rhs.append(0)
            add("u", -1, i, j, 0)
            add("u", -1, i, j, 1)
            add("u", 1, i, j+1, 1)
            add("u", 1, i+1, j, 0)

A = scipy.sparse.csr_matrix((data, (row, col)), dtype=float)
sol = scipy.sparse.linalg.spsolve(A, rhs)

field = np.empty((nf, m + 1, m + 1))
field.fill(None)
for (i, j), k in ik.items():
    l = nf * k
    field[:, i, j] = sol[l : l + nf]

for name, f in zip(("ux", "uy", "p"), field):
    plt.imshow(f, origin="lower")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("stokes.%s.png" % name)
