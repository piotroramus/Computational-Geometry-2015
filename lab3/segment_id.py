__author__ = 'piotr'


class SegmentId(object):
    def __init__(self, label, sweep_state):
        self.label = label
        self.sweep_state = sweep_state

    def __lt__(self, other):
        self_sweep_crossing_point = self.sweep_state.segment_crossing_point(self)
        other_sweep_crossing_point = self.sweep_state.segment_crossing_point(other)
        return self_sweep_crossing_point - other_sweep_crossing_point > 0

    def __eq__(self, other):
        return self.label == other.label
