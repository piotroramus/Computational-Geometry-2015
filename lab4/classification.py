__author__ = 'piotr'

from lab4.orient import tuple_orient as orient


(STARTING, ENDING, CONNECTING, DIVIDING, CORRECT) = (0, 1, 2, 3, 4)


def classify(points):

    if len(points) < 3:
        raise ValueError("Classification needs at least 3 points")

    # max_y = max(points, key=lambda p: p[1])


