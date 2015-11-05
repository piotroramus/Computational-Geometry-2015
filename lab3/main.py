__author__ = 'piotr'

from display.graphics_wrapper import *
from segments_io import *
from sweeping import sweep
from utils import segment_to_tuple, tuple_to_segments
from alg_test import test


def draw_current_intersections(drawer, intersections):
    for i in intersections:
        drawer.draw_point((i[0], i[1]), color=intersection_color, radius=3)


def process_and_draw(lines):

    d = Drawer("Sweeping", axes_sizes=(x_ax, y_ax))
    d.start()
    d.draw_coordinate_system()

    segments = tuple_to_segments(lines)
    (inters, display_actions) = sweep(segments)

    for line in lines:
        d.draw_line(line[0], line[1], color=waiting_color, width=2)
        d.draw_point((line[0][0], line[0][1]), color="black", radius=2)
        d.draw_point((line[1][0], line[1][1]), color="black", radius=2)

    current_intersections = []
    prev_sweep = None

    # sweep animation
    for da in display_actions:
        if prev_sweep:
            d.remove(prev_sweep)
        prev_sweep = d.draw_line((da[0], -y_ax), (da[0], y_ax), color=sweep_color)
        sa_dict = da[1]
        if sa_dict['new_active']:
            active_segment = segment_to_tuple(sa_dict['new_active'])
            d.draw_line(active_segment[0], active_segment[1], color=active_color, width=2)
        if sa_dict['new_processed']:
            processed_segment = segment_to_tuple(sa_dict['new_processed'])
            d.draw_line(processed_segment[0], processed_segment[1], color=processed_color, width=2)
            draw_current_intersections(d, current_intersections)
        if sa_dict['intersection']:
            point = sa_dict['intersection']
            current_intersections.append((point.x, point.y))
            draw_current_intersections(d, current_intersections)
        d.wait_seconds(sweep_speed)
        # d.wait_for_click()

    # d.wait_for_click()
    d.wait_for_key_pressed()
    d.shutdown()


if __name__ == "__main__":

    active_color = "blue"
    processed_color = "grey"
    waiting_color = "green"
    sweep_color = "red"
    intersection_color = "yellow"
    sweep_speed = 1

    x_ax = 10
    y_ax = 10

    lines1 = read_lines_from_file('input/lines1.txt')
    lines2 = generate_random_lines(10, -x_ax, x_ax, -y_ax, y_ax)
    lines3 = read_lines_from_file('input/lines3.txt')
    lines4 = read_lines_from_file('input/lines2.txt')
    lines5 = read_lines_from_file('input/lines5.txt')

    random = lines2
    # lines_to_sweep = random
    lines_to_sweep = lines4

    # for tests purposes
    # write_lines_to_file(lines_to_sweep, 'alg_test/test_lines4.txt')

    process_and_draw(lines_to_sweep)
    # test.test_algorithm()