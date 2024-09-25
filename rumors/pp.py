import random
import matplotlib.pyplot as plt

random.seed(12345)
tend = 50
r, g = 100, 1000  # rabbit, grass
kr, krg, kg = 1, 0.002, 1
Trace = []
t = 0
while True:
    Trace.append((t, r, g))
    if t >= tend or r == 0:
        break
    a = kr * r, krg * r * g, kg * g
    i, = random.choices([0, 1, 2], a)
    if i == 0:
        r -= 1
    elif i == 1:
        r += 1
        g -= 1
    else:
        g += 1
    tau = random.expovariate(sum(a))
    t += tau
t, r, g = zip(*Trace)
plt.axis((None, tend, None, None))
plt.step(t, r, t, g, where='post')
plt.show()
