import math

t = 0.4
i = 0
while True:
    print("%.2f" % round(t, 2), end=' ')
    if i == 4:
        break
    i += 1
    L1 = t * (1 - t)
    L2 = t / 2 * (1 - t / 2)
    C = L1 / (L1 + L2)
    t = (C + 4 - math.sqrt(C * C + 8 * C)) / 4
print('')
