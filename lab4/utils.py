__author__ = 'piotr'


def cmp_to_key(custom_cmp):
    """ Convert a cmp= function into a key= function """

    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj

        def __lt__(self, other):
            return custom_cmp(self.obj, other.obj) < 0

        def __gt__(self, other):
            return custom_cmp(self.obj, other.obj) > 0

        def __eq__(self, other):
            return custom_cmp(self.obj, other.obj) == 0

        def __le__(self, other):
            return custom_cmp(self.obj, other.obj) <= 0

        def __ge__(self, other):
            return custom_cmp(self.obj, other.obj) >= 0

        def __ne__(self, other):
            return custom_cmp(self.obj, other.obj) != 0

    return K


def add_point(visualisation, point, color="black"):
    step = {
        "type": "point",
        "value": (point, color)
    }
    visualisation.append(step)


def add_points(visualisation, points, color="black"):
    step = {
        "type": "points",
        "value": (points, color)
    }
    visualisation.append(step)


def add_segment(visualisation, point1, point2, color="black"):
    segment = point1, point2
    step = {
        "type": "line",
        "value": (segment, color)
    }
    visualisation.append(step)


def add_segments(visualisation, segments, color="black"):
    step = {
        "type": "lines",
        "value": (segments, color)
    }
    visualisation.append(step)


class Point(object):
    def __init__(self, point, chain):
        super().__init__()
        self.value = point
        self.chain = chain