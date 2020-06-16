#!/usr/bin/env python3

from math import cos, pi
from numpy import exp
import sys
import random
import time

def salomon(x_vector):
    vec_len = 0 
    for x in x_vector:
        vec_len += x*x
    vec_len **= 0.5
    return 1-cos(2*pi*vec_len)+0.1*vec_len

def generate_start(x,y):
    x_vector = []
    random.seed()
    for _ in range(4):
        x_vector.append(random.uniform(x, y))
    return x_vector

def generate_neighbour(x_vector):
    random.seed()
    n = []
    add =random.uniform(-0.5, 0.5)
    for x in x_vector:
        n.append(x+add)
    return n

def find_minimum(t, x_vector, t0, c):
    start_time = time.time()
    current_min = salomon(x_vector)
    curr_min_vec = x_vector.copy()
    temp = t0
    while time.time() - start_time < t and temp > 0:
        #n_vector = generate_start(min(x_vector), max(x_vector))
        #n_val = salomon(n_vector)
        y_vector = generate_neighbour(x_vector)
        y_val = salomon(y_vector)
        #if n_val < y_val and n_val != current_min:
        #    y_vector = n_vector.copy()
        #    y_val = n_val
        if y_val < current_min:
            current_min = y_val
            curr_min_vec = y_vector.copy()
            x_vector = y_vector.copy()
        else:
            x_val = salomon(x_vector)
            num = exp(-1*(y_val - x_val)/temp)
            r = random.uniform(0.0, 1.0)
            if num > r:
                x_vector = y_vector.copy()
        temp *= c
    curr_min_vec.append(current_min)
    return curr_min_vec

def main():
    arg = sys.stdin.read()
    arg = arg.strip("\n")
    arg = arg.split()
    for i in range(len(arg)):
        arg[i] = float(arg[i])
    ret = find_minimum(arg[0], arg[1:], 100, 0.75)
    for x in ret:
        print(format(x, ".16f"), end=" ")
    print()

if __name__ == "__main__":
    main()
