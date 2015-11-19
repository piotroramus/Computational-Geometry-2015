__author__ = 'piotr'

from project.tests.algo_tests import test


def linear_searching(points, x1, x2, y1, y2):

    result = []
    for p in points:
        if x1 <= p.x <= x2 and y1 <= p.y <= y2:
            result.append(p)

    return result


if __name__ == "__main__":
    test(linear_searching)