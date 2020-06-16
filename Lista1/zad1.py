#!/usr/bin/env python3

from math import cos
import sys
import random
import time

def happy_cat(x_vector):
    len = 0
    sum = 0
    for x in x_vector:
        len += x**2
        sum += x
    factor1 = ((len-4)**2)**0.125
    factor2 = 0.25*(0.5*len+sum)+0.5
    return factor1 + factor2

def griewank(x_vector):
    sum = 0
    product = 1
    for i in range(0,4):
        sum += x_vector[i]**2/4000
        product *= cos(x_vector[i]/(i+1)**0.5)
    return 1+sum-product


def generate_start(x,y):
    x_vector = []
    random.seed()
    for _ in range(0, 4):
        x_vector.append(random.uniform(x, y))
    return x_vector

def generate_neighbours(x_vector, radius):
    neighborhood = []
    n_sub = []
    n_add = []
    for i in range(0,4):
        new_x = x_vector.copy()
        n_sub.append(x_vector[i]-radius)
        n_add.append(x_vector[i]+radius)
        new_x[i] -= radius
        neighborhood.append(new_x)
        new_x[i] += radius
        neighborhood.append(new_x)
    neighborhood.append(n_sub)
    neighborhood.append(n_add)
    return neighborhood


def find_minimum(t, b):
    start_time = time.time()
    if b:
        start_x = generate_start(-10.0, 10.0)
        current_min = griewank(start_x)
    else:
        start_x = generate_start(-2.0,2.0)
        current_min = happy_cat(start_x)
    basic_rad = 0.1
    rad = 0.1
    j = 0
    while time.time() - start_time < t:
        temp = generate_start(min(start_x), max(start_x))
        if b:
            n_val = griewank(temp)
        else:
            n_val = happy_cat(temp)
        if n_val < current_min:
            current_min = n_val
            start_x = temp.copy()
        neighborhood = generate_neighbours(start_x, rad)
        for x in neighborhood:
            if b:
                n_val = griewank(x)
            else:
                n_val = happy_cat(x)
            if n_val < current_min:
                current_min = n_val
                start_x = x.copy()
                if rad > 0.0001:
                    rad /= 4
                j = 0
            else:
                j += 1
        if j > 10:
            j = basic_rad
    start_x.append(current_min)
    return start_x

def main():
    arg = sys.stdin.read()
    arg = arg.strip("\n")
    arg = arg.split()
    ret = find_minimum(int(arg[0]), int(arg[1]))
    for x in ret:
        print(format(x, ".16f"), end=" ")
    print()

if __name__ == "__main__":
    main()

