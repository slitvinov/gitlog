I want to illustrate what variational auctoenocder (VAE) does. I have
coins with unifromly distributed biases `z` and a "biase scaling
device" which changes a bias to `z * t` (`t` is between `0` and
`1`). I pick one coin, scale its bias, and toss two times. Than I pick
another coin, scale, and toss two times. I had

<pre>
Tail-Tail Head-Tail
</pre>

I want to guess `t` and biases of two coins I picked. Lets
<pre>
H = z*t
T = 1 - z*t
</pre>

and `i(expr)` is an integral of `expr` by z from 0 to 1. Likelihood
<pre>
E = i(T * T) * i(H * T)
</pre>
is at maximum for `t = 0.473` and two conditional distributions are weigthed guesses for two biases.
<pre>
Q1 = T * H / i(T * H)
Q2 = T * T / i(T * T)
</pre>

VAE approximates those answers. Choose approximations to conditional.
My pick is two liner functions

<pre>
q1(z) = p * z - (p - 2)/2
q2(z) = -p * z - (p + 2)/2
</pre>

Slopes are connected and intersects are fixed by normalization. VAE
maximizes _evidence lower bound_ to find parameters `p` and `t` which
is KL-divergence of conditional with prior and ... I choose uniform
priror over `z`.

<pre>
L1 = i(q1(z) * log(H * T)) + i(q2(z) * log(T * T))
L2 = i(q1(z) * log(q1(z))) + i(q2(z) * log(q2(z)))
L = L1 - L2
</pre>

Maximum of `L` is at `t = 0.489` and `p = 1.562`. VAE approximations
and maximum likelihood solutions are cover image. VAE does not learn
enough about generative model to mimic it and to tell the
probabilities of the data points.

P.S. `z` is a latent variable, `t` the generative model parameter,
log(H * T) and log(T * T) are encoders, and q2(z) and q1(z) are
decoders.

<img src="vai.png" align="center">