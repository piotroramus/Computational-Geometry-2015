__author__ = 'piotr'


class Intersection(object):
    def __init__(self, segment1, segment2, point):
        self.point = point
        self.segment1 = segment1
        self.segment2 = segment2

    def __eq__(self, other):
        eq1 = self.segment1 == other.segment1 and self.segment2 == other.segment2
        eq2 = self.segment1 == other.segment2 and self.segment2 == other.segment1
        return eq1 or eq2

    def __hash__(self):
        return hash(self.segment1) + 31 * hash(self.segment2) + 31 * hash(self.point)