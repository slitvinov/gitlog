An illustration of expectation–maximization (EM) algorithm. I have two coins with biases `t` and `t/2`. I pick one coin blindly and toss it two times:

<pre>
Head, Tail
</pre>

I want to guess t. Likelihood

<pre>
L(t) = t * (1 - t) / 2 + t/2 * (1 - t/2) / 2
</pre>

has a maximum at t = 0.6 and this the best guess. EM gets this answer by iterations. Start with any t0 (let's say 0.4) and compute likelihoods for each coin

<pre>
L1 = t0 * (1 - t0) = 0.24
L2 = t0/2 * (1 - t0/2) = 0.16
</pre>

Normalizing them yields the probabilities of picking a coin given the data

<pre>
C1 = L1/(L1 + L2) = 0.6
C2 = L2/(L1 + L2) = 0.4 = 1 - C1
</pre>

which are used as weights to build a sum of log-likelihoods

<pre>
Q(t) = C1 * log(t * (1 - t)) + (1 - C1) * log(t/2 * (1 - t/2))
</pre>

Note that t is an argument and t0 is absorbed into weights. Set t0 to a value which maximizes Q(t) and start a new iteration. I maximize analytically. I have this sequence for t0:

<pre>
0.40 0.58 0.60 0.60 0.60
</pre>

The algorithm postulates the form of Q(t) and the Wikipedia article gives the intuition and explains the benefits. An index of a coin is Z (unobserved data) on Wikipedia, and the weighted sum in Q(t) is how I compute the expectation E_{Z|X,t0}. Often the problem specific shortcuts are taken to enumerate the states of unobserved data and to maximize Q(t) which complicate many illustrations.


P.S The maximum of Q(t) is at
```
       sqrt(C1 C1  + 8 C1) - C1 - 4
t = - -----------------------------
                    4
```

P.S.S.S. Failed attempts to construct an example

- https://stackoverflow.com/questions/11808074/what-is-an-intuitive-explanation-of-the-expectation-maximization-technique
- https://scholar.google.com/scholar?cluster=8576697373613937077&hl=de&as_sdt=2005&sciodt=0,5
- https://math.stackexchange.com/questions/25111/how-does-expectation-maximization-work
- https://math.stackexchange.com/questions/81004/how-does-expectation-maximization-work-in-coin-flipping-problem
