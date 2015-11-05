# coding=utf-8

from lab3.intersection_test import get_intersection_point, intersects
from lab3.intersection import Intersection
from lab3.event_class import Event
from lab3.state_class import State
from lab3.segment_id import SegmentId
from lab3.utils import *
import heapq


def sweep(segments):
    if len(segments) == 0:
        return []

    for segment in segments:

        #if segments were generated in reverted way, order them
        if segment.x1 > segment.x2:
            segment.x1, segment.x2 = segment.x2, segment.x1
            segment.y1, segment.y2 = segment.y2, segment.y1
            segment.point1, segment.point2 = segment.point2, segment.point1

        #if segments is a point
        if segment.x1 == segment.x2:
            segment.x2 = segment.x2 + epsilon

    min_segment = min(segments, key=lambda x: x.x1)
    state = State(segments, min_segment.x1)
    intersections = set()
    events = []
    display_actions = []

    i = 0
    for segment in segments:
        heapq.heappush(events, Event(START_SEGMENT, segment.point1, SegmentId(i, state), None))
        heapq.heappush(events, Event(SEGMENT_END, segment.point2, SegmentId(i, state), None))
        i += 1

    while len(events) > 0:

        event = heapq.heappop(events)
        state.x = event.point.x
        new_neighbours = []

        if event.event_type == START_SEGMENT:
            new_neighbours = state.insert(event.segment1)
            sweep_dict = {"new_active": segments[event.segment1.label], "new_processed": None, "intersection": None}
            display_actions.append([event.point.x, sweep_dict])
        elif event.event_type == SEGMENT_END:
            new_neighbours = state.delete(event.segment1)
            sweep_dict = {"new_active": None, "new_processed": segments[event.segment1.label], "intersection": None}
            display_actions.append([event.point.x, sweep_dict])
        elif event.event_type == INTERSECTION:
            new_neighbours = state.swap(event.segment1, event.segment2)
            sweep_dict = {"new_active": None, "new_processed": None, "intersection": event.point}
            display_actions.append([event.point.x, sweep_dict])

        #if there are some new pairs of neighbours
        for neighbours in new_neighbours:

            (segment_id1, segment_id2) = neighbours
            segment1 = segments[segment_id1.label]
            segment2 = segments[segment_id2.label]

            if intersects(segment1, segment2):

                intersection_point = get_intersection_point(segment1, segment2)
                already_got1 = Intersection(segment_id1.label, segment_id2.label, intersection_point) in intersections
                already_got2 = Intersection(segment_id2.label, segment_id1.label, intersection_point) in intersections
                if already_got1 or already_got2:
                    continue

                new_event = Event(INTERSECTION, intersection_point, segment_id1, segment_id2)
                heapq.heappush(events, new_event)
                intersections.add(Intersection(segment_id1.label, segment_id2.label, intersection_point))


    # generate test output
    # with open('alg_test/expected_output4.txt', 'w') as f:
    #     for i in intersections:
    #         f.write(str(i.point.x) + " " + str(i.point.y) + "\n")

    result = []
    for i in intersections:
        seg1 = segments[i.segment1]
        seg2 = segments[i.segment2]
        result.append((seg1, seg2, i.point))

    return (result, display_actions)
