__author__ = 'piotr'

EVEN, ODD = 0, 1


class KDTree(object):
    """2-dimensional kd-tree"""
    def __init__(self):
        super().__init__()
        self.root = None

    def construct_balanced(self, points):
        """Builds balanced tree by recursively dividing sorted indices of points."""
        xsort = list(sorted(points))
        ysort = list(sorted(points, key=lambda p: (p[1], p[0])))
        xi, yi = [], []
        for i, x in enumerate(xsort):
            xi.append(points.index(x))
        for i, y in enumerate(ysort):
            yi.append(points.index(y))

        length = len(xi)
        mi = self._median_index(length)
        median = points[xi[mi]]
        self.root = KDNode(median, EVEN)

        key = self._key(median, EVEN)

        low_x = xi[:mi]
        high_x = xi[mi+1:]
        low_y, high_y = [], []
        for index in yi:
            k = self._key(points[index], EVEN)
            if k < key:
                low_y.append(index)
            elif k > key:
                high_y.append(index)

        self._construct_balanced(points, low_x, low_y, ODD, self.root)
        self._construct_balanced(points, high_x, high_y, ODD, self.root)

    def _construct_balanced(self, points, xi, yi, depth, node):

        length = len(xi) if depth == EVEN else len(yi)

        if length <= 3:
            if length == 3:
                if depth == EVEN:
                    median = points[xi[1]]
                    node = self.insert2(node, median)
                    self.insert2(node, points[xi[0]])
                    self.insert2(node, points[xi[2]])
                else:
                    median = points[yi[1]]
                    node = self.insert2(node, median)
                    self.insert2(node, points[yi[0]])
                    self.insert2(node, points[yi[2]])
            elif length == 2:
                if depth == EVEN:
                    self.insert2(node, points[xi[0]])
                    self.insert2(node, points[xi[1]])
                else:
                    self.insert2(node, points[yi[0]])
                    self.insert2(node, points[yi[1]])
            elif length == 1:
                if depth == EVEN:
                    self.insert2(node, points[xi[0]])
                else:
                    self.insert2(node, points[yi[0]])

        if depth == EVEN and length > 0:

            mi = self._median_index(length)
            median = points[xi[mi]]
            key = self._key(median, depth)
            node = self.insert2(node, median)

            low_x = xi[:mi]
            high_x = xi[mi+1:]

            low_y, high_y = [], []
            for index in yi:
                k = self._key(points[index], EVEN)
                if k < key:
                    low_y.append(index)
                elif k > key:
                    high_y.append(index)

            self._construct_balanced(points, low_x, low_y, (depth + 1) % 2, node)
            self._construct_balanced(points, high_x, high_y, (depth + 1) % 2, node)

        elif depth == ODD and length > 0:

            mi = self._median_index(length)
            median = points[yi[mi]]
            key = self._key(median, depth)
            node = self.insert2(node, median)

            low_y = yi[:mi]
            high_y = yi[mi+1:]

            low_x, high_x = [], []
            for index in xi:
                k = self._key(points[index], ODD)
                if k < key:
                    low_x.append(index)
                elif k > key:
                    high_x.append(index)

            self._construct_balanced(points, low_x, low_y, (depth + 1) % 2, node)
            self._construct_balanced(points, high_x, high_y, (depth + 1) % 2, node)

    def construct_balanced_slow(self, points):
        """Constructs balanced tree by recursively dividing points into parts.
           Slower than construct_balanced. """
        if self.root:
            raise ValueError("Tree already initialized")

        if points:
            points_x = sorted(points)
            points_y = sorted(points, key=lambda pt: (pt[1], pt[0]))

            median_index = self._median_index(len(points_x))
            root_point = points_x[median_index]
            points_y.remove(root_point)
            self.root = KDNode(root_point, EVEN)
            leftp_x = points_x[:median_index]
            leftp_y = [p for p in points_y if p in leftp_x]
            rightp_x = points_x[median_index+1:]
            rightp_y = [p for p in points_y if p in rightp_x]
            if leftp_x:
                self._construct_balanced_slow(leftp_x, leftp_y, self.root)
            if rightp_x:
                self._construct_balanced_slow(rightp_x, rightp_y, self.root)

    def _construct_balanced_slow(self, points_x, points_y, node):

        depth = (node.depth + 1) % 2

        if depth == EVEN:
            median_index = self._median_index(len(points_x))
            pivot = points_x[median_index]
            node = self.insert(node, pivot)

            leftp_x = points_x[:median_index]
            leftp_y = [p for p in points_y if p in leftp_x]

            rightp_x = points_x[median_index+1:]
            rightp_y = [p for p in points_y if p in rightp_x]

            if leftp_x:
                self._construct_balanced_slow(leftp_x, leftp_y, node)
            if rightp_x:
                self._construct_balanced_slow(rightp_x, rightp_y, node)

        elif depth == ODD:
            median_index = self._median_index(len(points_y))
            pivot = points_y[median_index]
            node = self.insert(node, pivot)

            leftp_y = points_y[:median_index]
            leftp_x = [p for p in points_x if p in leftp_y]

            rightp_y = points_y[median_index+1:]
            rightp_x = [p for p in points_x if p in rightp_y]
            if leftp_y:
                self._construct_balanced_slow(leftp_x, leftp_y, node)
            if rightp_y:
                self._construct_balanced_slow(rightp_x, rightp_y, node)

        else:
            raise ValueError("Depth error in _construct_balanced_slow")

    def construct_unbalanced(self, points):
        """Builds slightly unbalanced tree, but works fast.
           Queries on this tree will be slightly slower than on balanced one,
           but the difference is not that big."""
        if self.root:
            raise ValueError("Tree already initialized")

        if points:

            points_x = sorted(points)
            points_y = sorted(points, key=lambda pt: (pt[1], pt[0]))

            root_point = points_x.pop(self._median_index(len(points_x)))
            points_y.remove(root_point)
            self.root = KDNode(root_point, EVEN)

            depth = ODD
            plen = len(points) - 1
            lenx = len(points_x)
            p = None
            while plen > 0:

                if depth == ODD:
                    p = points_y.pop(self._median_index(len(points_y)))
                    points_x.remove(p)
                    lenx -= 1
                else:
                    p = points_x.pop(self._median_index(len(points_x)))
                    points_y.remove(p)
                    lenx -= 1

                self.insert(self.root, p)
                depth = (depth + 1) % 2
                plen -= 1

        else:
            raise ValueError("Points are empty.")

    def get(self, point):
        node = KDNode(point, depth=EVEN)
        result = self.root
        while result:
            if result == node:
                return result
            elif result >= node:
                result = result.left
            else:
                result = result.right
        return None

    def insert(self, root, point):

        depth = root.depth

        if point[depth] < root.point[depth]:
            if not root.left:
                root.left = KDNode(point, (depth + 1) % 2)
                return root.left
            else:
                return self.insert(root.left, point)
        else:
            if not root.right:
                root.right = KDNode(point, (depth + 1) % 2)
                return root.right
            else:
                return self.insert(root.right, point)

    def insert2(self, root, point):

        depth = root.depth

        if self._key(point, depth) < self._key(root.point, depth):
            if not root.left:
                root.left = KDNode(point, (depth + 1) % 2)
                return root.left
            else:
                return self.insert2(root.left, point)
        else:
            if not root.right:
                root.right = KDNode(point, (depth + 1) % 2)
                return root.right
            else:
                return self.insert2(root.right, point)

    def _key(self, point, depth):
        return (point[0], point[1]) if depth == EVEN else (point[1], point[0])

    def _median_index(self, length):
        return (length - 1) // 2

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

    def query(self, x1, x2, y1, y2):

        result = []
        queue = [self.root]

        while queue:

            node = queue.pop()
            depth = node.depth

            if depth == EVEN:
                if x1 > node.point[0]:
                    if node.right:
                        queue.append(node.right)
                elif x2 < node.point[0]:
                    if node.left:
                        queue.append(node.left)
                else:
                    if y1 <= node.point[1] <= y2:
                        result.append(node.point)
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)
            elif depth == ODD:
                if y1 > node.point[1]:
                    if node.right:
                        queue.append(node.right)
                elif y2 < node.point[1]:
                    if node.left:
                        queue.append(node.left)
                else:
                    if x1 <= node.point[0] <= x2:
                        result.append(node.point)
                    if node.left:
                        queue.append(node.left)
                    if node.right:
                        queue.append(node.right)
            else:
                raise ValueError("Incorrect depth while querying the tree")

        return result

    # TODO: rename and make static
    def query_test_signature(self, points, x1, x2, y1, y2):
        kdtree = KDTree()
        kdtree.construct_balanced_slow(points)
        return kdtree.query(x1, x2, y1, y2)

    def size(self):
        return self._size(self.root) + 1

    def _size(self, node):
        size = 0
        if node.left:
            size = self._size(node.left) + 1
        if node.right:
            size = size + self._size(node.right) + 1
        return size


class KDNode(object):
    """Node of 2-dimensional KDTree"""
    def __init__(self, point, depth):
        super().__init__()
        self.point = point
        self.depth = depth
        self.left = None
        self.right = None

    def __repr__(self, *args, **kwargs):
        return self.__str__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return "Node [" + str(self.point) + ", " + str(self.depth) + "]"