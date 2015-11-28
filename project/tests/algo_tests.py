__author__ = 'piotr'

from project.Point import Point
from copy import deepcopy


def _the_same_points(points1, points2):
    if len(points1) != len(points2):
        return False

    points2 = deepcopy(points2)
    for point in points1:
        if point in points2:
            points2.remove(point)
        else:
            return False
    if points2:
        return False

    return True


def test(searching_function):

    p00 = Point(0, 0)
    p01 = Point(0, 1)
    p02 = Point(0, 2)
    p03 = Point(0, 3)
    p10 = Point(1, 0)
    p11 = Point(1, 1)
    p12 = Point(1, 2)
    p13 = Point(1, 3)
    p20 = Point(2, 0)
    p21 = Point(2, 1)
    p22 = Point(2, 2)
    p23 = Point(2, 3)
    p30 = Point(3, 0)
    p31 = Point(3, 1)
    p32 = Point(3, 2)
    p33 = Point(3, 3)

    points = [p00, p01, p02, p03, p10, p11, p12, p13, p20, p21, p22, p23, p30, p31, p32, p33]

    # small square
    result1 = searching_function(points, 2, 3, 2, 3)
    assert _the_same_points(result1, [p22, p23, p32, p33])

    # single point
    result2 = searching_function(points, 0, 0, 0, 0)
    assert _the_same_points(result2, [p00])

    # square outside the set
    result3 = searching_function(points, 5, 6, 5, 6)
    assert _the_same_points(result3, [])

    # all points
    result4 = searching_function(points, -10, 10, -10, 10)
    assert _the_same_points(result4, points)

    # rectangle intersecting set
    result5 = searching_function(points, 1, 5, 2.5, 4)
    assert _the_same_points(result5, [p13, p23, p33])

    # rectangle intersecting set
    result6 = searching_function(points, 0.8, 1.2, -1, 1.87)
    assert _the_same_points(result6, [p10, p11])

    # square containing one point
    result7 = searching_function(points, 1.5, 2.5, 2.5, 3.5)
    assert _the_same_points(result7, [p23])

    # invalid input
    result8 = searching_function(points, 3, 1, 1, 1)
    assert _the_same_points(result8, [])

    # invalid input
    result9 = searching_function(points, 3, 1, 4, 1)
    assert _the_same_points(result9, [])

    # vertical line
    result10 = searching_function(points, 1, 1, 1, 4)
    assert _the_same_points(result10, [p11, p12, p13])

    # horizontal line
    result11 = searching_function(points, -2, 2, 0, 0)
    assert _the_same_points(result11, [p00, p10, p20])