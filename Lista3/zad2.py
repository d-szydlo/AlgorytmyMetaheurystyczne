#!/usr/bin/python

import sys
from time import time
from random import randint, uniform

dictionary = []
multiset = []
values = {}

def read_dict():
    global dictionary
    dictionary = [[] for _ in range(26)]
    with open('dict.txt', 'r') as f:
        for line in f:
            word = line.lower().strip('\n')
            index = ord(word[0])-97
            dictionary[index].append(word)

def evaluate(word):
    global values
    val = 0
    for ch in word:
        val += values[ch]
    return val

def mutate(word):
    global multiset
    index = randint(0, len(word)-1)
    letter = multiset[randint(0, len(multiset)-1)]
    while word[index] == letter:
        letter = multiset[randint(0, len(multiset)-1)]
    return word[:index] + letter + word[index+1:]

def get_additional():
    out = ['' for _ in range(5)]
    global multiset
    for i in range(5):
        for _ in range(len(multiset)*3//4):
            out[i] += multiset[randint(0, len(multiset)-1)]
    return out

def find_word(t, start):
    cur_max = 0
    cur_max_w = None
    for word in start:
        v = evaluate(word)
        if v > cur_max:
            cur_max = v
            cur_max_w = word
    population = start.copy()
    population += get_additional()
    s_time = time()
    while time() - s_time < t:
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
            v = evaluate(c)
            if v >= cur_max and verify(c):
                cur_max = v
                cur_max_w = c
            if f not in population:
                population.append(f)
            v = evaluate(f)
            if v >= cur_max and verify(f):
                cur_max = v
                cur_max_w = f
        if len(population) > 200:
            for word in population:
                if not verify(word):
                    population.remove(word)
            if len(population) > 200:
                population = sorted(population, key=lambda word: evaluate(word), reverse=True)
                population = population[:201]
    print(population)
    return cur_max_w

def verify(word):
    global dictionary
    index = ord(word[0])-97
    if word not in dictionary[index]:
        return False
    global multiset
    mult = multiset.copy()
    for c in word:
        if c in mult:
            mult.remove(c)
        else:
            return False
    return True

def main():
    read_dict()
    arg = sys.stdin.read()
    arg = arg.split("\n")
    arg.pop(-1)
    for i in range(len(arg)):
        arg[i] = arg[i].split()
    t = int(arg[0][0])
    n = int(arg[0][1])
    s = int(arg[0][2])
    start = []
    global multiset, values
    for i in range(1, n+1):
        if arg[i][0] not in multiset:
            values[arg[i][0]] = int(arg[i][1])
        multiset.append(arg[i][0])
    for i in range(n+1, n+s+1):
        start.append(arg[i][0])
    ret = find_word(t, start)
    print(evaluate(ret))
    print(ret, file=sys.stderr)

if __name__ == '__main__':
    main()