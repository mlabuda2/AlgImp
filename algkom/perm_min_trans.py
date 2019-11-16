# Globalne: Tablica ∏.
# Wejście: Liczba n.
# Wyjście: Ciąg wszystkich n-elementowych permutacji.


# Funkcja B(n, i):
# 1. Jeżeli n mod 2 = 0 oraz n > 2
#  1.1. Jeżeli i < n - 1
#   1.1.1. B ← i
#  1.2. W przeciwnym razie
#   1.2.1. B ← n - 2
# 2. W przeciwnym razie
#  2.1. B ← n - 1
# 3. Zwróć B
# Program główny:
# 1. i ← 1
# 2. Dopóki i ≤ n
#  2.1. πi ← i
#  2.2. i ← i + 1
# 3. Perm(n)


# PERM(n)
# 1. Jeżeli n = 1
#  1.1. Wypisz(π1, π2, ..., πn)
# 2. W przeciwnym razie
#  2.1. i ← 1
#  2.2. Dopóki i ≤ n
#   2.2.1. Perm(n-1)
#   2.2.2. Jeżeli i < n
#    2.2.2.1. πB(n, i) ↔ πn
#   2.2.3. i ← i + 1

from cprint import cprint


def b_func(n, i):
    cprint.warn(f"B({n},{i})")
    if n % 2 == 0 and n > 2:
        if i < (n - 1):
            cprint.warn(f"return {i}")
            return i
        else:
            cprint.warn(f"return {n - 2}")
            return n - 2
    else:
        cprint.warn(f"return {n - 1}")
        return n - 1


def permutation(n):
    # Jednoelementowa lista
    if n == 1:
        print(data)

    # Lista o len >= 2
    curent_perm = []
    i = 1
    while i <= n:
        permutation(n - 1)
        if i < n:
            # podmiana miejscami
            tmp = data[b_func(n, i) -1]
            data[b_func(n, i) - 1] = data[n - 1]
            data[n - 1] = tmp
        i += 1


data = list('12345')
permutation(len(data))
