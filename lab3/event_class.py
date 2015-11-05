__author__ = 'piotr'

from utils import epsilon


def event_a_lt_b(a, b):
    return a.x - b.x < -epsilon or (abs(a.x - b.x) <= epsilon and a.y - b.y < -epsilon)


class Event(object):
    def __init__(self, event_type, point, segment1, segment2):
        self.event_type = event_type
        self.point = point
        self.segment1 = segment1
        self.segment2 = segment2

    def __lt__(self, other):
        self_lt_other = event_a_lt_b(self.point, other.point)
        self_et_lt_other = self.point == other.point and self.event_type < other.event_type
        return self_lt_other or self_et_lt_other
