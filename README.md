An illustration of the Variational Bayesian method. I have three coins with biases

<pre>
b1 = 1
b2 = 1/2
b3 = 1/8
</pre>
I pick one, toss it
<pre>
Head
</pre>

What are the probabilities I picked each of the coins (posteriors)? The evidence is

<pre>
E = b1/3 + b2/3 + b3/3 = 13/24
</pre>

and the posteriors are

<pre>
b1/3/E, b2/3/E, b3/3/E = 8/13, 4/13, 1/13 ~
0.615 0.308 0.077
</pre>

The method approximates this answer. It starts with a simpler then general form for posterior distribution `Q`. I simplify by ignoring the third coin:

<pre>
Q = q, 1 - q, 0
</pre>

To find `q` the method maximizes _evidence lower bound_ which is cross entropy of `Q` with the joined distribution minus entropy of `Q`.

<pre>
L1 = q * log(b1/3) + (1 - q) * log(b2/3) = -log(3)*q - log(6)*(1 - q)
L2 = q * log(q) + (1 - q) * log(1 - q)
L = L1 - L2
</pre>
The maximum of `L` is at `q = 2/3` and `Q` (an approximation to the true posteriors) is
<pre>
0.667 0.334 0.000
</pre>

The maximum of `L` is `-0.693` and it is an approximation to `log(E) = -0.613`. The approximation is lower, as the name suggests.

P.S. [a plot of L(q)](https://www.wolframalpha.com/input/?i=plot+%28-q*log%28q%29%29-log%283%29*q-log%281-q%29*%281-q%29-log%286%29*%281-q%29%2C+q%3D0..1)
