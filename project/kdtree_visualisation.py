from lab4.display.graphics_wrapper import Drawer
from project.kdtree import KDTreeVisualisation
from project.visualisation_utils import draw_points_with_mouse, INFINITE
from project.visualisation_utils import UP, DOWN, LEFT, RIGHT, BOTH


def visualise(filename=None):

    exit_keys = ["Escape", 'q']
    build_keys = ['b']

    x_ax = 10
    y_ax = 10

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

    d.put_text_not_scaled("b -> build   ", (40, win_size_y - 70), size=9)
    d.put_text_not_scaled("q -> quit    ", (40, win_size_y - 30), size=9)

    pressed_key = d.get_pressed_key()
    while pressed_key not in exit_keys:

        if pressed_key in build_keys:
            kdtree = KDTreeVisualisation()
            kdtree.construct_balanced(points)

            for step in kdtree.visualisation:
                p1 = step['point1']
                p2 = None
                if step['direction'] == INFINITE:
                    p1 = p1[0], -win_size_y
                    p2 = p1[0], win_size_y
                elif step['direction'] == BOTH:
                    p2 = step['point2']
                elif step['direction'] == UP:
                    p2 = p1[0], win_size_y
                    d.draw_line(p1, p2)
                elif step['direction'] == LEFT:
                    p2 = -win_size_x, p1[1]
                elif step['direction'] == DOWN:
                    p2 = p1[0], -win_size_y
                elif step['direction'] == RIGHT:
                    p2 = win_size_x, p1[1]
                d.draw_line(p1, p2)
                d.wait_for_click()

        pressed_key = d.get_pressed_key()

    d.shutdown()