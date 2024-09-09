How to solve a linear PDE without making a mess of the indices?  My
example is Poisson's equation, illustrated in 1D. The result,
unsurprisingly, is a bunch of parabolas.

https://colab.research.google.com/github/slitvinov/gitlog/blob/main/poisson/1.ipynb

With very few modifications, it extends to 2D (and 3D). Here, two
sections of the boundary have different conditions.

https://colab.research.google.com/github/slitvinov/gitlog/blob/main/poisson/2.ipynb

```
jupytext --sync 1.md 2.md
```

A nine-point stencil (derived by Rosser in 1975) offers superior
accuracy for approximating the Laplace operator compared to the common
five-point stencil. Here's an example comparing both, reproducing a
table from Strikwerda's book (references in the notebook):

https://colab.research.google.com/github/slitvinov/gitlog/blob/main/poisson/9points.ipynb

It achieves 1e-8 accuracy on the grid shown.
