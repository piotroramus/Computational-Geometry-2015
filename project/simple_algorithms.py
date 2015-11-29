from bisect import bisect_left, bisect_right

__author__ = 'piotr'


def linear_searching(points, x1, x2, y1, y2):

    result = []
    for p in points:
        if x1 <= p.x <= x2 and y1 <= p.y <= y2:
            result.append(p)

    return result


def linear_searching_with_sort(points, x1, x2, y1, y2):
    result = []
    points = sorted(points, key=lambda p: p.x)
    points_x = [p.x for p in points]

    index1 = bisect_left(points_x, x1)
    index2 = bisect_right(points_x, x2)

    points = points[index1:index2]
    for p in points:
        if y1 <= p.y <= y2:
            result.append(p)

    return result