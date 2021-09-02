A simple illustration why Bayesian model selection is hard. Let's select
a model for a coin. Toss it three times:

    Head, Tail, Tail

Model one (M1) is a fair coin, model two (M2) is a coin with a
parameter (bias) which can be 1/2 (a), 1/3 (b), and 2/3 (c).

Pick priors

    P1 = 1/2
    P2a = 1/6
    P2b = 1/6
    P2c = 1/6

Compute likelihoods

    L1 = 1/2 * 1/2 * 1/2
    L2a = 1/2 * 1/2 * 1/2
    L2b = 1/3 * 2/3 * 2/3
    L2c = 2/3 * 1/3 * 1/3

and the evidence

    E = P1*L1 + P2a*L2a + P2b*L2b + P2c*L2c = 13/108

The posterior of M1 is

    O1 = L1*P1/E = 27/52 ~ 0.52

Note that M1 is "nested" in M2 (for bias = 1/2), M2 with bias = 1/3
fits better, but the data tells me to believe in M1 a bit more than
before. All posteriors to stare at

    0.52 0.17 0.21 0.10

priors were

    0.50 0.17 0.17 0.17

"Unfixing" priors and looking at how O1 changes is also
interesting. All priors (not only for best-fitting parameters)
"inside" a model influence the posterior of the model index.