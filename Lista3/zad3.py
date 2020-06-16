#!/usr/bin/python

import sys
from time import time
from random import uniform, randint

maze = []
start_x = 0
start_y = 0

def walk_path(path):
    global maze, start_x, start_y
    x = start_x
    y = start_y
    counter = 0
    for i in range(len(path)):
        counter += 1
        if path[i] == 'U':
            y -= 1
        elif path[i] == 'D':
            y += 1
        elif path[i] == 'L':
            x -= 1
        elif path[i] == 'R':
            x += 1
        if maze[y][x] == '8' or maze[y][x] == '1':
            break
    if maze[y][x] == '8':
        return [True, counter]
    else:
        return [False, counter]

def mark_path(path):
    global maze, start_x, start_y
    x = start_x
    y = start_y
    for i in range(len(path)):
        maze[y][x] = '|'
        if path[i] == 'U':
            y -= 1
        elif path[i] == 'D':
            y += 1
        elif path[i] == 'L':
            x -= 1
        elif path[i] == 'R':
            x += 1
    for row in maze:
        print(row)

def mutate(path):
    steps = ['U', 'D', 'R', 'L']
    index = randint(0, len(path)-1)
    step = steps[randint(0, len(steps)-1)]
    steps.remove(step)
    while step == path[index]:
        step = steps[randint(0,len(steps)-1)]
        steps.remove(step)
    return path[:index] + step + path[index+1:]

def find_min_path(start, t, pop):
    start = sorted(start, key=lambda x: len(x))
    cur_min_path = start[0]
    cur_min = len(cur_min_path)
    t_start = time()
    population = start.copy()
    while time() - t_start < t:
        indices = [i for i in range(len(population))]
        parents = []
        while len(indices) > 1:
            a = indices[randint(0, len(indices)-1)]
            b = indices[randint(0, len(indices)-1)]
            while b == a:
                b = indices[randint(0, len(indices)-1)]
            parents.append((a,b))
            indices.remove(a)
            indices.remove(b)
        for p in parents:
            d = 0
            if randint(0, 1) == 1:
                d = p[0]
            else:
                d = p[1]
            k = randint(0, min(len(population[p[0]]), len(population[p[1]]))-1)
            l = randint(0, min(len(population[p[0]]), len(population[p[1]]))-1)
            c = population[d][:k] + population[p[0]+p[1]-d][k:]
            if uniform(0, 1) < 0.1:
                c = mutate(c)
            f = population[d][:k] + population[p[0]+p[1]-d][k:l] + population[d][l:]
            if uniform(0, 1) < 0.1:
                f = mutate(f)
            if c not in population:
                population.append(c)
            v = walk_path(c)
            if v[0] and v[1] < cur_min:
                cur_min = v[1]
                cur_min_path = c[:v[1]]
            if f not in population:
                population.append(f)
            v = walk_path(f)
            if v[0] and v[1] < cur_min:
                cur_min = v[1]
                cur_min_path = f[:v[1]]
        if len(population) > pop:
            for path in population:
                if not walk_path(path)[0]:
                    population.remove(path)
            if len(population) > pop:
                population = sorted(population, key=lambda path: walk_path(path)[1])
                population = population[:pop]
    return (cur_min_path, cur_min)

def main():
    arg = sys.stdin.read()
    arg = arg.split('\n')
    arg[0] = arg[0].split()
    t = int(arg[0][0])
    n = int(arg[0][1])
    s = int(arg[0][3])
    p = int(arg[0][4])
    global maze, start_x, start_y
    for i in range(1, n+1):
        arg[i] = arg[i].strip('\n')
        if arg[i].find('5') != -1:
            start_y = i-1
            start_x = arg[i].find('5')
        maze.append(list(arg[i]))
    start = []
    for i in range(n+1, n+s+1):
        start.append(arg[i].strip('\n'))
    ret = find_min_path(start, t, p)
    print(ret[1])
    print(ret[0], file=sys.stderr)
    
if __name__ == '__main__':
    main()