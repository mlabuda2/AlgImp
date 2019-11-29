# Zadanie na 3 pkt (bez przeszukiwania -2)
# Budowanie KDTree
import csv
import matplotlib
matplotlib.use('QT4agg')
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return "<" + repr(self.x) + ", " + repr(self.y) + ">"


class Node(object):
    def __init__(self, id, left, right):
        self.id = id
        self.left = left
        self.right = right

    def __repr__(self):
        return "Node id: %s" % (self.id)


def traverse(rootnode):
    thislevel = [rootnode]
    depth, p = 0, 0
    a = ' ' * 170
    while thislevel:
        nextlevel = []
        a = a[:len(a) // 2]
        for n in thislevel:
            if isinstance(n.id, Point):
                print(a + str(n.id), end='')
                p += 1
            else:
                print(a + 'l' + str(depth) + a, end='')
                depth += 1

            if n.left:
                nextlevel.append(n.left)
            if n.right:
                nextlevel.append(n.right)
            thislevel = nextlevel
        print("\n")


# Calculating median
def median(P):
    length = len(P)
    if length % 2 == 0:
        return Point(P[(length // 2) - 1].x, P[(length // 2) - 1].y)
    else:
        return Point(P[length // 2].x, P[length // 2].y)


def compare(a, b, attr):
    if attr == 'x':
        return True if a.x > b.x else False
    elif attr == 'y':
        return True if a.y > b.y else False


def buildKDTree(points_x, points_y, depth=0, label='l'):
    p_right = []
    p_left = []

    if points == []:
        return

    if depth % 2 == 0:
        med = median(points_x)
        print("Dividing by x axis with median: ", med.x, med.y)
        for it in points_x:
            p_right.append(it) if compare(it, med, 'x') is True else p_left.append(it)

    else:
        med = median(points_y)
        print("Dividing by y axis with median: ", med.x, med.y)
        for it in points_y:
            p_right.append(it) if compare(it, med, 'y') is True else p_left.append(it)

    p_right_x = sorted(p_right, key=lambda x: x.x)
    p_right_y = sorted(p_right, key=lambda x: x.y)
    p_left_x = sorted(p_left, key=lambda x: x.x)
    p_left_y = sorted(p_left, key=lambda x: x.y)
    # print(p_right_x)
    # print(p_right_y)
    # print(p_left_x)
    # print(p_left_y)

    label += str(depth)
    node = Node(label, None, None)
    if (len(p_left) == 1) & (len(p_right) == 1):
        node.left, node.right = Node(Point(p_left[0].x, p_left[0].y), None, None), Node(Point(p_right[0].x, p_right[0].y), None, None)
    elif len(p_left) == 1:
        node.left = Node(Point(p_left[0].x, p_left[0].y), None, None)
        node.right = buildKDTree(p_right_x, p_right_y, depth + 1)
    elif len(p_right) == 1:
        node.right = Node(Point(p_right[0].x, p_right[0].y), None, None)
        node.left = buildKDTree(p_left_x, p_left_y, depth + 1)
    else:
        node.left = buildKDTree(p_left_x, p_left_y, depth + 1)
        node.right = buildKDTree(p_right_x, p_right_y, depth + 1)
    return node


points = []
with open('points2.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        points.append(Point(int(row['x']), int(row['y'])))

x, y = [], []
for p in points:
    x.append(p.x)
    y.append(p.y)

plt.axis([0, 40, 0, 40])
plt.grid()
plt.scatter(x, y)
plt.show()

points_x = sorted(points, key=lambda x: x.x)
points_y = sorted(points, key=lambda x: x.y)
print("Sorted x: ", points_x)
print("Sorted y: ", points_y)
root = buildKDTree(points_x, points_y, 0)
print(root)
traverse(root)
