import math

t = 0.4
i = 0
while True:
    print("%.2f" % t)
    if i == 4:
        break
    i += 1
    L1 = t * (1 - t)
    L2 = t/2 * (1 - t/2)
    C = L1/(L1 + L2)
    t = -(math.sqrt(C*C+8*C)-C-4)/4
