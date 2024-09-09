---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

[![Open in
Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/slitvinov/gitlog/blob/main/poisson/9points.ipynb)

```{code-cell} ipython3
import itertools
import math
import numpy as np
import scipy
def u(i, j):
    return math.cos(i / m) * math.sin(j / m)
def f(i, j):
    return -2 * math.cos(i / m) * math.sin(j / m)
def boundary(i, j):
    cond = i == 0 or j == 0 or j == m or i == m
    return u(i, j) if cond else None
def add(i, j, c):
    val = boundary(i, j)
    if boundary(i, j) is None:
        if (i, j) not in ik:
            ik[i, j] = len(ik)
        data.append(c)
        col.append(ik[i, j])
        row.append(len(rhs) - 1)
    else:
        rhs[-1] -= c * val
def nine():
    f0 = 1 / 12 * f(i - 1, j)
    f0 += 1 / 12 * f(i, j - 1)
    f0 += 2 / 3 * f(i, j)
    f0 += 1 / 12 * f(i, j + 1)
    f0 += 1 / 12 * f(i + 1, j)
    rhs.append(f0 * h**2)
    add(i - 1, j - 1, 1 / 6)
    add(i - 1, j, 2 / 3)
    add(i - 1, j + 1, 1 / 6)
    add(i, j - 1, 2 / 3)
    add(i, j, -10 / 3)
    add(i, j + 1, 2 / 3)
    add(i + 1, j - 1, 1 / 6)
    add(i + 1, j, 2 / 3)
    add(i + 1, j + 1, 1 / 6)
def five():
    rhs.append(f(i, j) * h**2)
    add(i, j, -4)
    add(i - 1, j, 1)
    add(i + 1, j, 1)
    add(i, j - 1, 1)
    add(i, j + 1, 1)
print("scheme      h      error")
for scheme, m in itertools.product((five, nine), (10, 20, 40)):
    h = 1 / m
    ik = {}
    data = []
    col = []
    row = []
    rhs = []
    for i in range(m):
        for j in range(m):
            if boundary(i, j) is None:
                scheme()
    A = scipy.sparse.csr_matrix((data, (row, col)), dtype=float)
    sol = scipy.sparse.linalg.spsolve(A, rhs)
    err = 0
    for s, t in zip(sol, ik):
        err += (s - u(*t))**2
    print(f"{scheme.__name__} {h:8.3f} {math.sqrt(err / m**2):10.2e}")
```
