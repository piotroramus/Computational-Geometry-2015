# coding=utf-8
import matplotlib.pyplot as plt

__author__ = 'Michał Ciołczyk'


# noinspection PyTypeChecker
class Line(object):
    def __init__(self, x1, y1, x2, y2, color, label=None):
        """Creates a line segment from (x1, y1) to (x2, y2) of color `color` and label `label`.

        :param x1: the x coordinate of the first point
        :type x1: float
        :param y1: the y coordinate of the first point
        :type y1: float
        :param x2: the x coordinate of the second point
        :type x2: float
        :param y2: the y coordinate of the second point
        :type y2: float
        :param color: line color (expressed as `matplotlib`'s color)
        :type color: str
        :param label: line label
        :type label: str
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.label = label

    @classmethod
    def from_points(cls, p1, p2, color, label=None):
        """Creates a line segment from p1 to p2 of color `color` and label `label`.

        :param p1: first point
        :type p1: Point
        :param p2: second point
        :type p2: Point
        :param color: line color (expressed as `matplotlib`'s color)
        :type color: str
        :param label: line label
        :type label: str
        :return: Line instance.
        :rtype: Line
        """
        return cls(p1.x, p1.y, p2.x, p2.y, color, label)

    def draw(self, ax, dy=0, animate=False):
        if animate:
            figures = [plt.Line2D([self.x1, self.x2], [self.y1, self.y2], color=self.color)]
            x_middle = (self.x1 + self.x2) / 2.0
            y_middle = (self.y1 + self.y2) / 2.0 - dy
            if self.label:
                figures.append(plt.Text(x_middle, y_middle, self.label,
                                        horizontalalignment='center',
                                        verticalalignment='center',
                                        fontsize=10))
            return figures
        else:
            ax.plot([self.x1, self.x2], [self.y1, self.y2], c=self.color)
            if self.label:
                x_middle = (self.x1 + self.x2) / 2.0
                y_middle = (self.y1 + self.y2) / 2.0 - dy
                ax.text(x_middle, y_middle, self.label, horizontalalignment='center', verticalalignment='center',
                        fontsize=10)

    def max_y(self):
        return max(self.y1, self.y2)

    def min_y(self):
        return min(self.y1, self.y2)

    def max_x(self):
        return max(self.x1, self.x2)

    def min_x(self):
        return min(self.x1, self.x2)


# noinspection PyTypeChecker
class Point(object):
    def __init__(self, x, y, color, label=None):
        self.x = x
        self.y = y
        self.color = color
        self.label = label

    def draw(self, ax, dy=0, animate=False):
        if animate:
            figures = [plt.Line2D([self.x], [self.y], marker='o', color=self.color)]
            if self.label:
                figures.append(plt.Text(self.x, self.y - dy, self.label, horizontalalignment='center',
                                        verticalalignment='center', fontsize=10))

            return figures
        else:
            ax.plot([self.x], [self.y], 'o', c=self.color)
            if self.label:
                ax.text(self.x, self.y - dy, self.label, horizontalalignment='center', verticalalignment='center',
                        fontsize=10)

    def max_y(self):
        return self.y

    def min_y(self):
        return self.y

    def max_x(self):
        return self.x

    def min_x(self):
        return self.x

    def __str__(self):
        return "Point(%f, %f, color=%s)" % (self.x, self.y, self.color)

    def __unicode__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)