from project.Point import Point
from project.kdtree import KDTree
from project.quadtree import QuadTree, Boundary
from project.tests.algo_tests import test
from project.tests.execution_time_tests import test as execution_time_test


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
    # kdtree.from_points_recursively(points)
    kdtree.from_points_with_indices(points)
    # kdtree.print()

    # print(kdtree.query(1, 5, 0.5, 3.4))

    # test(kdtree.query_test_signature)

    # while True:
    #     execution_time_test()

    execution_time_test()

    # TODO: increase bounds
    # minbound = -1.0e2
    # maxbound = 1.0e2
    # boundary = Boundary(minbound, maxbound, minbound, maxbound)
    # qtree = QuadTree(boundary)
    # qtree.from_points(points)
    # qtree.print()

    # print(qtree.query(2, 3, 2, 3))
    # test(qtree.query_test_signature)

