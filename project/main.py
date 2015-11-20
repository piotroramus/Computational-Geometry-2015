from project.Point import Point
from project.kdtree import KDTree
from project.tests.algo_tests import test

def linear_searching(points, x1, x2, y1, y2):

    result = []
    for p in points:
        if x1 <= p.x <= x2 and y1 <= p.y <= y2:
            result.append(p)

    return result


if __name__ == "__main__":
    # test(linear_searching)

    p1 = Point(3, 1)
    p2 = Point(2, 3)
    p3 = Point(2, 1)
    p4 = Point(2, 4)
    p5 = Point(4, 3)
    p6 = Point(6, 1)
    p7 = Point(4, 5)

    points = [
              p1, p2, p3,
              p4, p5, p6, p7
              ]
    kdtree = KDTree()
    kdtree.from_points(points)
    kdtree.print()