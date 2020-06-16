#!/usr/bin/python3

import sys
import random
import time

e = []

def func(x):
    out = 0
    for i in range(5):
        out += e[i]*(abs(x[i]))**(i+1)
    return out

def find_min(t, x_start):
    glob_min = func(x_start)
    glob_min_x = x_start.copy()
    alpha = 0.7
    beta = 2
    eta = 0.4
    swarm = [[random.uniform(-5, 5) for _ in range(5)] for _ in range(20)]
    v = [[random.uniform(-0.5, 0.5) for _ in range(5)] for _ in range(20)]
    loc_min = [func(x) for x in swarm]
    loc_min_x = [x.copy() for x in swarm]
    start = time.time()
    while time.time() - start < t:
        i = 0
        while i < len(swarm):
            moving = False
            for x in v[i]:
                if x > 0:
                    moving = True
            if not moving:
                swarm.pop(i)
                v.pop(i)
            else:
                i += 1
        for i in range(len(swarm)):
            val = func(swarm[i])
            if val < glob_min:
                glob_min = val
                glob_min_x = swarm[i].copy()
            if val < loc_min[i]:
                loc_min[i] = val
                loc_min_x[i] = swarm[i].copy()
        for i in range(len(swarm)):
            for j in range(5):
                b = random.uniform(0, beta)
                n = random.uniform(0, eta)
                v[i][j] = alpha*v[i][j] + b*(loc_min_x[i][j]-swarm[i][j]) + n*(glob_min_x[j] - swarm[i][j])
        for i in range(len(swarm)):
            for j in range(5):
                swarm[i][j] += v[i][j]
    glob_min_x.append(glob_min)
    return glob_min_x

def main():
    arg = sys.stdin.read()
    arg = arg.strip("\n")
    arg = arg.split()
    for i in range(len(arg)):
        arg[i] = float(arg[i])
    global e
    e = arg[6:]
    ret = find_min(arg[0], arg[1:6])
    for x in ret:
        print(format(x, ".16f"), end=" ")
    print()

if __name__ == '__main__':
    main()