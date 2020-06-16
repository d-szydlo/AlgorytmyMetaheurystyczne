#!/usr/bin/env python3

import sys
from time import time
from random import randint, uniform, seed
from numpy import exp
from collections import deque

def generate_start(maze, start_x, start_y):
    visited = [[0 for j in range(len(maze[i]))] for i in range(len(maze))]
    visited[start_x][start_y] = 1
    queue = deque()
    start = [start_x, start_y, []]
    queue.append(start)
    while len(queue) > 0:
        pt = queue.popleft()
        if maze[pt[0]][pt[1]] == "8":
            return pt[2]
        else:
            steps = [(1, 0, "D"), (-1, 0, "U"), (0, 1, "R"), (0, -1, "L")]
            for step in steps:
                x = pt[0] + step[0]
                y = pt[1] + step[1]
                if x > -1 and x < len(maze[0]) and y > -1 and y < len(maze) and maze[x][y] != "1" and visited[x][y] == 0:
                    path = pt[2].copy()
                    path.append(step[2])
                    queue.append([x, y, path])
                    visited[x][y] = 1
    return -1

def walk_path(maze, path, start_x, start_y):
    x = start_x
    y = start_y
    counter = 0
    for i in range(len(path)):
        counter += 1
        if path[i] == "U":
            x -= 1
        elif path[i] == "D":
            x += 1
        elif path[i] == "L":
            y -= 1
        elif path[i] == "R":
            y += 1
        if maze[x][y] == "8" or maze[x][y] == "1":
            break
    if maze[x][y] == "8":
        return [True, counter]
    else:
        return [False, counter]

def mark_path(maze, path, x, y):
    for i in range(len(path)):
        maze[x][y] = "|"
        if path[i] == "U":
            x -= 1
        elif path[i] == "D":
            x += 1
        elif path[i] == "L":
            y -= 1
        elif path[i] == "R":
            y += 1
    for row in maze:
        print(row)

def generate_neighborhood(path, ttl):
    seed()
    neighborhood = []
    for _ in range(ttl):
        j = randint(0, len(path)-1)
        k = randint(0, len(path)-1)
        temp = path.copy()
        temp[j], temp[k] = temp[k], temp[j]
        neighborhood.append(temp)
    return neighborhood

def find_path(maze, t, start_x, start_y, c, t0):
    path = generate_start(maze, start_x, start_y)
    print(path)
    min_path = path.copy()
    curr_len = walk_path(maze, path, start_x, start_y)[1]
    min_len = curr_len
    temp = t0
    start = time()
    while time() - start < t and temp > 0:
        neigh = generate_neighborhood(path, 10)
        min_len = len(maze)*len(maze[0])
        min_n = []
        for n in neigh:
            p = walk_path(maze, n, start_x, start_y)
            if p[0] and p[1] < min_len:
                min_n = n.copy()
                min_len_n = p[1]
        if min_n == []:
            continue
        if min_len_n < min_len:
            min_len = min_len_n
            min_path = min_n.copy()
            path = min_n.copy()
            curr_len = min_len_n
        else:
            num = exp(-1*(min_len_n - min_len)/temp)
            r = uniform(0.0, 1.0)
            if num > r:
                path = min_n.copy()
                curr_len = min_len_n
        temp *= c
    return [min_path, min_len]

def main():
    args = sys.stdin.readline()
    args = args.split()
    args[0] = int(args[0])
    args[1] = int(args[1])
    args[2] = int(args[2])
    y = 0
    maze = []
    for line in sys.stdin:
        line = line.strip("\n")
        if line.find("5") != -1:
            start_y = y
            start_x = line.find("5")
        maze.append(list(line))
        y += 1
    p = find_path(maze, args[0], start_x, start_y, 0.8, 100)
    print(p[1])
    for step in p[0][:p[1]]:
        print(step, end="", file=sys.stderr)
    print("", file=sys.stderr)

if __name__ == "__main__":
    main()