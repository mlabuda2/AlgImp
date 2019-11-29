"""
Zadanie 1 (2* pkt.) Skonstruuj i zaimplementuj algorytm znajdujący wszystkie k-elementowe kompozycje liczby n.
"""


def generate_composition(t=2, s=2):
    q = [0] * (t + 1)
    r = None
    q[0] = s
    while True:
        if 0 not in q:  # jeśli chcemy również kompozycje z zerami to zakomentować
            yield q
        if q[0] == 0:
            if r == t:
                break
            else:
                q[0] = q[r] - 1
                q[r] = 0
                r = r + 1
        else:
            q[0] = q[0] - 1
            r = 1
        q[r] = q[r] + 1


for x in generate_composition(2, 5):
    print(x)
