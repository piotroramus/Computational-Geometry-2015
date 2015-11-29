__author__ = 'piotr'

import random
from project.Point import Point


def generate_points(n, min_x, max_x, min_y, max_y):

    points = []

    for i in range(n):
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)
        points.append(Point(x, y))

    return points


def read_from_file(filename):

    points = []
    with open(filename, 'r') as f:
        for line in f:
            x, y = line.strip().split(",")
            points.append(Point(float(x), float(y)))

    return points


def write_to_file(points, filename):

    with open(filename, 'w') as f:
        for p in points:
            f.write(str(p.x) + "," + str(p.y) + "\n")