__author__ = 'piotr'

from lab4.Segment import Segment


class SegmentList(object):
    def __init__(self):
        super().__init__()
        self.segments = []

    def add_segment(self, segment):
        self.segments.append(segment)

    def add_segment_from_points(self, p1, p2):
        self.segments.append(Segment(p1[0], p1[1], p2[0], p2[1]))

    def validate(self):
        for segments in self.segments:
            pass

    def sort_by_path(self):
        pass

    def print(self):
        for segment in self.segments:
            print(segment)

    def __len__(self):
        return len(self.segments)
