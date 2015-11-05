__author__ = 'piotr'

from primitives import *


def orient(a, b, c):
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)


def dist(a, b):
    return (a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y)


def takeFurthest(points, relativePoint):
    max_dist = dist(relativePoint, points[0])
    max_point = points[0]
    for point in points[1:]:
        current_dist = dist(relativePoint, point)
        if current_dist > max_dist:
            max_dist = current_dist
            max_point = point
    return max_point


def qsort(points, relativePoint, epsilon):
    if not points:
        return []
    else:
        pivot = points[0]
        equals = [x for x in points[1:] if abs(orient(relativePoint, x, pivot)) <= epsilon]
        less   = [x for x in points     if orient(relativePoint, x, pivot) > epsilon]
        more   = [x for x in points[1:] if orient(relativePoint, x, pivot) < -epsilon]
        if equals:
            equals.append(pivot)
            pivot = takeFurthest(equals, relativePoint)
        return qsort(less, relativePoint, epsilon) + [pivot] + qsort(more, relativePoint, epsilon)


def find_min(points):
    min_point = points[0]
    for point in points:
        if point.y < min_point.y:
            min_point = point
        elif point.y == min_point.y:
            if point.x < min_point.x:
                min_point = point
    return min_point


def graham_solver(input_points, epsilon=0):

    if len(input_points) < 3:
        return input_points

    min_point = find_min(input_points)
    input_points.remove(min_point)

    points = qsort(input_points, min_point, epsilon)

    p1 = points.pop(0)
    p1 = Point(p1.x, p1.y, 'r')
    p2 = points.pop(0)
    p2 = Point(p2.x, p2.y, 'r')
    stack = [min_point, p1, p2]

    for current_point in points:
        while orient(stack[-2], stack[-1], current_point) <= epsilon:
            stack.pop()
        stack.append(current_point)

    return stack


def find_point_with_min_angle(points, reference_point, epsilon):
    result = reference_point
    for r in points:
        t = orient(reference_point, result, r)
        if t < epsilon or (abs(t) <= epsilon) and dist(reference_point, r) > dist(reference_point, result):
            result = r
    return result


def jarvis_solver(input_points, epsilon=0):

    if len(input_points) < 3:
        return input_points

    min_point = find_min(input_points)
    stack = [min_point]
    next_point = find_point_with_min_angle(input_points, stack[0], epsilon)
    stack.append(next_point)

    while next_point != stack[0]:
        next_point = find_point_with_min_angle(input_points, stack[-1], epsilon)
        stack.append(next_point)

    return stack