An illustration of expectation–maximization (EM) algorithm. I have two
coins with biases `t` and `t/2`. I pick one coin and toss it two
times:

    Head, Tail

I want to guess `t`. Likelihood

    L(t) = t * (1 - t) / 2 + t/2 * (1 - t/2) / 2

has a maximum at t = 0.6 and this is a good guess. EM gets this number
by iterations. Use an initial guess `t0 = 0.4` to compute likelihoods:

    L1 = t0 * (1 - t0) = 0.24
    L2 = t0/2 * (1 - t0/2) = 0.16

normalizing them gives conditional probabilities

    C1 = L1/(L1 + L2) = 0.6
    C2 = L2/(L1 + L2) = 0.4 = 1 - C1

which are used as weights to build an approximation of log(L(t))

    Q(t) = C1 * log(t * (1 - t)) + (1 - C1) * log(t/2 * (1 - t/2))

Note that `t` is an argument and `t0` is absorbed into weights. `t`
which maximizes Q(t) is used as `t0` and a new interaction starts. I
got this sequence for `t0`:

    0.40 0.58 0.60 0.60 0.60

P.S. Hints to related this illustration to a [description in
wikipedia](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm#Description):
an index of a coin is Z, and weighted sum in Q(t) is a way to compute an expectation `E_{Z|X,t}`

P.S.S. A maximimum of Q(t) is at
```
                                     2
                       sqrt(C1  + 8 C1) - C1 - 4
                 t = - -------------------------
                                   4
```
