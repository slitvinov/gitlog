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
M0 = T * H / i(T * H)
M1 = T * T / i(T * T)
</pre>

VAE approximates those answers.
