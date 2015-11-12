__author__ = 'piotr'

from lab4.display.graphics_wrapper import Drawer
from lab4.classification import *
from lab4.triangulation import is_y_monotonic, triangulate_with_visualisation
from lab4.points_io import get_segments_from_file, draw_segments_with_mouse


def draw(filename=None):

    d = Drawer("Triangulation", axes_sizes=(x_ax, y_ax), window_sizes=(400, 400))
    d.start()
    d.draw_coordinate_system()

    win_size_x = d.window_x_size
    win_size_y = d.window_y_size
    scale_arguments = d, win_size_x, win_size_y, x_ax, y_ax

    segments = None
    if filename:
        segments = get_segments_from_file(filename, d)
    else:
        segments = draw_segments_with_mouse(scale_arguments, click_epsilon)

    segments.sort_by_monotonicity()

    assert segments.validate()

    d.put_text_not_scaled("c -> classify    ", (40, win_size_y - 70), size=9)
    d.put_text_not_scaled("t -> triangulate ", (40, win_size_y - 50), size=9)
    d.put_text_not_scaled("q -> quit        ", (40, win_size_y - 30), size=9)

    text = None
    y_monotonic = is_y_monotonic(segments.segments)
    if y_monotonic:
        text = d.put_text_not_scaled("Polygon is y-monotonic", (win_size_x - 93, win_size_y - 30), size=10)
    else:
        text = d.put_text_not_scaled("Polygon is not y-monotonic", (win_size_x - 100, win_size_y - 30), size=10)

    pressed_key = d.get_pressed_key()
    while pressed_key not in exit_keys:

        if pressed_key in classify_keys:
            classification = classify(segments.segments)
            for point, category in classification:
                d.draw_point(point, radius=3, color=category_color[category])

        elif pressed_key in monotonicity_check_keys:
            if is_y_monotonic(segments.segments):
                text = d.put_text_not_scaled("Polygon is y-monotonic", (win_size_x - 93, win_size_y - 30), size=10)
            else:
                text = d.put_text_not_scaled("Polygon is not y-monotonic", (win_size_x - 100, win_size_y - 30), size=10)

        elif pressed_key in triangulation_keys:
            if not y_monotonic:
                d.remove(text)
                text = d.put_text_not_scaled("Cannot triangulate not y-monotonic polygon!", (win_size_x - 150, win_size_y - 30), size=10)
            else:
                triangles, visualisation = triangulate_with_visualisation(segments.segments)
                for step in visualisation:
                    if step["type"] == "points":
                        (points, color) = step["value"]
                        for point in points:
                            d.draw_point(point, radius=3, color=color)
                    elif step["type"] == "point":
                        point, color = step["value"]
                        d.draw_point(point, radius=3, color=color)
                    elif step["type"] == "line":
                        segment, color = step["value"]
                        d.draw_line(segment[0], segment[1], color=color)
                    elif step["type"] == "lines":
                        (lines, color) = step["value"]
                        for line in lines:
                            d.draw_line(line[0], line[1], color=color)

                    d.wait_for_click()

        pressed_key = d.get_pressed_key()

    d.shutdown()


if __name__ == "__main__":

    exit_keys = ["Escape", 'q']
    classify_keys = ['c']
    triangulation_keys = ['t']
    monotonicity_check_keys = ['m']

    x_ax = 10
    y_ax = 10
    click_epsilon = 0.03

    draw()
    # draw(filename='input/example_from_lab.txt')
