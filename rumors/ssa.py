import random
import matplotlib.pyplot as plt

random.seed(12345)
N = 100
X, Y, Z = N, 1, 0  # ignorants, spreaders, and stiflers
tend = 0.2

Trace = []
t = 0
while True:
    Trace.append((t, X, Y, Z))
    if t >= tend or Y == 0:
        break
    a = X * Y, Y * (Y - 1) / 2 if Y > 1 else 0, Y * Z
    i, = random.choices([0, 1, 2], a)
    if i == 0:
        X -= 1
        Y += 1
    elif i == 1:
        Y -= 2
        Z += 2
    elif i == 2:
        Y -= 1
        Z += 1
    tau = random.expovariate(sum(a))
    t += tau

t, X, Y, Z = zip(*Trace)
plt.axis((None, tend, None, None))
plt.step(t, X, t, Y, where='post')
plt.show()
