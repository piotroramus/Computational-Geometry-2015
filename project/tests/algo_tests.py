__author__ = 'piotr'

from project.io import read_from_file
from project.Point import Point


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
    assert result1 == [p22, p23, p32, p33]

    # single point
    result2 = searching_function(points, 0, 0, 0, 0)
    assert result2 == [p00]

    # square outside the set
    result3 = searching_function(points, 5, 6, 5, 6)
    assert result3 == []

    # all points
    result4 = searching_function(points, -10, 10, -10, 10)
    assert result4 == points

    # rectangle intersecting set
    result5 = searching_function(points, 1, 5, 2.5, 4)
    assert result5 == [p13, p23, p33]

    # rectangle intersecting set
    result6 = searching_function(points, 0.8, 1.2, -1, 1.87)
    assert result6 == [p10, p11]

    # square containing one point
    result7 = searching_function(points, 1.5, 2.5, 2.5, 3.5)
    assert result7 == [p23]

    # invalid input
    result8 = searching_function(points, 3, 1, 1, 1)
    assert result8 == []

    # invalid input
    result9 = searching_function(points, 3, 1, 4, 1)
    assert result9 == []

    # vertical line
    result10 = searching_function(points, 1, 1, 1, 4)
    assert result10 == [p11, p12, p13]

    # horizontal line
    result11 = searching_function(points, -2, 2, 0, 0)
    assert result11 == [p00, p10, p20]