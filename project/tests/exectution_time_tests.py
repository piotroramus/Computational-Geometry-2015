import time
from project.kdtree import KDTree
from project.io import generate_points
from copy import deepcopy
from project.simple_algorithms import *
from project.tests.algo_tests import the_same_points

__author__ = 'piotr'


def test():
    points = generate_points(10000, -100, 100, -100, 100)

    points1 = deepcopy(points)
    points2 = deepcopy(points)
    points3 = deepcopy(points)

    area = -100, 10, 5, 8

    start = time.time()
    res1 = linear_searching(points1, *area)
    end = time.time()
    print("Linear searching: " + str(end - start) + "s")

    start = time.time()
    res2 = linear_searching_with_sort(points2, *area)
    end = time.time()
    print("Linear searching with sorting: " + str(end - start) + "s")

    start = time.time()
    kdtree = KDTree()
    kdtree.from_points_recursively(points3)
    # res3 = kdtree.query_test_signature(points3, *area)
    start2 = time.time()
    res3 = kdtree.query(*area)
    end = time.time()
    print("KDTree searching with tree building: " + str(end - start) + "s")
    print("KDTree searching on already built tree: " + str(end - start2) + "s")

    assert the_same_points(res1, res2)
    assert the_same_points(res2, res3)
