import random
import matplotlib.pyplot as plt

random.seed(6)
tend = 100
G, R, F = 1000, 1000, 100  # Grass, Rabbit, Fox
alpha = 0.001
beta = 0.002
gamma = 1
delta = 1
epsilon = 0.5
Trace = []
t = 0
while True:
    Trace.append((t, G, R, F))
    if t >= tend or G == 0 or R == 0 or F == 0:
        break
    a = alpha * R * G, beta * R * F, gamma * F, delta * G, epsilon * G
    i, = random.choices([0, 1, 2, 3, 4], a)
    if i == 0:
        G -= 1
        R += 1
    elif i == 1:
        R -= 1
        F += 1
    elif i == 2:
        F -= 1
    elif i == 3:
        G += 1
    elif i == 4:
        G -= 1
    tau = random.expovariate(sum(a))
    t += tau
t, G, R, F = zip(*Trace)
plt.axis((None, tend, None, None))
plt.step(t, G, 'green', t, R, 'blue', t, F, 'red', where='post')
plt.savefig('grf.png')
