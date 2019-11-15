# A divide and conquer program in Python
# to find the smallest distance from a
# given set of points.
import csv
import math


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return "<Point " + repr(self.x) + ", " + repr(self.y) + ">"


class MinDist:
    def __init__(self, p1, p2, dist):
        self.p1 = p1
        self.p2 = p2
        self.dist = dist


min_dist = MinDist(None, None, None)


# A utility function to find the
# distance between two points
def dist(p1, p2):
    return math.sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y))


# A Brute Force method to return the
# smallest distance between two points
# in list points of size n
def bruteForce(points, n):
    print("Brute: ", points)
    if n == 3:
        points.append(points[0])
    nearest = None
    for pair in zip(points, points[1:]):
        pair_dist = dist(pair[0], pair[1])
        if not nearest or pair_dist < nearest:
            nearest = pair_dist
            print("Nearest: ", pair, pair_dist)
            if not min_dist.dist or nearest < min_dist.dist:
                min_dist.p1 = pair[0]
                min_dist.p2 = pair[1]
                min_dist.dist = nearest
    return nearest


# A utility function to find the
# distance between the closest points of
# strip of given size. All points in
# strip are sorted accordint to
# y coordinate. They all have an upper
# bound on minimum distance as d.
# Note that this method seems to be
# a O(n^2) method, but it's a O(n)
# method as the inner loop runs at most 6 times
def stripClosest(strip, size, d):
    print("Strip: ", strip)
    print("d: ", d)
    minimum = d  # Initialize the minimum distance as d

    # Pick all points one by one and try the next points till the difference
    # between y coordinates is smaller than d.
    # This is a proven fact that this loop runs at most 6 times
    for i in range(size):
        for j in range(1, size):
            if i == j:
                break
            if not ((strip[j].y - strip[i].y) < minimum):
                break
            if (dist(strip[i], strip[j]) < minimum):
                minimum = dist(strip[i], strip[j])
                print("New minimum: ", strip[i], strip[j], minimum)
                if not min_dist.dist or minimum < min_dist.dist:
                    min_dist.p1 = strip[i]
                    min_dist.p2 = strip[j]
                    min_dist.dist = minimum

    return minimum


# A recursive function to find the
# smallest distance. The list points_x contains
# all points sorted according to x coordinate
def closestUtil(points_x, points_y, n):
    # If there are 2 or 3 points, then use brute force
    if (n <= 3):
        return bruteForce(points_x, n)

    # Find the middle point
    mid = n // 2
    mid_point = points_x[mid]

    # Divide points in y sorted array around the vertical line.
    # Assumption: All x coordinates are distinct.
    points_y_l = [point for point in points_y if point.x <= mid_point.x]   # y sorted points on left of vertical line
    points_y_r = [point for point in points_y if point.x > mid_point.x]  # y sorted points on right of vertical line

    # Consider the vertical line passing through the middle point
    # calculate the smallest distance dl on left of middle point and
    # dr on right side
    dl = closestUtil(points_x[:mid], points_y_l, mid)
    dr = closestUtil(points_x[mid:], points_y_r, n - mid)

    # Find the smaller of two distances
    d = min(dl, dr)

    # Build an list strip that contains
    # points close (closer than d)
    # to the line passing through the middle point
    strip = []
    for point in points_y:
        if abs(point.x - mid_point.x) < d:
            strip.append(point)
    j = len(strip)
    # Find the closest points in strip.
    # Return the minimum of d and closest
    # distance is strip
    return min(d, stripClosest(strip, j, d))


# The main function that finds the smallest distance
# This method mainly uses closestUtil()
def closest(points, n):
    points_x = sorted(points, key=lambda p: p.x)
    points_y = sorted(points, key=lambda p: p.y)
    print("Sorted by x: ", points_x)
    print("Sorted by y: ", points_y)
    # Use recursive function closestUtil()
    # to find the smallest distance
    return closestUtil(points_x, points_y, n)


# Driver code
if __name__ == "__main__":
    points = []
    with open('points1.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            points.append(Point(float(row['x']), float(row['y'])))
    print(f"The smallest distance is {closest(points, len(points))} between: {min_dist.p1} and {min_dist.p2}")
