import math
import matplotlib.pyplot as plt
import numpy as np
import scipy
import itertools
import collections


def boundaryp(i, j):
    cond0 = (i <= 0 or j <= 0 or i >= m or j >= m) and not (j in pbc)
    cond1 = (8 * i - 3 * m)**2 + (8 * j - 3 * m)**2 < 2 * m**2
    cond2 = (8 * i - 6 * m)**2 + (8 * j - 6 * m)**2 < 2 * m**2
    return cond0 or cond1 or cond2


def domainp(i, j):
    return not boundaryp(i, j) and 0 <= i < m


def realp(i, j):
    return not boundaryp(i, j) and 0 <= i < m


def fu(i, j):
    return 1 / scales["f"]


def fv(i, j):
    return 0


def pbc0(i, j):
    if j in pbc:
        while i < 0:
            i += m
        while i >= m:
            i -= m
    return i, j


def add(c, *idx):
    f, *ij = idx
    if f == "u" or f == "v" or f == "p":
        ij = pbc0(*ij)
        return add0(c, f, *ij)
    else:
        return add0(c, f, *ij)


def add0(c, *idx):
    f, *ij = idx
    if f == "sigma" or f == "p" or not boundaryp(*ij):
        if idx not in ik:
            ik[idx] = len(ik)
        data.append(c)
        col.append(ik[idx])
        row.append(len(rhs) - 1)
    else:
        i, j = ij
        val = 0
        # val = -1 / h if f == "u" and j == m else 0
        rhs[-1] -= c * val


plt.rcParams["image.cmap"] = "jet"
m = 20
ik = {}
data = []
col = []
row = []
rhs = []
h = 1 / m
pbc = set(range(m))
scales = {"u": h, "v": h, "p": 1, "f": 1 / h}
for i, j in itertools.product(range(-1, m + 1), range(-1, m + 1)):
    if domainp(i, j):
        rhs.append(0)
        add(-1, "u", i - 1, j)
        add(-1, "u", i, j - 1)
        add(4, "u", i, j)
        add(-1, "u", i, j + 1)
        add(-1, "u", i + 1, j)
        add(-1, "p", i - 1, j)
        add(1, "p", i, j)
        rhs[-1] += fu(i, j)
        rhs.append(0)
        add(-1, "v", i - 1, j)
        add(-1, "v", i, j - 1)
        add(4, "v", i, j)
        add(-1, "v", i, j + 1)
        add(-1, "v", i + 1, j)
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
D = collections.defaultdict(list)
for r, c, d in zip(row, col, data):
    D[r].append((c, d))

data0 = []
row0 = []
col0 = []
rhs0 = []
seen = set()
cnt = 0
for ro, rh in zip(D.values(), rhs):
    ro = tuple(ro)
    if not ro in seen or len(ro) == 0:
        row0.extend([len(rhs0)] * len(ro))
        col0.extend(t[0] for t in ro)
        data0.extend(t[1] for t in ro)
        rhs0.append(rh)
    else:
        cnt += 1
    seen.add(ro)
print("duplicates:", cnt)
A = scipy.sparse.csr_array((data0, (row0, col0)), dtype=float)
print("unknown:", len(ik))
print("equations:", len(rhs))
sol = scipy.sparse.linalg.spsolve(A, rhs0)
# sol, *rest = scipy.sparse.linalg.lsqr(A, rhs0)
print("sigma:", sol[ik[
    "sigma",
]])
names = "u", "v", "p"
fields = {name: np.empty((m, m)) for name in names}
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
