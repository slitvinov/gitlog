An illustration of expectation–maximization (EM) algorithm. I have two
coins with biases `t` and `t/2`. I pick one coin and toss it two
times:

    Head, Tail

I want to guess `t`. Likelihood

    L(t) = t * (1 - t) / 2 + t/2 * (1 - t/2) / 2

has a maximum at `t = 0.6` and this is a good guess. EM gets this
answer by iterations. Use any value for `t0` (let's say 0.4) to
compute likelihoods:

    L1 = t0 * (1 - t0) = 0.24
    L2 = t0/2 * (1 - t0/2) = 0.16

normalizing them gives conditional probabilities

    C1 = L1/(L1 + L2) = 0.6
    C2 = L2/(L1 + L2) = 0.4 = 1 - C1

which are used as weights to build a sum of log-likelihoods

    Q(t) = C1 * log(t * (1 - t)) + (1 - C1) * log(t/2 * (1 - t/2))

Note that `t` is an argument and `t0` is absorbed into weights. `t`
which maximizes `Q(t)` is used as `t0` and a new interaction starts. I
got this sequence for `t0`:

    0.40 0.58 0.60 0.60 0.60

The form of `Q(t)` is postulated by the algorithm, and
[wikipedia](https://en.wikipedia.org/wiki/Expectation–maximization_algorithm)
gives the intuition and explains the benefits. An index of a coin is Z
in wikipedia, and the weighted sum in Q(t) is the way to compute an
expectation `E_{Z|X,t0}`

P.S. [em.py](em.py)

P.S.S. A maximimum of Q(t) is at
```
       sqrt(C1 C1  + 8 C1) - C1 - 4
t = - -----------------------------
                    4
```

P.S.S.S. Failed attempts to give an example

- https://stackoverflow.com/questions/11808074/what-is-an-intuitive-explanation-of-the-expectation-maximization-technique
- https://scholar.google.com/scholar?cluster=8576697373613937077&hl=de&as_sdt=2005&sciodt=0,5
- https://math.stackexchange.com/questions/25111/how-does-expectation-maximization-work
- https://math.stackexchange.com/questions/81004/how-does-expectation-maximization-work-in-coin-flipping-problem
