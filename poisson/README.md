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


A five-point stencil (dereived by Rossent in 1975) to approximate
Laplace operator gains a lot of accury for the model computational
work compare to popular five-point stencil. Here is a complite example
which comapares the two and reporduced the table from (Strikwerda's
books, references are in the notebook).  And we talking about accuracy
~1e-8 on the grid like in the picture.

https://colab.research.google.com/github/slitvinov/gitlog/blob/main/poisson/9points.ipynb
