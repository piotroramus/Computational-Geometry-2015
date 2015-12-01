from lab4.display.graphics_wrapper import Drawer
from project.visualisation_utils import draw_points_with_mouse

__author__ = 'piotr'


def visualise(filename=None):

    exit_keys = ["Escape", 'q']

    x_ax = 10
    y_ax = 10
    click_epsilon = 0.03

    d = Drawer("KDTree", axes_sizes=(x_ax, y_ax), window_sizes=(600, 600))
    d.start()

    win_size_x = d.window_x_size
    win_size_y = d.window_y_size
    scale_arguments = d, win_size_x, win_size_y, x_ax, y_ax

    points = []
    if filename:
        pass
        # segments = get_segments_from_file(filename, d)
    else:
        points = draw_points_with_mouse(scale_arguments)

    d.put_text_not_scaled("q -> quit        ", (40, win_size_y - 30), size=9)

    pressed_key = d.get_pressed_key()
    while pressed_key not in exit_keys:

        pressed_key = d.get_pressed_key()

    d.shutdown()