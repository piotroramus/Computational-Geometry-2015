__author__ = 'piotr'


class KDTree(object):
    """2-dimensional kd-tree"""
    def __init__(self):
        super().__init__()
        self.root = None

    def from_points(self, points):
        if self.root:
            raise ValueError("Tree already initialized")

        if points:
            self.root = KDNode(points.pop(0), 0)

        for p in points:
            self.insert(self.root, p)

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

    def query(self, x1, x2, y1, y2):
        pass

    def get(self, point):
        node = KDNode(point, index=0)
        result = self.root
        while result:
            if result == node:
                return result
            elif self.root < node:
                result = result.left
            else:
                result = result.right
        return result

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

    def __eq__(self, other):
        return self.point == other.point

    def __lt__(self, other):
        return self.coord_at_index(self.index) < other.coord_at_index(self.index)

    def __repr__(self, *args, **kwargs):
        return self.__str__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return "Node [" + str(self.point) + ", " + str(self.index) + "]"