from math import fabs

from project.Point import Point

__author__ = 'piotr'


class QuadTree(object):
    def __init__(self, boundary):
        super().__init__()
        self.boundary = boundary
        self.point = None
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None

    def from_points(self, points):
        pass

    def query(self, x1, x2, y1, y2):
        pass

    def insert(self, point):
        if not self.boundary.contains(point):
            return False
        if not self.point and not self.NW:
            self.point = point
            return True
        if not self.NW:
            self.subdivide()

        if self.NW.insert(point):
            return True
        if self.NE.insert(point):
            return True
        if self.SW.insert(point):
            return True
        if self.SE.insert(point):
            return True

        raise RuntimeError("Cannot insert point for some reason")

    def subdivide(self):

        self.NW, self.NE, self.SW, self.SE = self.boundary.subdivide()
        self.insert(self.point)
        self.point = None


class Boundary(object):
    def __init__(self, x1, x2, y1, y2):
        super().__init__()
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def center(self):
        return fabs(self.x2 - self.x1), fabs(self.y2 - self.y1)

    def contains(self, point):
        return self.x1 <= point.x <= self.x2 and self.y1 <= point.y <= self.y2

    def corners(self):
        return [Point(self.x1, self.y1), Point(self.x1, self.y2),
                Point(self.x2, self.y1), Point(self.x2, self.y2)]

    def intersects(self, boundary):
        for corner in self.corners():
            if boundary.contains(corner):
                return True
        return False

    def subdivide(self):
        center_x, center_y = self.center()
        NWBoundary = Boundary(self.x1, center_x, center_y, self.y2)
        NEBoundary = Boundary(center_x, self.x2, center_y, self.y2)
        SWBoundary = Boundary(self.x1, center_x, self.y1, center_y)
        SEBoundary = Boundary(center_x, self.x2, self.y1, center_y)
        NW = QuadTree(NWBoundary)
        NE = QuadTree(NEBoundary)
        SW = QuadTree(SWBoundary)
        SE = QuadTree(SEBoundary)
        return NW, NE, SW, SE
