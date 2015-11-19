__author__ = 'piotr'


class KDTree(object):
    """2-dimensional kd-tree"""
    def __init__(self):
        super().__init__()

    def create(self, points):
        pass

    def query(self, x1, x2, y1, y2):
        pass


class KDNode(object):
    """Node of 2-dimensional KDTree"""
    def __init__(self, point, index):
        super().__init__()
        self.point = point
        self.index = index

    def coord_at_index(self, index):
        if index == 0:
            return self.point.x
        return self.point.y

    def __eq__(self, other):
        return self.point == other.point

    def __lt__(self, other):
        return self.coord_at_index(self.index) < other.coord_at_index(self.index)
