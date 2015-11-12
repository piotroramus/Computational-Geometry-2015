from lab4.SegmentList import SegmentList

__author__ = 'piotr'


def write_points_to_file(points, filename, separator=' '):
    with open(filename, 'w') as f:
        for point in points:
            f.write(str(point[0]) + separator + str(point[1]) + "\n")


def read_points_from_file(filename, separator=' '):
    points = []
    with open(filename) as f:
        for line in f:
            x, y = line.split(separator)
            points.append((float(x), float(y)))
    return points


def get_segments_from_file(filename, drawer):

    segments = SegmentList()
    points = read_points_from_file(filename, ' ')
    p1 = points[0]
    for point in points[1:]:
        segments.add_segment_from_points(p1, point)
        p1 = point
    segments.add_segment_from_points(points[-1], points[0])

    for segment in segments.segments:
        p1 = (segment.x1, segment.y1)
        p2 = (segment.x2, segment.y2)
        drawer.draw_line(p1, p2, color="grey")
        drawer.draw_point(p1, color="black")
        drawer.draw_point(p2, color="black")

    return segments


def get_mouse_scaled(drawer, win_size_x, win_size_y, x_range, y_range):
        point = drawer.get_mouse_click()
        new_x = 2 * x_range * point[0] / win_size_x - x_range
        new_y = 2 * y_range * (win_size_y - point[1]) / win_size_y - y_range
        return new_x, new_y


def click_difference(point1, point2, epsilon):
    x_dist = abs(point1[0] - point2[0])
    y_dist = abs(point1[1] - point2[1])
    if x_dist + y_dist > epsilon:
        return True
    return False


def draw_segments_with_mouse(scale_arguments, click_epsilon=0.03):

    d, win_size_x, win_size_y, x_ax, y_ax = scale_arguments
    segments = SegmentList()

    prev_point = None
    init_point = get_mouse_scaled(*scale_arguments)
    current_point = init_point
    while not prev_point or click_difference(prev_point, current_point, click_epsilon):
        if prev_point:
            segments.add_segment_from_points(prev_point, current_point)
        d.draw_point(current_point, color="black")
        prev_point = current_point
        current_point = get_mouse_scaled(*scale_arguments)
        d.draw_line(current_point, prev_point, color="grey")

    segments.add_segment_from_points(prev_point, init_point)
    d.draw_line(current_point, init_point, color="gray")

    return segments