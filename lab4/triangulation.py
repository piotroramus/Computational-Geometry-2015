from lab4.Triangle import Triangle

__author__ = 'piotr'

from lab4.classification import *
from lab4.orient import tuple_orient as orient
from lab4.utils import cmp_to_key, Point


LEFT, RIGHT = 0, 1


def is_y_monotonic(segments):
    classification = classify(segments)
    for _, category in classification:
        if category == CONNECTING or category == DIVIDING:
            return False
    return True


def split_chains(segments):

    left, right = [], []
    classification = classify(segments)

    current_chain = left
    for point, category in classification:
        current_chain.append(point)
        if category == ENDING:
            current_chain = right
            # print(str(point) + ": " + category_description[category])

    return left, list(reversed(right))


def is_higher(p1, p2):
    a = p1.value
    b = p2.value
    if a[1] > b[1] or (a[1] == b[1] and a[0] < b[0]):
        return -1
    return 1


def connect_pairs(stack):

    pairs = []
    for i in range(len(stack) - 1, 0, -1):
        pair = (stack[i - 1].value, stack[i]. value)
        pairs.append(pair)

    return pairs


def belongs_to_polygon(triangle, chain):
    point1, point2, point3 = triangle.point1, triangle.point2, triangle.point3
    orientation = orient(point1, point2, point3)
    return (chain == LEFT and orientation > 0) or (chain == RIGHT and orientation < 0)


def triangulate(segments):

    if not is_y_monotonic(segments):
        raise ValueError("Cannot triangulate not y-monotonic polygon")

    triangles = []
    left_chain, right_chain = split_chains(segments)

    points_with_chain = [Point(p, LEFT) for p in left_chain]
    points_with_chain.extend([Point(p, RIGHT) for p in right_chain])
    points = sorted(points_with_chain, key=cmp_to_key(is_higher))

    stack = [points[0], points[1]]

    for current_point_index in range(2, len(segments)):
        point = points[current_point_index]
        top = stack[-1]

        pairs = connect_pairs(stack)
        if point.chain != top.chain:
            for pair in pairs:
                triangle = Triangle(point.value, pair[0], pair[1])
                triangles.append(triangle)
            stack = [top, point]
        else:
            last = stack.pop()
            for pair in pairs:
                triangle = Triangle(point.value, pair[0], pair[1])
                if not belongs_to_polygon(triangle, point.chain):
                    break
                triangles.append(triangle)
                last = stack.pop()
            stack.append(last)
            stack.append(point)

    return triangles


def add_point(visualisation, point, color="black"):
    step = {
        "type": "point",
        "value": (point, color)
    }
    visualisation.append(step)


def add_points(visualisation, points, color="black"):
    step = {
        "type": "points",
        "value": (points, color)
    }
    visualisation.append(step)


def add_segment(visualisation, point1, point2, color="black"):
    segment = point1, point2
    step = {
        "type": "line",
        "value": (segment, color)
    }
    visualisation.append(step)


def add_segments(visualisation, segments, color="black"):
    step = {
        "type": "lines",
        "value": (segments, color)
    }
    visualisation.append(step)


def triangulate_with_visualisation(segments):

    if not is_y_monotonic(segments):
        raise ValueError("Cannot triangulate not y-monotonic polygon")

    visualisation = []
    triangles = []
    left_chain, right_chain = split_chains(segments)
    add_points(visualisation, left_chain, color="brown")
    add_points(visualisation, right_chain, color="cyan")

    points_with_chain = [Point(p, LEFT) for p in left_chain]
    points_with_chain.extend([Point(p, RIGHT) for p in right_chain])
    points = sorted(points_with_chain, key=cmp_to_key(is_higher))

    add_points(visualisation, [points[0].value, points[1].value], color="red")
    stack = [points[0], points[1]]

    for current_point_index in range(2, len(segments)):
        point = points[current_point_index]
        top = stack[-1]
        add_point(visualisation, top.value, color="blue")

        pairs = connect_pairs(stack)
        if point.chain != top.chain:
            for pair in pairs:
                triangle = Triangle(point.value, pair[0], pair[1])
                triangles.append(triangle)
                add_segments(visualisation, triangle.get_lines())
            stack = [top, point]
        else:
            last = stack.pop()
            for pair in pairs:
                triangle = Triangle(point.value, pair[0], pair[1])
                if not belongs_to_polygon(triangle, point.chain):
                    break
                triangles.append(triangle)
                add_segments(visualisation, triangle.get_lines())
                last = stack.pop()
            stack.append(last)
            stack.append(point)

    return triangles, visualisation