import matplotlib.pyplot as plt
import numpy as np
import scipy


def boundary(i, j):
    boundary0 = i == m - 1 or j == 0 or j == m - 1 or i <= j
    boundary1 = (8 * i - 6 * m)**2 + (8 * j - 2 * m)**2 < m**2
    return 0 if boundary0 else 1 if boundary1 else None


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


m = 40
ik = {}
data = []
col = []
row = []
rhs = []
for i in range(m):
    for j in range(m):
        if boundary(i, j) is None:
            rhs.append(0)
            add(i, j, -4)
            add(i - 1, j, 1)
            add(i + 1, j, 1)
            add(i, j - 1, 1)
            add(i, j + 1, 1)
A = scipy.sparse.csr_matrix((data, (row, col)), dtype=float)
sol = scipy.sparse.linalg.spsolve(A, rhs)
fi = np.empty((m, m))
fi.fill(None)
for s, t in zip(sol, ik):
    fi[t] = s
plt.imshow(fi)
plt.axis("off")
plt.tight_layout()
plt.savefig("2.png")
