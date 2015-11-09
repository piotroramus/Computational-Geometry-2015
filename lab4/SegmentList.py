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

    def validate(self):
        for segments in self.segments:
            pass

    def sort_by_path(self):
        pass

    def print(self):
        print("SEGMENTS START: ")
        for segment in self.segments:
            print(segment)
        print("SEGMENTS END")

    def __len__(self):
        return len(self.segments)
