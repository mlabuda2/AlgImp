# Globalne: Tablica ∏.
# Wejście: Liczba n.
# Wyjście: Ciąg wszystkich n-elementowych permutacji.
# 1. Jeżeli n = 1
#  1.1. Wypisz(π1, π2, ..., πn)
# 2. W przeciwnym razie
#  2.1. i ← 1
#  2.2. Dopóki i ≤ n
#   2.2.1. Perm(n-1)
#   2.2.2. Jeżeli i < n
#    2.2.2.1. πB(n, i) ↔ πn
#   2.2.3. i ← i + 1
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


def permutation(lst):
    # Pusta lista
    if len(lst) == 0:
        return []
    # Jednoelementowa lista
    if len(lst) == 1:
        return [lst]

    # Lista o len >= 2
    curent_perm = []

    for i in range(len(lst)):
        m = lst[i]
        # Extract lst[i] or m from the list.  remLst is
        # remaining list
        remaining_list = lst[:i] + lst[i + 1:]

        # Generating all permutations where m is first
        # element
        for p in permutation(remaining_list):
            curent_perm.append([m] + p)
    return curent_perm


# Driver program to test above function
data = list('123')
for p in permutation(data):
    print(p)