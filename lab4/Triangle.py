__author__ = 'piotr'


class Triangle(object):
    def __init__(self, p1, p2, p3):
        super().__init__()
        self.point1 = p1
        self.point2 = p2
        self.point3 = p3

    def __repr__(self, *args, **kwargs):
        return self.__str__()

    def __str__(self, *args, **kwargs):
        p1 = "(" + str(self.point1[0]) + "," + str(self.point1[1]) + ")"
        p2 = "(" + str(self.point2[0]) + "," + str(self.point2[1]) + ")"
        p3 = "(" + str(self.point3[0]) + "," + str(self.point3[1]) + ")"
        return "[" + p1 + "," + p2 + "," + p3 + "]"