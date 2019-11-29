from abc import ABC, abstractmethod
import sys


class Utils:
    def __init__(self, elements):
        self.elements = elements

    def change_elements_positions(self, source_index, destination_index):
        temp = self.elements[source_index]
        self.elements[source_index] = self.elements[destination_index]
        self.elements[destination_index] = temp

    def reverse_elements_in_range_m(self, m):
        i = 0
        j = m
        while i < j:
            self.change_elements_positions(i, j)
            i += 1
            j -= 1


class Listener:
    @staticmethod
    def action(data):
        print(data)


class PermutationStrategy(ABC):
    @abstractmethod
    def generate(self, elements, listener):
        pass


class PermutationGenerator:
    def __init__(self, elements, listener):
        self.init_elements = elements
        self.listener = listener
        self.elements = elements

    def generate(self, strategy):
        strategy.generate(self.elements, self.listener)


class MinAdjacentTranspositionStrategy(PermutationStrategy):
    def __init__(self):
        self.elements = []
        self.listener = None

    def generate(self, elements, listener):
        self.elements = elements
        self.listener = listener
        self.generate_m(len(self.elements) - 1)

    def generate_m(self, m):
        c = [0] * (m + 1)
        pr = [True] * m

        self.listener.action(self.elements)
        while True:
            i = 0
            x = 0
            while i < m and c[i] == m - i:
                pr[i] = not pr[i]
                c[i] = 0
                if pr[i]:
                    x += 1
                i += 1
            if i >= m:
                break
            if pr[i]:
                k = c[i] + x
            else:
                k = m - i - 1 - c[i] + x
            utils = Utils(self.elements)
            utils.change_elements_positions(k, k + 1)
            self.listener.action(self.elements)
            c[i] += 1


data = [1, 2, 3, 4]
listener = Listener()
perm = PermutationGenerator(data, listener)
print('generowanie permutacji przez minimalną liczbę transpozycji sąsiednich elementów:')
perm.generate(MinAdjacentTranspositionStrategy())









