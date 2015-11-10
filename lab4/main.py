__author__ = 'piotr'

from lab4.display.graphics_wrapper import Drawer
from lab4.classification import classify
from lab4.SegmentList import SegmentList
from lab4.tests.classification_tests import test_classification, category_color


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


def draw():

    d = Drawer("Sweeping", axes_sizes=(x_ax, y_ax))
    d.start()
    d.draw_coordinate_system()

    win_size_x = d.window_x_size
    win_size_y = d.window_y_size
    scale_arguments = d, win_size_x, win_size_y, x_ax, y_ax

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

    segments.add_segment_from_points(current_point, init_point)
    d.draw_line(current_point, init_point, color="gray")

    segments.sort_by_path()

    assert segments.validate()
    test_classification()

    key = d.get_pressed_key()
    if key == 'c':
        classification = classify(segments.segments)
        for point, category in classification:
            d.draw_point(point, radius=3, color=category_color[category])
            print(str(point) + "; " + str(category))

    elif key in closing_keys:
        d.shutdown()
        return

    pressed_key = d.get_pressed_key()
    while pressed_key not in closing_keys:
        pressed_key = d.get_pressed_key()

    d.shutdown()


if __name__ == "__main__":

    #counterclockwise -> det > 0

    closing_keys = ["Escape", 'q']

    x_ax = 10
    y_ax = 10
    click_epsilon = 0.03
    draw()