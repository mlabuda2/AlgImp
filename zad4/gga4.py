"""
Zadanie 2. (5 pkt.) Zaimplementuj algorytm rozwiązujący problem
prostokątnej gałęzi Steinera w pierwszej ćwiartce płaszczyzny ℝ2
wykorzystując programowanie dynamiczne (4,5 pkt.).
Implementacja powinna mieć złożoność czasową rzędu O(3n),
gdzie n jest liczbą punktów pierwszej ćwiartki płaszczyzny.
Przetestuj eksperymentalnie jego złożoność obliczeniową
(wykonaj pomiar czasu działania zaimplementowanego algorytmu) (0,5 pkt.).
"""

from operator import itemgetter, attrgetter
import matplotlib
matplotlib.use('QT4agg')
import matplotlib.pyplot as plt
import timeit

class Point():
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.met = self.x + self.y

    def __repr__(self):
        return("(%s,%s)") % (self.x, self.y)

    def __str__(self):
        return("(%s,%s)") % (self.x, self.y)


class MPoint():
    def __init__(self, x, y):
        if(get_met(x) == get_met(y)):
            self.P = x if x.x < y.x else y
            self.Q = y if x.x < y.x else x
        else:
            self.P = x if get_met(x) < get_met(y) else y
            self.Q = y if get_met(x) < get_met(y) else x

        self.merge = Point(min(self.P.x, self.Q.x), min(self.P.y, self.Q.y))
        self.met = get_met(self.merge)
        self.cost = get_cost(self.P, self.Q)

    def __repr__(self):
        return("(%s,%s)" % (self.merge.x, self.merge.y))


def get_met(a):
    return a.x + a.y


def get_cost(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def rsa(points):
    merges = []
    while (len(points) > 1):
        bMerge = MPoint(points[0], points[1])
        for i in range(0, len(points)):
            for j in range(i + 1, len(points)):
                merged = MPoint(points[i], points[j])
                if((merged.met >= bMerge.met) and (merged.cost < bMerge.cost)):
                    bMerge = merged
        merges.append(bMerge)
        idx = points.index(bMerge.Q)
        del points[idx]
        idx2 = points.index(bMerge.P)
        points[idx2] = bMerge.merge

    return merges


def draw(points, merges):
    x, y = [], []
    x = [p.x for p in points]
    y = [p.y for p in points]
    plt.scatter(x, y, color='blue')
    for m in merges:
        print((m.merge.x, m.P.x), (m.merge.y, m.P.y))
        print((m.merge.x, m.Q.x), (m.merge.y, m.Q.y))
        plt.plot((m.merge.x, m.P.x), (m.merge.y, m.P.y), 'b')
        plt.plot((m.merge.x, m.Q.x), (m.merge.y, m.Q.y), 'r')

    plt.plot((merges[-1].merge.x, merges[-1].merge.x), (merges[-1].merge.y, 0), 'b')
    plt.plot((merges[-1].merge.x, 0), (0, 0), 'b')
    plt.grid()
    plt.show()


def run(points):
    # sort by met
    points_core = list(points)
    points.sort(key=attrgetter('met'), reverse=True)
    merge_points = rsa(points)
    draw(points_core, merge_points)
    return ''

# points = [Point(4,7),Point(7,7),Point(3,4),Point(5,4),Point(7,4),Point(5,2),Point(9,2)]
# points = [Point(0,8), Point(1,7), Point(2,6), Point(3,5),Point(4,4),Point(5,3),Point(6,2), Point(7,1)]
points = [Point(2, 2), Point(2, 5), Point(7, 2), Point(4, 9), Point(5, 4), Point(6, 6)]
# for _ in range(1000):
#     start = timeit.timeit()
#     run(points)
#     end = timeit.timeit()
#     print(end - start)
run(points)