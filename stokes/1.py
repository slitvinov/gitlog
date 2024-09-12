import math
import matplotlib.pyplot as plt
import numpy as np
import scipy


def u(i, j):
    return 0


def boundaryp(i):
    return i <= 0 or i >= m


def f(i):
    return (i / m) / scales["f"]


def add(c, *idx):
    f, *i = idx
    if f == "sigma" or f == "p" or not boundaryp(*i):
        if idx not in ik:
            ik[idx] = len(ik)
        data.append(c)
        col.append(ik[idx])
        row.append(len(rhs) - 1)
    else:
        val = 0
        rhs[-1] -= c * val


plt.rcParams["image.cmap"] = "jet"
m = 20
h = 1 / m
scales = {"u": h, "p": 1, "f": 1 / h}
ik = {}
data = []
col = []
row = []
rhs = []
for i in range(-1, m + 1):
    if not boundaryp(i):
        rhs.append(0)
        add(1, "u", i - 1)
        add(-2, "u", i)
        add(1, "u", i + 1)
        add(-1, "p", i - 1)
        add(1, "p", i)
        rhs[-1] += f(i)
    if not boundaryp(i) or not boundaryp(i + 1):
        rhs.append(0)
        add(-h, "sigma")
        add(-1, "u", i)
        add(1, "u", i + 1)
for i in range(-1, m + 1):
    if not boundaryp(i):
        rhs.append(0)
        add(1, "p", i)
        break

A = scipy.sparse.csr_matrix((data, (row, col)), dtype=float)
sol = scipy.sparse.linalg.spsolve(A, rhs)
print("unknown:", len(ik))
print("equations:", len(rhs))
print("sigma:", sol[ik[
    "sigma",
]])
names = "u", "p"
fields = {name: np.empty(m + 1) for name in names}
for f in fields.values():
    f.fill(None)
for (name, *ij), k in ik.items():
    if name in names:
        i, = ij
        fields[name][i] = sol[k]
for name, f in fields.items():
    plt.plot(f * scales[name], 'o-')
    plt.tight_layout()
    plt.savefig("1.%s.png" % name)
    plt.close()
