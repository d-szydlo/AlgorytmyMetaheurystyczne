#!/usr/bin/env python3

import sys
from time import time
import random

maze = []
start_x = 0
start_y = 0

def find_wall():
    global start_x, start_y
    route = []
    x = start_x
    y = start_y
    while maze[y][x] != "1" and maze[y][x] != "8":
        y += 1
        route.append("D")
    if maze[y][x] != "8":
        y -= 1
        route.pop()
        while maze[y][x] != "1" and maze[y][x] != "8" and maze[y+1][x] != "8":
            x += 1
            route.append("R")
        if maze[y+1][x] == "8":
            route.append("D")
        elif maze[y][x] == "8":
            x -= 1
        else:
            x -= 1
            route.pop()
            while maze[y][x] != "1" and maze[y][x] != "8" and maze[y][x+1] != "8":
                y -= 1
                route.append("U")
            if maze[y][x+1] == "8":
                route.append("R")
            elif maze[y][x] == "8":
                x -= 1
            else:
                y += 1
                route.pop()
                while maze[y][x] != "1" and maze[y][x] != "8" and maze[y-1][x] != "8":
                    x -= 1
                    route.append("L")
                if maze[y-1][x] == "8":
                    route.append("U")
                elif maze[y][x] == "8":
                    x -= 1
                else:
                    x += 1
                    route.pop()
                    while maze[y][x] != "1" and maze[y][x] != "8" and maze[y][x-1] != "8":
                        y += 1
                        route.append("D")
                    if maze[y][x-1] == "8":
                        route.append("L")
                    elif maze[y][x] == "8":
                        x -= 1
                    else:
                        y -= 1
                        route.pop()
                        while maze[y][x] != "1" and maze[y][x] != "8" and maze[y+1][x] != "8":
                            x += 1
                            route.append("R")
                        route.append("D")
    return route

def walk_path(path):
    global start_x, start_y
    x = start_x
    y = start_y
    counter = 0
    for i in range(0,len(path)):
        counter += 1
        if path[i] == "U":
            y -= 1
        elif path[i] == "D":
            y += 1
        elif path[i] == "L":
            x -= 1
        elif path[i] == "R":
            x += 1
        if maze[y][x] == "8" or maze[y][x] == "1":
            break
    if maze[y][x] == "8":
        return [True, counter]
    else:
        return [False, counter]

def generate_neighborhood(path, ttl):
    random.seed()
    neighborhood = []
    for _ in range(0, ttl-1):
        j = random.randint(0, len(path)-1)
        k = random.randint(0, len(path)-1)
        temp = path.copy()
        temp[j], temp[k] = temp[k], temp[j]
        neighborhood.append(temp)
    return neighborhood


def find_route(t, n, m):
    current_path = find_wall()
    current_min = len(current_path)
    start_time = time()
    tabu = [current_path]
    ttl = (current_min-1)*(current_min-2)//6
    if ttl == 0:
        ttl = 1
    while time()-start_time < t:
        neighborhood = generate_neighborhood(current_path, ttl)
        for neighbour in neighborhood:
            if neighbour not in tabu:
                ret = walk_path(neighbour)
                if ret[0]:
                    if ret[1] < current_min:
                        current_min = ret[1]
                        neighbour = neighbour[:ret[1]]
                        current_path = neighbour.copy()
                if len(tabu) > ttl:
                    tabu.pop(0)
                tabu.append(neighbour)
    print(current_min)
    print("".join(current_path), file = sys.stderr)

def main():
    global maze, start_x, start_y
    args = sys.stdin.readline()
    args = args.split()
    args[0] = int(args[0])
    args[1] = int(args[1])
    args[2] = int(args[2])
    y = 0
    for line in sys.stdin:
        line = line.strip("\n")
        if line.find("5") != -1:
            start_y = y
            start_x = line.find("5")
        maze.append(line)
        y += 1
    find_route(args[0], args[1], args[2])

if __name__ == "__main__":
    main()