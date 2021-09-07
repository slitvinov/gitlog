An illustration of the Variational Bayesian method. I have three coins
with biases
```
b1 = 1
b2 = 1/2
b3 = 1/8
```
I pick one, toss it
```
Head
```
What are the probabilities I picked each of the coins (posteriors)? The
evidance is
```
E = b1/3 + b2/3 + b3/3 = 13/24
````
and the poseriors are
```
b1/3/E, b2/3/E, b3/3/E = 8/13, 4/13, 1/13
```

The VB method approximates this answer. I assume posteriors
are (pretending the third coin was not picked)
```
Q = q, 1 - q, 0
```
To find q the method maximizes evidence lower bound which has two parts: cross
entropy of the joined distribution and entropy of Q.
```
L1 = q * log(b1/3) + (1 - q) * log(b2/3) = -log(3)*q - log(6)*(1 - q)
L2 = q * log(q) + (1 - q) * log(1 - q)
L = L1 - L2
```
The maximum of L is at q = 2/3 and Q is
```
0.667 0.334 0.00
```
and the exact answer was
```
0.615 0.308 0.077
```
L at maximum is -0.693 which is an approximation to log(E) =
-0.613. And the approximation is lower as the name suggests.