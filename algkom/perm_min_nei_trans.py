# Zadanie 3. (4* pkt.)
# Zaimplementuj algorytm generowanie permutacji
# przez minimalną liczbę transpozycji sąsiednich
# elementów (Algorytm 3) (4* pkt.).


p = list('1234')
n = len(p)
c = []
pr = []
for i in range(0, len(p)):
    c.append(1)
    pr.append(True)
c[len(p)-1] = 0
print(p)
i = 1

while i < n:
    print(i, n)
    i = 1
    x = 0
    while c[i-1] == n - i + 1:
        pr[i-1] = not pr[i-1]
        c[i-1] = 1
        if pr[i-1]:
            x += 1
        i += 1
    if i < n:
        if pr[i-1]:
            k = c[i-1] + x
        else:
            k = n - i + 1 - c[i-1] + x
        tmp = p[k-1]
        p[k-1] = p[k + 1 - 1]
        p[k + 1 - 1] = tmp
        print(f"zamiana indeksów {k-1} :=: {k + 1 - 1}")
        print(p)
        c[i-1] = c[i-1] + 1
