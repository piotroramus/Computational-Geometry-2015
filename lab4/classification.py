__author__ = 'piotr'

from lab4.orient import tuple_orient as orient


(STARTING, ENDING, CONNECTING, DIVIDING, CORRECT) = (0, 1, 2, 3, 4)

point_category = {STARTING: "STARTING",
                  ENDING: "ENDING",
                  CONNECTING: "CONNECTING",
                  DIVIDING: "DIVIDING",
                  CORRECT: "CORRECT"}


def is_below(point, first_point, second_point):
    return point[1] < first_point[1] and point[1] < second_point[1]


def is_above(point, first_point, second_point):
    return point[1] > first_point[1] and point[1] > second_point[1]


def classify_point(point, previous_point, next_point):
    orientation = orient(previous_point, point, next_point)
    if is_below(point, previous_point, next_point):
        if orientation > 0:
            return ENDING
        else:
            return CONNECTING
    elif is_above(point, previous_point, next_point):
        if orientation > 0:
            return STARTING
        else:
            return DIVIDING
    else:
        return CORRECT


def classify(segments):

    if len(segments) < 3:
        raise ValueError("Classification needs at least 3 segments")
