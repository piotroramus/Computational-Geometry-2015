__author__ = 'piotr'


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other:
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return "("+str(self.x)+", " + str(self.y) + ")"

    def __hash__(self):
        return hash(self.x) + 31 * hash(self.y)