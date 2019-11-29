
"""
Zadanie 2 (3* pkt.) Zaimplementuj rekurencyjną wersje algorytmu generowania wszystkich podziałów zbioru {1, 2, ..., n}
"""


def run():
    global n
    global k
    codeword = [1 for digit_index in range(0, n)]
    while True:
        print(codeword)
        codeword = get_codeword(codeword, n - 1)


def get_codeword(codeword, start_index):
    global n
    global k
    maxValue = max(codeword[0 : start_index])
    if codeword[start_index] > maxValue:
        codeword[start_index] = 1
        codeword = get_codeword(codeword, start_index - 1)
    else:
        if maxValue <= k and codeword[start_index] < k:
            codeword[start_index] += 1
        else:
            codeword[start_index] = 1
            codeword = get_codeword(codeword, start_index - 1)
    return codeword


n, k = 4, 4
try:
    run()
except Exception:
    pass
