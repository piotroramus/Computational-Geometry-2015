__author__ = 'piotr'

from lab4.orient import tuple_orient as orient


(STARTING, ENDING, CONNECTING, DIVIDING, CORRECT) = (0, 1, 2, 3, 4)

category_description = {
    STARTING: "STARTING",
    ENDING: "ENDING",
    CONNECTING: "CONNECTING",
    DIVIDING: "DIVIDING",
    CORRECT: "CORRECT"
}

category_color = {
    STARTING: "green",
    ENDING: "red",
    CONNECTING: "blue",
    DIVIDING: "cyan",
    CORRECT: "brown"
}


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

    classification = []

    #classify starting point
    current_point = segments[0].point1()
    next_point = segments[0].point2()
    previous_point = segments[-1].point1()
    c = classify_point(current_point, previous_point, next_point)
    classification.append([current_point, c])

    previous_point = segments[0].point1()
    current_point = segments[0].point2()
    for segment in segments[1:]:
        next_point = segment.point2()
        c = classify_point(current_point, previous_point, next_point)
        classification.append([current_point, c])
        previous_point = current_point
        current_point = next_point

    return classification