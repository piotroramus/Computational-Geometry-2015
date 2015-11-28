__author__ = 'piotr'

# TODO: define 0: HORIZONTAL_SPLIT 1: VERTICAL_SPLIT


class KDTree(object):
    """2-dimensional kd-tree"""
    def __init__(self):
        super().__init__()
        self.root = None

    def _median_index(self, length):
        index = None
        if length % 2 == 0:
            index = length // 2
        else:
            index = (length - 1) // 2
        return index

    def from_points(self, points):
        if self.root:
            raise ValueError("Tree already initialized")

        if points:

            points_x = sorted(points, key=lambda pt: pt.x)
            points_y = sorted(points, key=lambda pt: pt.y)

            # TODO: think if it's possible to manage both points_x and points_y at the same time
            root_point = points_x.pop(self._median_index(len(points_x)))
            points_y.remove(root_point)
            self.root = KDNode(root_point, 0)

            index = 1
            plen = len(points) - 1
            p = None
            while plen > 0:

                if index == 1:
                    p = points_y.pop(self._median_index(len(points_y)))
                    points_x.remove(p)
                else:
                    p = points_x.pop(self._median_index(len(points_x)))
                    points_y.remove(p)

                self.insert(self.root, p)
                index = (index + 1) % 2
                plen -= 1

        else:
            raise ValueError("Points are empty.")

    def insert(self, root, point):

        index = root.index
        root_coord = root.coord_at_index(index)
        point_coord = point.x if index == 0 else point.y

        if point_coord < root_coord:
            if not root.left:
                root.left = KDNode(point, (index + 1) % 2)
            else:
                self.insert(root.left, point)
        else:
            if not root.right:
                root.right = KDNode(point, (index + 1) % 2)
            else:
                self.insert(root.right, point)

    # TODO: rename and make static
    def query_test_signature(self, points, x1, x2, y1, y2):
        kdtree = KDTree()
        kdtree.from_points(points)
        return kdtree.query(x1, x2, y1, y2)

    def query(self, x1, x2, y1, y2):

        #TODO: check if x1 <= x2 and y1 <= y2

        result = []
        queue = [self.root]

        while queue:

            node = queue.pop()
            index = node.index

            if index == 0:
                if x1 > node.point.x:
                    if node.right:
                        queue.append(node.right)
                elif x2 < node.point.x:
                    if node.left:
                        queue.append(node.left)
                else:
                    if y1 <= node.point.y <= y2:
                        result.append(node.point)
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)
            elif index == 1:
                if y1 > node.point.y:
                    if node.right:
                        queue.append(node.right)
                elif y2 < node.point.y:
                    if node.left:
                        queue.append(node.left)
                else:
                    if x1 <= node.point.x <= x2:
                        result.append(node.point)
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)
            else:
                raise ValueError("Incorrect index while querying the tree")

        return result

    def get(self, point):
        node = KDNode(point, index=0)
        result = self.root
        while result:
            if result == node:
                return result
            elif result >= node:
                result = result.left
            else:
                result = result.right
        return None

    def print(self):

        queue = [(self.root, 1)]
        levels = []
        while queue:
            node, lvl = queue.pop(0)
            if node.left:
                queue.append((node.left, lvl + 1))
            if node.right:
                queue.append((node.right, lvl + 1))

            if len(levels) < lvl:
                levels.append([node.point])
            else:
                levels[lvl-1].append(node.point)

        for level in levels:
            print(level)


class KDNode(object):
    """Node of 2-dimensional KDTree"""
    def __init__(self, point, index):
        super().__init__()
        self.point = point
        self.index = index
        self.left = None
        self.right = None

    def coord_at_index(self, index):
        if index == 0:
            return self.point.x
        return self.point.y

    def get_subpoints(self, pts=None):
        if not pts:
            pts = []
        pts.append(self.point)
        if self.left:
            pts = self.left.get_subpoints(pts)
        if self.right:
            pts = self.right.get_subpoints(pts)
        return pts

    def __eq__(self, other):
        return self.point == other.point

    def __ge__(self, other):
        return self.coord_at_index(self.index) >= other.coord_at_index(self.index)

    def __gt__(self, other):
        return self.coord_at_index(self.index) > other.coord_at_index(self.index)

    def __le__(self, other):
        return self.coord_at_index(self.index) <= other.coord_at_index(self.index)

    def __lt__(self, other):
        return self.coord_at_index(self.index) < other.coord_at_index(self.index)

    def __repr__(self, *args, **kwargs):
        return self.__str__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return "Node [" + str(self.point) + ", " + str(self.index) + "]"