import math
import matplotlib.pyplot as plt
import numpy as np
import scipy


def u(i, j):
    return 0


def boundaryp(i):
    return i <= 0 or i >= m


def f(i, d):
    return h


FIELDS = {("u", 0): 0, ("p", None): 1}


def add(f, c, i, d=None):
    if not boundaryp(i):
        if i not in ik:
            ik[i] = len(ik)
        data.append(c)
        col.append(nf * ik[i] + FIELDS[f, d])
        row.append(len(rhs) - 1)
    else:
        assert f == "u"
        val = 0
        rhs[-1] -= c * val


plt.rcParams["image.cmap"] = "jet"
nf = len(FIELDS)
m = 20
h = 1 / m
ik = {}
data = []
col = []
row = []
rhs = []
for i in range(-1, m + 1):
    if not boundaryp(i) and not boundaryp(i - 1):
        rhs.append(0)
        add("u", 1, i - 1, 0)
        add("u", -2, i, 0)
        add("u", 1, i + 1, 0)
        add("p", -1, i - 1)
        add("p", 1, i)
        rhs[-1] += f(i, 0)
    if not boundaryp(i) or not boundaryp(i + 1):
        rhs.append(0)
        add("u", -1, i, 0)
        add("u", 1, i + 1, 0)
rhs.append(0)
add("p", 1, 1)

A = scipy.sparse.csr_matrix((data, (row, col)), dtype=float)
sol, istop, itn, r1norm, r2norm, acond, *rest = scipy.sparse.linalg.lsqr(
    A, rhs)
print(f"{acond=} {r1norm=}")
print("unknown:", nf * len(ik))
print("equations:", len(rhs))

field = np.empty((nf, m + 1))
field.fill(None)
for i, k in ik.items():
    l = nf * k
    field[:, i] = sol[l:l + nf]
for name, scale, f in zip(("u", "p"), (h, 1), field):
    plt.plot(scale * f, '-o')
    plt.tight_layout()
    plt.savefig("1.%s.png" % name)
    plt.close()
