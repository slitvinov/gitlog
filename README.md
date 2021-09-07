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

What are the probabilities I picked each of the coins (posteriors)? The evidance is

<pre>
E = b1/3 + b2/3 + b3/3 = 13/24
</pre>
and the poseriors are
<pre>
b1/3/E, b2/3/E, b3/3/E = 8/13, 4/13, 1/13
</pre>

The method approximates this answer. I assume posteriors are (pretending the third coin was not picked)

<pre>
Q = q, 1 - q, 0
</pre>

To find `q` the method maximizes evidence lower bound which has two parts: cross entropy of `Q` and the joined distribution and entropy of `Q`.

<pre>
L1 = q * log(b1/3) + (1 - q) * log(b2/3) = -log(3)*q - log(6)*(1 - q)
L2 = q * log(q) + (1 - q) * log(1 - q)
L = L1 - L2
</pre>
The maximum of `L` is at `q = 2/3` and `Q` is
<pre>
0.667 0.334 0.00
</pre>
and the exact answer was
<pre>
0.615 0.308 0.077
</pre>
L at maximum is `-0.693` which is an approximation to `log(E) = -0.613`. And the approximation is lower as the name suggests.
