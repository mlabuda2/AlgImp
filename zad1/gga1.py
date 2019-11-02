import matplotlib
matplotlib.use('QT4agg')
import matplotlib.pyplot as plt

import csv
import numpy as np
from operator import attrgetter
from shapely.geometry import LineString, Polygon
from shapely.geometry import Point as PointShapely
import traceback
import sys

class Point:
    def __init__(self, x, y, is_corner=None, is_kernel_point=None):
        self.x, self.y = x, y
        self.is_kernel_corner = is_corner
        self.is_kernel_point = is_kernel_point

    def __repr__(self):
        if self.is_kernel_corner:
            return "<Kernel Corner " + repr(self.x) + ", " + repr(self.y) + ">"
        elif self.is_kernel_point:
            return "<Kernel Point " + repr(self.x) + ", " + repr(self.y) + ">"
        else:
            return "<Point " + repr(self.x) + ", " + repr(self.y) + ">"


def is_orientation_right(cur, cons, prec):
    mat = np.array([[cons.x, cons.y ,1], [cur.x, cur.y, 1], [prec.x, prec.y, 1]])
    if(np.linalg.det(mat) > 0):
        return True
    else:
        return False


def is_maximum(cur, cons, prec):
    if((cur.y > cons.y) & (cur.y > prec.y)):
        return True
    else:
        return False


def is_minimum(cur, cons, prec):
    if((cur.y < cons.y) & (cur.y < prec.y)):
        return True
    else:
        return False


def find_kernel_points(verticies):
    kernel_indexes = []
    for i, vertex in enumerate(verticies):
        if vertex.is_kernel_corner:
            kernel_indexes.append(i)

    kernel_points = verticies[kernel_indexes[0]:kernel_indexes[1]+1] + verticies[kernel_indexes[2]:kernel_indexes[3]+1]
    print(kernel_points)
    return kernel_points


def find_corners_and_points(verticies, min_num, max_num):
    min_y = min_num.y  # y kolca minimum
    max_y = max_num.y  # y kolca maximum
    min_x = min(verticies, key=attrgetter('x')).x
    max_x = max(verticies, key=attrgetter('x')).x
    # corners = []
    verticies = list(verticies)
    verticies.append(verticies[0])
    for v in range(0, len(verticies)-1):
        added = 0
        line1 = LineString([(verticies[v].x, verticies[v].y), (verticies[v+1].x, verticies[v+1].y)])  # odcinek każdy po kolei
        line2 = LineString([(min_x, max_y), (max_x, max_y)])  # stała max_y
        obj = line1.intersection(line2)  # przecięcie linii
        if isinstance(obj, PointShapely):
            add = True
            for vert in verticies:
                if vert.x == obj.x and vert.y == obj.y:
                    add = False
                    vert.is_kernel_point = True
            if add:
                # sprawdź czy to nie maximum
                if not (obj.x == max_num.x and obj.y == max_num.y):
                    idx_to_insert = v + 1 + added
                    verticies = verticies[:idx_to_insert] + [Point(obj.x, obj.y, is_kernel_point=True)] + verticies[idx_to_insert:]
                    added += 1
                    # corners.append(Point(obj.x, obj.y))
    for v in range(0,len(verticies)-1):
        added = 0
        line1 = LineString([(verticies[v].x, verticies[v].y), (verticies[v+1].x, verticies[v+1].y)])
        line2 = LineString([(min_x, min_y), (max_x, min_y)])  # stała min_y
        obj = line1.intersection(line2)  # przecięcie linii
        if isinstance(obj, PointShapely):
            print("Przecięcie:", obj.x, obj.y)
            add = True
            for vert in verticies:
                if vert.x == obj.x and vert.y == obj.y:
                    add = False
                    vert.is_kernel_point = True
            if add:
                if not (obj.x == min_num.x and obj.y == min_num.y):
                    idx_to_insert = v + 1 + added
                    verticies = verticies[:idx_to_insert] + [Point(obj.x, obj.y, is_kernel_point=True)] + verticies[idx_to_insert:]
                    added += 1
                    # corners.append(Point(obj.x, obj.y))
    verticies.pop()
    return verticies


def mark_kernel_corners(verticies, min_num, max_num):
    min_y = min_num.y  # y kolca minimum
    max_y = max_num.y  # y kolca maximum
    verticies = list(verticies)
    maximum_point_with_min_x = None
    maximum_point_with_max_x = None
    minimum_point_with_min_x = None
    minimum_point_with_max_x = None
    kernel_points_list_on_maximum_line = []
    kernel_points_list_on_minimum_line = []
    for vert in verticies:
        if vert.is_kernel_point:
            if vert.y == min_y:
                kernel_points_list_on_minimum_line.append(vert)
            elif vert.y == max_y:
                kernel_points_list_on_maximum_line.append(vert)

    left_minimum_kernel_corner = min(kernel_points_list_on_minimum_line, key=attrgetter('x'))
    right_minimum_kernel_corner = max(kernel_points_list_on_minimum_line, key=attrgetter('x'))
    left_minimum_kernel_corner.is_kernel_corner = True
    right_minimum_kernel_corner.is_kernel_corner = True

    left_maximum_kernel_corner = min(kernel_points_list_on_maximum_line, key=attrgetter('x'))
    right_maximum_kernel_corner = max(kernel_points_list_on_maximum_line, key=attrgetter('x'))
    left_maximum_kernel_corner.is_kernel_corner = True
    right_maximum_kernel_corner.is_kernel_corner = True

    return verticies

def calculate_area(kernel_verticies):
    list_vertex = []
    for vertex in kernel_verticies:
        list_vertex.append((vertex.x, vertex.y))
    print(list_vertex)
    print("Pole: ", Polygon(list_vertex).area)
    # https://www.mathopenref.com/coordpolygonarea.html


def calculate_perimeter(kernel_verticies):
    list_vertex = []
    for vertex in kernel_verticies:
        list_vertex.append((vertex.x, vertex.y))
    print(list_vertex)
    print("Obwód: ", Polygon(list_vertex).length)


verticies = []
maximas = []
minimas = []
coord = []

with open('points3.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        verticies.append(Point(float(row['x']),float(row['y'])))
        coord.append([float(row['x']), float(row['y'])])

coord.append(coord[0])  # close polygon
xs, ys = zip(*coord)  # create lists of x and y values

########################################
for v in range(0,len(verticies)):
    cur = Point(verticies[v].x,verticies[v].y)
    if(v == len(verticies)-1):
        conss = Point(verticies[1].x,verticies[1].y)
        cons = Point(verticies[0].x,verticies[0].y)
        prec = Point(verticies[v-1].x,verticies[v-1].y)
        precc = Point(verticies[v-2].x,verticies[v-2].y)
    else:
        if(v == len(verticies)-2):
            conss = Point(verticies[0].x,verticies[0].y)
        else:
            conss = Point(verticies[v+2].x,verticies[v+2].y)
            cons = Point(verticies[v+1].x,verticies[v+1].y)
            prec = Point(verticies[v-1].x,verticies[v-1].y)
            precc = Point(verticies[v-2].x,verticies[v-2].y)

    # checking collinearity
    if(cur.y == prec.y):
        prec = precc
    elif(cur.y == cons.y):
        cons = conss

    if(is_maximum(cur,cons,prec) & is_orientation_right(cur,cons,prec)):
        maximas.append(cur)
    elif(is_minimum(cur,cons,prec) & is_orientation_right(cur,cons,prec)):
        minimas.append(cur)
    else:
        continue

if not minimas and not maximas:
    print("Brak jądra")
    sys.exit(0)
elif len(maximas) == 1:
    print(f"Jądro istnieje i jest to stała y = {maximas[0].y}")
    print(f"Pole wynosi: 0")
    print(f"Obwód wynosi: 0")
    sys.exit(0)

min_num = min(minimas, key=attrgetter('y'))
max_num = max(maximas, key=attrgetter('y'))

# check if kernel exist
if(float(len(minimas)) == 0 or float(len(maximas)) == 0 or min_num.y < max_num.y):
    print("There is no {O}-Kernel, because local minimum is lower placed than local maximum");
else:
    print("Kernel of given polygon is located between below shown points: ")
    print("Minimum:")
    print(min_num.x,min_num.y)
    print("Maximas:")
    print(max_num.x,max_num.y)

verticies = find_corners_and_points(verticies, min_num, max_num)

# plt.figure()
# plt.plot(xs, ys)
# plt.show() # if you need...
kernel_points = mark_kernel_corners(verticies, min_num, max_num)
kernel_points = find_kernel_points(verticies)
print(kernel_points)
calculate_area(kernel_points)
calculate_perimeter(kernel_points)


kernel = []
for c in kernel_points:
    kernel.append([float(c.x), float(c.y)])

kernel.append(kernel[0])  # repeat the first point to create a 'closed loop'
kxs, kys = zip(*kernel)  # create lists of x and y values


# draw
plt.figure()
plt.plot(xs, ys)
plt.plot(kxs, kys)
plt.show()
