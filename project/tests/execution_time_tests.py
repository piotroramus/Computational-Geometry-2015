import time
from project.kdtree import KDTree
from project.io import generate_points
from copy import deepcopy

from project.quadtree import QuadTree, Boundary
from project.simple_algorithms import *
from project.tests.algo_tests import the_same_points

__author__ = 'piotr'


def test():
    points = generate_points(1000, -100, 100, -100, 100)

    points1 = deepcopy(points)
    points2 = deepcopy(points)
    points3 = deepcopy(points)
    points4 = deepcopy(points)
    points5 = deepcopy(points)
    points6 = deepcopy(points)

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
    kdtree.construct_balanced_slow(points3)
    start2 = time.time()
    res3 = kdtree.query(*area)
    end = time.time()
    print("KDTree searching with (slow) balanced tree building: " + str(end - start) + "s")
    print("KDTree searching on already built tree: " + str(end - start2) + "s")

    start = time.time()
    kdtree = KDTree()
    kdtree.construct_balanced(points4)
    start2 = time.time()
    res4 = kdtree.query(*area)
    end = time.time()
    print("KDTree searching with balanced tree building: " + str(end - start) + "s")
    print("KDTree searching on already built tree: " + str(end - start2) + "s")

    start = time.time()
    kdtree = KDTree()
    kdtree.construct_unbalanced(points5)
    start2 = time.time()
    res5 = kdtree.query(*area)
    end = time.time()
    print("KDTree searching with unbalanced tree building: " + str(end - start) + "s")
    print("KDTree searching on already built tree: " + str(end - start2) + "s")

    start = time.time()
    boundary = Boundary(-1.0e6, 1.0e6, -1.0e6, 1.0e6)
    qtree = QuadTree(boundary)
    qtree.from_points(points6)
    start2 = time.time()
    res6 = qtree.query(*area)
    end = time.time()
    print("QuadTree searching with tree building: " + str(end - start) + "s")
    print("QuadTree searching on already built tree: " + str(end - start2) + "s")

    assert the_same_points(res1, res2)
    assert the_same_points(res1, res3)
    assert the_same_points(res1, res4)
    assert the_same_points(res1, res5)
    assert the_same_points(res1, res6)
