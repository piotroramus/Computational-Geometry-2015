__author__ = 'piotr'

from segment import Segment


epsilon = 10e-9

START_SEGMENT = 0
INTERSECTION = 1
SEGMENT_END = 2


def event_desc(event_type):
    desc = ["START", "INTERSECTION", "END"]
    return desc[event_type]


def segment_to_tuple(segment):
    return [(segment.x1, segment.y1), (segment.x2, segment.y2)]


def tuple_to_segments(lines_list):
    segments = []
    for line in lines_list:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[1][0]
        y2 = line[1][1]
        segments.append(Segment(x1, y1, x2, y2))

    return segments