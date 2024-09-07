import matplotlib.pyplot as plt
import scipy
import numpy as np
import random
def boundary(i):
    return i == 0 or i == m - 1 or i in boundaries
def add(i, c):
    if not boundary(i):
        if not i in ik:
            ik[i] = len(ik)
        col.append(ik[i])
        row.append(len(rhs) - 1)
        data.append(c)
m = 100
random.seed(12)
boundaries = random.sample(range(m), 8)
rhs = []; row = []; col = []; data = []; ik = {}
for i in range(m):
    if not boundary(i):
        rhs.append(-1)
        add(i, -1)
        add(i + 1, 1 / 2)
        add(i - 1, 1 / 2)
A = scipy.sparse.csr_matrix((data, (row, col)), dtype=float)
sol = scipy.sparse.linalg.spsolve(A, rhs)
fi = np.zeros(m)
for i, s in zip(ik, sol):
    fi[i] = s
plt.plot(fi)
plt.tight_layout()
plt.savefig("1.png")
