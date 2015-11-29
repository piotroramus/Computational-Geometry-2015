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

    def _fp(self, points_x, points_y, node):

        depth = (node.index + 1) % 2

        if depth == 0:
            median_index = self._median_index(len(points_x))
            pivot = points_x[median_index]
            node = self.insert(node, pivot)

            leftp_x = points_x[:median_index]
            leftp_y = [p for p in points_y if p in leftp_x]

            rightp_x = points_x[median_index+1:]
            rightp_y = [p for p in points_y if p in rightp_x]

            if leftp_x:
                self._fp(leftp_x, leftp_y, node)
            if rightp_x:
                self._fp(rightp_x, rightp_y, node)

        elif depth == 1:
            median_index = self._median_index(len(points_y))
            pivot = points_y[median_index]
            node = self.insert(node, pivot)

            leftp_y = points_y[:median_index]
            leftp_x = [p for p in points_x if p in leftp_y]

            rightp_y = points_y[median_index+1:]
            rightp_x = [p for p in points_x if p in rightp_y]
            if leftp_y:
                self._fp(leftp_x, leftp_y, node)
            if rightp_y:
                self._fp(rightp_x, rightp_y, node)

        else:
            raise ValueError("Depth error in _fp")

    def from_points_recursively(self, points):

        if self.root:
            raise ValueError("Tree already initialized")

        if points:
            points_x = sorted(points, key=lambda pt: pt.x)
            points_y = sorted(points, key=lambda pt: pt.y)

            median_index = self._median_index(len(points_x))
            root_point = points_x[median_index]
            points_y.remove(root_point)
            self.root = KDNode(root_point, 0)
            leftp_x = points_x[:median_index]
            leftp_y = [p for p in points_y if p in leftp_x]
            rightp_x = points_x[median_index+1:]
            rightp_y = [p for p in points_y if p in rightp_x]
            if leftp_x:
                self._fp(leftp_x, leftp_y, self.root)
            if rightp_x:
                self._fp(rightp_x, rightp_y, self.root)

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
            lenx = len(points_x)
            p = None
            while plen > 0:

                if index == 1:
                    p = points_y.pop(self._median_index(len(points_y)))
                    points_x.remove(p)
                    lenx -= 1
                else:
                    p = points_x.pop(self._median_index(len(points_x)))
                    points_y.remove(p)
                    lenx -= 1

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
                return root.left
            else:
                self.insert(root.left, point)
        else:
            if not root.right:
                root.right = KDNode(point, (index + 1) % 2)
                return root.right
            else:
                self.insert(root.right, point)

    # TODO: rename and make static
    def query_test_signature(self, points, x1, x2, y1, y2):
        kdtree = KDTree()
        kdtree.from_points_recursively(points)
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