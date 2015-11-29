from project.Point import Point
from project.kdtree import KDTree
from project.tests.algo_tests import test
from project.tests.exectution_time_tests import test as execution_time_test

if __name__ == "__main__":

    # test(linear_searching)
    # test(linear_searching_with_sort)

    p1 = Point(3, 1)
    p2 = Point(2, 3)
    p3 = Point(2, 1)
    p4 = Point(2, 4)
    p5 = Point(4, 3)
    p6 = Point(6, 1)
    p7 = Point(4, 5)

    points = [
              p1,
              p2,
              p3,
              p4,
              p5,
              p6,
              p7
              ]

    kdtree = KDTree()
    kdtree.from_points_recursively(points)
    # kdtree.print()

    # print(kdtree.query(1, 5, 0.5, 3.4))

    # test(kdtree.query_test_signature)

    execution_time_test()
