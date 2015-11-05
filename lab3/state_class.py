__author__ = 'piotr'

from bintrees import AVLTree
from lab3.utils import epsilon


class State(object):
    def __init__(self, segments, x):
        self.segments = segments
        self.x = x
        self.tree = AVLTree()

    def segment_crossing_point(self, segment_id):

        segment = self.segments[segment_id.label]
        segment_dx = segment.x2 - segment.x1
        sweep_dx = self.x - segment.x1
        segment_dy = segment.y2 - segment.y1
        sweep_dy = segment_dy * (sweep_dx / segment_dx)
        return segment.y1 + sweep_dy

    def insert(self, new_segment):
        """ Returns new pair of neighbours """
        new_neighbours = []
        self.tree.insert(new_segment, new_segment)
        try:
            new_neighbours.append((self.tree.prev_item(new_segment)[0], new_segment))
        except KeyError:
            pass
        try:
            new_neighbours.append((self.tree.succ_item(new_segment)[0], new_segment))
        except KeyError:
            pass
        return new_neighbours

    def delete(self, segment):
        """ Returns new pair of neighbours """
        new_neighbours = []
        predecessor = None
        successor = None
        try:
            predecessor = self.tree.prev_item(segment)[0]
        except KeyError:
            pass
        try:
            successor = self.tree.succ_item(segment)[0]
        except KeyError:
            pass
        if predecessor and successor:
            # make predecessor and successor new neighbours
            new_neighbours.append((predecessor, successor))

        self.tree.remove(segment)
        return new_neighbours

    def swap(self, segment1, segment2):
        """ Returns new pair of neighbours """
        pos_x = self.x
        self.x = pos_x - epsilon
        new_neighbours1 = self.delete(segment1)
        self.x = pos_x + epsilon
        new_neighbours2 = self.insert(segment1)
        self.x = pos_x

        all_neighbours = new_neighbours1 + new_neighbours2
        new_neighbours = []

        for neighbours in all_neighbours:
            if neighbours != (segment1, segment2) and neighbours != (segment2, segment1):
                new_neighbours.append(neighbours)
        return new_neighbours
