from bisect import bisect_left, bisect_right

__author__ = 'piotr'


def linear_searching(points, x1, x2, y1, y2):

    result = []
    for p in points:
        if x1 <= p[0] <= x2 and y1 <= p[1] <= y2:
            result.append(p)

    return result


def linear_searching_with_sort(points, x1, x2, y1, y2):
    result = []
    points = sorted(points)
    points_x = [p[0] for p in points]

    index1 = bisect_left(points_x, x1)
    index2 = bisect_right(points_x, x2)

    points = points[index1:index2]
    for p in points:
        if y1 <= p[1] <= y2:
            result.append(p)

    return result