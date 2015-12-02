__author__ = 'piotr'


class Boundary(object):
    def __init__(self, x1, x2, y1, y2):
        super().__init__()
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def center(self):
        return (self.x2 + self.x1)/2, (self.y2 + self.y1)/2

    def contains(self, point):
        return self.x1 <= point[0] <= self.x2 and self.y1 <= point[1] <= self.y2

    def intersects(self, boundary):
        if self.x2 < boundary.x1 or boundary.x2 < self.x1 or\
                    self.y2 < boundary.y1 or boundary.y2 < self.y1:
            return False
        return True

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

    def __repr__(self, *args, **kwargs):
        return self.__str__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return str(self.x1) + ", " + str(self.x2) + ", " + str(self.y1) + ", " + str(self.y2)


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
        for point in points:
            self.insert(point)

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

    def print(self):
        point_str = " with " + str(self.point) if self.point else " with no point"
        print(str(self.boundary) + point_str)
        if self.NW:
            self.NW.print()
            self.NE.print()
            self.SW.print()
            self.SE.print()

    def query_range(self, qrange):
        result = []
        if not self.boundary.intersects(qrange):
            return result

        if self.point and qrange.contains(self.point):
            result.append(self.point)

        if not self.NW:
            return result

        result.extend(self.NW.query_range(qrange))
        result.extend(self.NE.query_range(qrange))
        result.extend(self.SW.query_range(qrange))
        result.extend(self.SE.query_range(qrange))

        return result

    def query(self, x1, x2, y1, y2):
        qrange = Boundary(x1, x2, y1, y2)
        return self.query_range(qrange)

    # TODO: do sth with this ugly code - rebuild tests
    def query_test_signature(self, points, x1, x2, y1, y2):
        qtree = QuadTree(Boundary(-1.0e6, 1.0e6, -1.0e6, 1.0e6))
        qtree.from_points(points)
        return qtree.query(x1, x2, y1, y2)

    def subdivide(self):
        self.NW, self.NE, self.SW, self.SE = self.boundary.subdivide()
        self.insert(self.point)
        self.point = None


class BoundaryVisualisation(object):
    def __init__(self, x1, x2, y1, y2):
        super().__init__()
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def center(self):
        return (self.x2 + self.x1)/2, (self.y2 + self.y1)/2

    def contains(self, point):
        return self.x1 <= point[0] <= self.x2 and self.y1 <= point[1] <= self.y2

    def intersects(self, boundary):
        if self.x2 < boundary.x1 or boundary.x2 < self.x1 or\
                    self.y2 < boundary.y1 or boundary.y2 < self.y1:
            return False
        return True

    def subdivide(self, parent):
        center_x, center_y = self.center()
        NWBoundary = BoundaryVisualisation(self.x1, center_x, center_y, self.y2)
        NEBoundary = BoundaryVisualisation(center_x, self.x2, center_y, self.y2)
        SWBoundary = BoundaryVisualisation(self.x1, center_x, self.y1, center_y)
        SEBoundary = BoundaryVisualisation(center_x, self.x2, self.y1, center_y)
        NW = QTV(NWBoundary, parent)
        NE = QTV(NEBoundary, parent)
        SW = QTV(SWBoundary, parent)
        SE = QTV(SEBoundary, parent)
        return NW, NE, SW, SE

    def __repr__(self, *args, **kwargs):
        return self.__str__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return str(self.x1) + ", " + str(self.x2) + ", " + str(self.y1) + ", " + str(self.y2)


class QuadTreeVisualisation(object):
    def __init__(self, boundary):
        self.visualisation = []
        self.query_visualisation = []
        self.tree = QTV(boundary, self)

    def construct(self, points):
        self.tree.construct(points)

    def query(self, x1, x2, y1, y2):
        return self.tree.query(x1, x2, y1, y2)


class QTV(object):
    def __init__(self, boundary, parent):
        super().__init__()
        self.boundary = boundary
        self.point = None
        self.NW = None
        self.NE = None
        self.SW = None
        self.SE = None
        self.parent = parent

    def construct(self, points):
        for point in points:
            self.parent.visualisation.append({
                'type': 'point_insert',
                'value': point
            })
            self.insert(point)
            self.parent.visualisation.append({
                'type': 'point_inserted',
                'value': point
            })

    def append_boundary(self, boundary):
        self.parent.visualisation.append({
            'type': 'boundary',
            'value': boundary
        })

    def append_boundary_division(self, boundary):

        center_x, center_y = boundary.center()
        segment1 = (boundary.x1, center_y), (boundary.x2, center_y)
        segment2 = (center_x, boundary.y1), (center_x, boundary.y2)
        self.parent.visualisation.append({
            'type': 'bedges',
            'value': [segment1, segment2]
        })

    def insert(self, point):

        self.append_boundary(self.boundary)
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

    def print(self, lvl=0):
        point_str = " with " + str(self.point) if self.point else " with no point"
        print(str(lvl) + " " + str(self.boundary) + point_str)
        if self.NW:
            self.NW.print(lvl+1)
            self.NE.print(lvl+1)
            self.SW.print(lvl+1)
            self.SE.print(lvl+1)

    def query_range(self, qrange):
        result = []
        if not self.boundary.intersects(qrange):
            return result

        if self.point and qrange.contains(self.point):
            result.append(self.point)

        if not self.NW:
            return result

        result.extend(self.NW.query_range(qrange))
        result.extend(self.NE.query_range(qrange))
        result.extend(self.SW.query_range(qrange))
        result.extend(self.SE.query_range(qrange))

        return result

    def query(self, x1, x2, y1, y2):
        qrange = BoundaryVisualisation(x1, x2, y1, y2)
        return self.query_range(qrange)

    def subdivide(self):
        self.NW, self.NE, self.SW, self.SE = self.boundary.subdivide(self.parent)

        self.append_boundary_division(self.boundary)
        self.insert(self.point)
        self.point = None