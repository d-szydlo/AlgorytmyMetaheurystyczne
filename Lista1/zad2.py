#!/usr/bin/env python3

import sys
from time import time
import random

distances = []

def greedy_approach(n):
    visited = [0]
    current = 0
    route = 0
    global distances
    while len(visited) != n-1:
        closest = -1
        distance = int(max(distances[current]))
        for i in range(0, n):
            if i not in visited:
                if distances[current][i] != 0 and distances[current][i] < distance:
                    distance = distances[current][i]
                    closest = i
        current = closest
        route += distance
        visited.append(current)
    for i in range(1,n):
        if i not in visited:
            visited.append(i)
            route += distances[current][i]
            current = i
    visited.append(0)
    route += distances[current][0]
    result = []
    result.append(visited)
    result.append(route)
    return result
        
def get_route(path,n):
    route = 0
    for i in range(0,n):
        route += distances[path[i]][path[i+1]]
    return route

def generate_swap(n):
    random.seed()
    i = random.randint(1,n-1)
    j = random.randint(1, n-1)
    while i == j:
        j = random.randint(1, n-1)
    return [i,j]


def tsp(t, n):
    start_time = time()
    tabu = []
    ttl = (n-1)*(n-2)//6
    #ttl = n*n
    if ttl == 0:
        ttl = 1
    start = greedy_approach(n)
    current = start[0]
    min_route = start[1]
    min_path = start[0]
    counter = 0
    while time() - start_time < t:
        if counter < 10:
            swap = generate_swap(n)
            c1 = current[swap[0]]
            c2 = current[swap[1]]
            while [c1, c2] in tabu:
                swap = generate_swap(n)
                c1 = current[swap[0]]
                c2 = current[swap[1]]
        else:
            frequency = []
            i = 0
            while i < n:
                frequency.append(0)
                i += 1
            for x in tabu:
                frequency[x[0]] += 1
                frequency[x[1]] += 1
            c1 = min(frequency)
            frequency.remove(c1)
            c2 = min(frequency)
            swap = [current.index(c1), current.index(c2)]
        if len(tabu) == ttl:
            tabu.pop(0)
        tabu.append([c1, c2])
        temp = current.copy()
        temp[swap[0]], temp[swap[1]] = temp[swap[1]], temp[swap[0]]
        temp_r = get_route(temp, n)
        if temp_r < min_route:
            min_route = temp_r
            min_path = temp.copy()
            counter = 0
        else:
            counter += 1
    for city in min_path:
        print(city, end=" ", file=sys.stderr)
    print(min_route)

def main():
    args = sys.stdin.readline()
    args = args.split()
    args[0] = int(args[0])
    args[1] = int(args[1])
    global distances
    for line in sys.stdin:
        line = line.split()
        row = []
        for num in line:
            row.append(int(num))
        distances.append(row)
    tsp(args[0], args[1])


if __name__ == "__main__":
    main()