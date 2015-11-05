# coding=utf-8

from __future__ import division
from lab3.utils import epsilon
from lab3.point import Point


def line_from_segment(p1, p2):
    A = (p1.y - p2.y)
    B = (p2.x - p1.x)
    C = (p1.x*p2.y - p2.x*p1.y)
    return A, B, -C


def get_intersection_point(segment1, segment2):

    L1 = line_from_segment(segment1.point1, segment1.point2)
    L2 = line_from_segment(segment2.point1, segment2.point2)
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return Point(x, y)
    else:
        return False


def orient(a, b, c):
    d = (c.y - a.y)*(b.x - a.x) - (b.y - a.y)*(c.x - a.x)
    return 1 if d > epsilon else (-1 if d < -epsilon else 0)


def intersects(segment1, segment2):

    a = segment1.point1
    b = segment1.point2
    c = segment2.point1
    d = segment2.point2

    if a == b:
        return a == c or a == d
    if c == d:
        return c == a or c == b

    s1 = orient(a, b, c)
    s2 = orient(a, b, d)

    # No touching and on the same side
    if s1 and s1 == s2:
        return False

    s1 = orient(c, d, a)
    s2 = orient(c, d, b)

    # No touching and on the same side
    if s1 and s1 == s2:
        return False

    return True