__author__ = 'piotr'


class Point(object):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self, *args, **kwargs):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __repr__(self, *args, **kwargs):
        return self.__str__(*args, **kwargs)