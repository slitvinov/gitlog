import math

def sol_min(al):
    return -(math.sqrt(al*al+8*al)-al-4)/4

def L1(t):
    return t * (1 - t)

def L2(t):
    return t/2 * (1 - t/2)

t0 = 0.4
i = 0
while True:
    print("%.2f" % t0)
    if i == 4:
        break
    i += 1
    C1 = L1(t0)/(L1(t0) + L2(t0))
    C2 = L2(t0)/(L1(t0) + L2(t0))
    C1 = C1/(C1 + C2)
    t0 = sol_min(C1)
    
