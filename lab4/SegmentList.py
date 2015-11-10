__author__ = 'piotr'

from lab4.Segment import Segment
from copy import deepcopy


class SegmentList(object):
    def __init__(self):
        super().__init__()
        self.segments = []

    def add_segment(self, segment):
        self.segments.append(segment)

    def add_segment_from_points(self, p1, p2):
        self.segments.append(Segment(p1[0], p1[1], p2[0], p2[1]))

    def find_init_segment(self):

        if not self.segments:
            return None

        init_segment = self.segments[0]

        for segment in self.segments:

            if segment.max_y() < init_segment.max_y():
                continue

            init_x, init_y = init_segment.max_point()
            seg_mx, seg_my = segment.max_point()

            if seg_my == init_y:
                if segment.min_x() < init_x:
                    init_segment = segment

            if seg_my > init_y:
                init_segment = segment

        return init_segment

    def sort_by_path(self):
        segs = deepcopy(self.segments)
        init_segment = self.find_init_segment()
        segs.remove(init_segment)
        mp = init_segment.max_point()
        sorted_init = init_segment.sort(*mp)
        new_order = [sorted_init]
        next_x, next_y = sorted_init.x2, sorted_init.y2

        while segs:

            next_segment = None
            for s in segs:
                if (s.x1 == next_x and s.y1 == next_y) or (s.x2 == next_x and s.y2 == next_y):
                    next_segment = s
                    segs.remove(s)
                    break

            ns = next_segment.sort(next_x, next_y)
            next_x, next_y = ns.x2, ns.y2
            new_order.append(ns)

        self.segments = new_order

    def validate(self):
        """ Checks if segments are logically connected in one coherent path """
        if not self.segments:
            return True
        prev_segment = self.segments[0]
        for segment in self.segments[1:]:
            if segment.x1 != prev_segment.x2 or segment.y1 != prev_segment.y2:
                return False
            prev_segment = segment

        first_segment = self.segments[0]
        last_segment = self.segments[-1]
        if first_segment.x1 != last_segment.x2 or first_segment.y1 != last_segment.y2:
            return False

        return True

    def print(self):
        print("SEGMENTS START: ")
        for segment in self.segments:
            print(segment)
        print("SEGMENTS END")

    def __len__(self):
        return len(self.segments)
