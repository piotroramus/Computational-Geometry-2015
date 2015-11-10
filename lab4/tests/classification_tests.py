__author__ = 'piotr'

from lab4.classification import *


def test_classification():

    point = (2, 5)
    previous_point = (1, 0)
    next_point = (0, 2)
    category = classify_point(point, previous_point, next_point)
    assert category == STARTING

    point = (2, 4)
    previous_point = (4, 2)
    next_point = (0, 0)
    category = classify_point(point, previous_point, next_point)
    assert category == STARTING

    point = (2, 2)
    previous_point = (4, 0)
    next_point = (0, 0)
    category = classify_point(point, previous_point, next_point)
    assert category == STARTING

    point = (3, 0)
    previous_point = (0, 4)
    next_point = (5, 2)
    category = classify_point(point, previous_point, next_point)
    assert category == ENDING

    point = (3, 0)
    previous_point = (0, 3)
    next_point = (5, 5)
    category = classify_point(point, previous_point, next_point)
    assert category == ENDING

    point = (3, 0)
    previous_point = (0, 2)
    next_point = (5, 2)
    category = classify_point(point, previous_point, next_point)
    assert category == ENDING

    point = (3, 0)
    previous_point = (6, 2)
    next_point = (0, 3)
    category = classify_point(point, previous_point, next_point)
    assert category == CONNECTING

    point = (0, 0)
    previous_point = (2, 2)
    next_point = (2, 6)
    category = classify_point(point, previous_point, next_point)
    assert category == CONNECTING

    point = (2, 0)
    previous_point = (4, 2)
    next_point = (0, 2)
    category = classify_point(point, previous_point, next_point)
    assert category == CONNECTING

    point = (3, 3)
    previous_point = (0, 0)
    next_point = (6, 1)
    category = classify_point(point, previous_point, next_point)
    assert category == DIVIDING

    point = (2, 4)
    previous_point = (0, 3)
    next_point = (4, 0)
    category = classify_point(point, previous_point, next_point)
    assert category == DIVIDING

    point = (0, 3)
    previous_point = (2, 6)
    next_point = (3, 0)
    category = classify_point(point, previous_point, next_point)
    assert category == CORRECT

    point = (0, 3)
    previous_point = (2, 5)
    next_point = (3, 0)
    category = classify_point(point, previous_point, next_point)
    assert category == CORRECT

    point = (2, 2)
    previous_point = (0, 0)
    next_point = (0, 4)
    category = classify_point(point, previous_point, next_point)
    assert category == CORRECT

    point = (0, 2)
    previous_point = (2, 0)
    next_point = (3, 3)
    category = classify_point(point, previous_point, next_point)
    assert category == CORRECT

    point = (3, 7)
    previous_point = (0, 0)
    next_point = (0, 11)
    category = classify_point(point, previous_point, next_point)
    assert category == CORRECT
