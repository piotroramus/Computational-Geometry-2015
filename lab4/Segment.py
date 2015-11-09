__author__ = 'piotr'


class Segment(object):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __repr__(self, *args, **kwargs):
        return self.__str__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        p1 = "(" + str(self.x1) + "," + str(self.y1) + ")"
        p2 = "(" + str(self.x2) + "," + str(self.y2) + ")"
        return p1 + "->" + p2

    def max_point(self):
        if self.y1 > self.y2:
            return self.x1, self.y1
        return self.x2, self.y2

    def min_x(self):
        if self.x1 < self.x2:
            return self.x1
        return self.x2

    def max_y(self):
        if self.y1 > self.y2:
            return self.y1
        return self.y2
