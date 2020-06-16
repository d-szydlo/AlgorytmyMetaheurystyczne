#!/usr/bin/env python3

import sys
from time import time
from random import randint, uniform
from numpy import exp

#funkcja odleglosci miedzy macierzami
def distance(m1, m2):
    distance = 0
    n = len(m1)
    m = len(m1[0])
    for i in range(n):
        for j in range(m):
            distance += (m1[i][j] - m2[i][j])**2
    distance *= 1/(n*m)
    return distance

#funckja generujaca x0 - szachownice o blokach kxk o wartosciach 0 i 255
def generate_start(n, m, k):
    x0 = []
    prev = 0
    i = 0
    j = 0
    while i < n:
        row = []
        if i >= n-n%k:
            val = prev
        else:
            if i%(2*k) >= k:
                val = 255
                prev = 255
            else:
                val = 0
                prev = 0
        while j < m:
            row.append(val)
            j += 1
            if not j >= m-m%k and j%k == 0:
                if val == 0:
                    val = 255
                else:
                    val = 0
        j = 0
        i += 1
        x0.append(row)
    return x0

#funkcja generujaca tablice podzialow poczatkowej macierzy na bloki
#kazdy rzad tablicy podzialow ma tyle elementow ile jest blokow w danym rzedzie, analogicznie jest z kolumnami
#elementy natomiast to tablice, ktore trzymaja wymiary danego bloku oraz jego kolor
def generate_start_div(n, m, k):
    div = [[[k,k,0] for _ in range(m//k)] for _ in range(n//k)]
    for i in range(n//k):
        div[i][-1][1] += m%k
    for i in range(m//k):
        div[-1][i][0] += n%k
    val = 0
    for row in div:
        for i in range(len(row)):
            row[i][2] = val
            if val == 0:
                val = 255
            else:
                val = 0
    return div

#funckja zmieniajaca kolor bloku w y-tej kolumnie i x-tym rzedzie na kolor color
def color_block(matrix, div, color, x, y):
    i = 0
    j = 0
    for k in range(x):
        i += div[k][y][0]
    for k in range(y):
        j += div[x][k][1]
    for _ in range(div[x][y][0]):
        for _ in range(div[x][y][1]):
            matrix[i][j] = color
            j += 1
        j -= div[x][y][1]
        i += 1
    return matrix

#funkcja, ktora dla kazdego bloku w biezacej rozpatrywanej macierzy zmienia jego wartosc na wszyskie inne mozliwe i sprawdza czy odleglosc sie zmniejsza
#wraca macierz ze zmieniona wartoscia jednego bloku, ktorej odleglosc od macierzy wyjsciowej jest najmniejsza
def check_colors(matrix, div, curr_matrix, curr_min):
    values = [0, 32, 64, 128, 160, 223, 255]
    #kopiowanie biezacej macierzy
    m1 = [[curr_matrix[i][j] for j in range(len(curr_matrix[0]))] for i in range(len(curr_matrix))]
    ret = []
    for i in range(len(div)): #dla kazdego rzedu blokow macierzy
        for j in range(len(div[i])): #dla kazdego bloku w rzedzie
            curr = div[i][j][2]
            values.remove(curr) #usuwanie biezacego koloru bloku z listy kolorow do sprawdzenia
            for val in values:
                m1 = color_block(m1, div, val, i, j) #zmiana koloru na aktualnie sprawdzany
                dis = distance(matrix, m1)
                if dis < curr_min: #jezeli odleglosc ze zmienionym kolorem jest mniejsza od biezacego minimum to kopiujemy do returna
                    ret = [[m1[k][m] for m in range(len(m1[k]))] for k in range(len(m1))]
            values.append(curr) #uzupelniamy tablice mozliwych kolorow
            m1 = [[curr_matrix[i][j] for j in range(len(curr_matrix[0]))] for i in range(len(curr_matrix))] #kolorujemy blok na pierwotny kolor
    return ret

#funckja losujaca blok o conajmniej jednym wymiarze wiekszym niz k, zmniejszajaca go i transferujaca dodatkowy rozmiar do sasiedniego bloku
def check_size(curr_matrix, k, div):
    bigger = []
    block = []
    neigh = []
    for i in range(len(div)):
        for j in range(len(div[0])):
            if div[i][j][0] > k or div[i][j][1] > k:
                bigger.append([i,j]) #generowanie tablicy z blokami spelniajacymi warunek wymiar > k
    if_ok = False
    while not if_ok:
        if len(bigger) == 0:
            break
        index = randint(0, len(bigger)-1) #losowanie bloku
        block = bigger[index]
        if div[block[0]][block[1]][0] > k: #w zaleznosci od tego czy manipulujemy wysokoscia czy szerokoscia wybieramy odpowiednie parametry
            #parametry jezeli zmniejszamy liczbe kolumn
            num = div[block[0]][block[1]][1] #liczba wierszy w bloku
            a = 1 #promien w pionie
            b = 0 #promien w poziomie
            edge = 1 #trzeba sprawdzic czy sasiad ma taka sama liczbe wierszy co wybrany blok
        else:
            #parametry jezeli zmniejszamy liczbe kolumn
            num = div[block[0]][block[1]][0]
            a = 0
            b = 1
            edge = 0
        try:
            #sprawdzamy sasiadow bloku wedlug wczesniej ustalonych parametrow
            if div[block[0]+a][block[1]+b][edge] == num:
                neigh = [block[0]+a, block[1]+b, a] #jezeli sasiad spelnia warunki kopiujemy jego wspolrzedne i flage ktorym wymiarem sie zajmujemy
                if_ok = True #znalezlismy rozwiazanie, wiec mozna wyjsc z while'a
        except:
            pass
        try:
            #sprawdzanie drugiego sasiada
            if div[block[0]-a][block[1]-b][edge] == num:
                neigh = [block[0]-a, block[1]-b, a]
                if_ok = True
        except:
            pass
        if not if_ok:
            #jezeli blok nie spelnia warunkow zdejmujemy go z listy
            bigger.pop(index)
    if len(neigh) == 0:
        #jezeli zaden z blokow nie spelnia warunkow to wracamy -1
        return [-1]
    #kopiowanie biezacej macierzy
    m1 = [[curr_matrix[i][j] for j in range(len(curr_matrix[0]))] for i in range(len(curr_matrix))]
    #kopiowanie biezacego podzialu
    div1 = [[div[i][j] for j in range(len(div[i]))] for i in range(len(div))]
    #w zaleznosci od tego czy modyfikujemy kolumny czy wiersze losujemy ich liczbe do przekazania i modyfikujemy podzial
    if neigh[2] == 1:
        transfer = randint(1, div1[block[0]][block[1]][0]-k)
        div1[block[0]][block[1]][0] -= transfer
        div1[neigh[0]][neigh[1]][0] += transfer
    else:
        transfer = randint(1, div1[block[0]][block[1]][1]-k)
        div1[block[0]][block[1]][1] -= transfer
        div1[neigh[0]][neigh[1]][1] += transfer
    #przemalowujemy blok, ktory dostal dodatkowe pola
    m1 = color_block(m1, div1, div1[neigh[0]][neigh[1]][2], neigh[0], neigh[1])
    return [m1, div1]

#funkcja wybierajaca dwa bloki o tej samej wysokosci z tego samego wiersza i zamienia je miejscami 
def check_swap(curr_matrix, div):
    if_ok = False
    #lista wierszy do sprawdzenia
    to_check = [i for i in range(len(div))]
    swap1 = []
    swap2 = []
    while not if_ok:
        if len(to_check) == 0:
            break
        row_id = randint(0, len(to_check)-1) #losowanie numeru wiersza do sprawdzenia
        col_id = randint(0, len(div[row_id])-1) #losowanie elementu z wiersza
        pos = []
        for i in range(len(div[row_id])):
            if div[row_id][i][0] == div[row_id][col_id][0] and i != col_id: #jezeli jest inny element w tym wierszu o tej samej wysokosci to dodajemy go do listy mozliwych
                pos.append(i)
        if len(pos) != 0:
            neigh = randint(0, len(pos)-1) #losujemy jeden z blokow spelniajacyh warunek
            swap1 = [row_id, col_id] #wspolrzedne pierwszego bloku
            swap2 = [row_id, pos[neigh]] #wspolrzedne drugiego bloku
            if_ok = True
        to_check.pop(row_id) #usuwamy dany wiersz z listy wierszy do sprawdzenia
    if len(swap1) == 0:
        return [-1]
    m1 = [[curr_matrix[i][j] for j in range(len(curr_matrix[0]))] for i in range(len(curr_matrix))] #kopiowanie biezacej macierzy
    div1 = [[div[i][j] for j in range(len(div[i]))] for i in range(len(div))] #kopiowanie biezacego podzialu
    temp = div1[swap1[0]][swap1[1]][1]
    div1[swap1[0]][swap1[1]][1] = div1[swap2[0]][swap2[1]][1] #zamiana rozmiarow blokow
    div1[swap2[0]][swap2[1]][1] = temp
    for i in range(len(div1[swap1[0]])):
        m1 = color_block(m1, div1, div1[swap1[0]][i][2],swap1[0], i) #przekolorowanie wiersza
    return [m1, div1]

def find_closest(t, n, m, k, matrix, c, t0):
    x = generate_start(n, m, k) #generowanie pierwszego rozwiazania
    div = generate_start_div(n,m,k) #generowanie pierwszej tablicy podzialow odpowiadajacej poczatkowemu x
    curr_min = distance(matrix, x) #przypisanie aktualnego dystansu do biezacego minimum
    initial = curr_min #zapisanie pierwotnego dystansu
    curr_min_x = [[x[i][j] for j in range(len(x[i]))] for i in range(len(x))] #przypisanie rozwiazania poczatkowego do biezacego minimum
    temp = t0 #temperatura poczatkowa
    start = time()
    while time() - start < t and temp > 0:
        color = check_colors(matrix, div, x, curr_min) #dla kazdego bloku jest sprawdzana odleglosc po pokolorowaniu go na kazdy inny mozliwy kolor
        if color == []: #jezeli nie udalo sie znalezc czegos lepszego niz biezace minimum to ustawiamy dystans na poczatkowy
            color_val = initial
        else:
            color_val = distance(matrix, color)
        size = check_size(x, k, div) #losowanie jednego bloku o ktoryms wymiarze wiekszym niz k i zmniejszenie go ze zwiekszeniem sasiada
        if size[0] == -1: #jezeli nie ma bloku o wymiarze >k to ustawiamy dystans na poczatkowy
            size_val = initial
        else:
            size_val = distance(matrix, size[0])
        swap = check_swap(x, div) #losowanie dwoch blokow o tej samej wysokosci i zamiana ich miejscami
        if swap[0] == -1: #jezeli w zadnym wierszu nie ma blokow o tej samej wysokosci to ustawiamy dystans na poczatkowy
            swap_val = initial
        else:
            swap_val = distance(matrix, swap[0])
        #szukamy minimum z powyzszych sasiadow
        if color_val <= size_val and color_val <= swap_val:
            min_n = [[color[i][j] for j in range(len(color[i]))] for i in range(len(color))]
            div_n = [[div[i][j] for j in range(len(div[i]))] for i in range(len(div))]
            val_n = color_val
        elif size_val <= color_val and size_val <= swap_val:
            min_n = [[size[0][i][j] for j in range(len(size[0][i]))] for i in range(len(size[0]))]
            div_n = [[size[1][i][j] for j in range(len(size[1][i]))] for i in range(len(size[1]))]
            val_n = size_val
        else:
            min_n = [[swap[0][i][j] for j in range(len(swap[0][i]))] for i in range(len(swap[0]))]
            div_n = [[swap[1][i][j] for j in range(len(swap[1][i]))] for i in range(len(swap[1]))]
            val_n = swap_val
        if val_n < curr_min:
            curr_min_x = [[min_n[i][j] for j in range(len(min_n[i]))] for i in range(len(min_n))]
            curr_min = val_n
            x = [[min_n[i][j] for j in range(len(min_n[i]))] for i in range(len(min_n))]
            div = [[div_n[i][j] for j in range(len(div_n[i]))] for i in range(len(div_n))]
        else:
            #tu wchodzi SA
            num = exp(-1*(val_n - curr_min)/temp)
            r = uniform(0.0, 1.0)
            if num > r:
                x = [[min_n[i][j] for j in range(len(min_n[i]))] for i in range(len(min_n))]
                div = [[div_n[i][j] for j in range(len(div_n[i]))] for i in range(len(div_n))]
        temp *= c
    return [curr_min_x, curr_min]

def main():
    arg = sys.stdin.read()
    arg = arg.split("\n")
    for i in range(len(arg)):
        arg[i] = arg[i].split()
    for line in arg:
        for i in range(len(line)):
            line[i] = int(line[i])
    arg.pop(-1)
    m = find_closest(arg[0][0], arg[0][1], arg[0][2], arg[0][3], arg[1:], 0.8, 100)
    print(m[1])
    for row in m[0]:
        for num in row:
            print(num, end=" ", file=sys.stderr)
        print("", file=sys.stderr)
    
if __name__ == "__main__":
    main()
    