from lab4.display.graphics_wrapper import Drawer
from project.kdtree import KDTreeVisualisation
from project.visualisation_utils import draw_points_with_mouse, INFINITE, HORIZONTAL, VERTICAL


def determine_rectangle(point_range, win_size_x, win_size_y):
    xmin, xmax, ymin, ymax = point_range

    if not xmin:
        xmin = -win_size_x
    if not xmax:
        xmax = win_size_x
    if not ymin:
        ymin = -win_size_y
    if not ymax:
        ymax = win_size_y

    p1 = xmin, ymin
    p2 = xmax, ymax
    return p1, p2


def determine_line(point_range, point, orient, win_size_x, win_size_y):
    xmin, xmax, ymin, ymax = point_range

    if not xmin:
        xmin = -win_size_x
    if not xmax:
        xmax = win_size_x
    if not ymin:
        ymin = -win_size_y
    if not ymax:
        ymax = win_size_y

    if orient == HORIZONTAL:
        p1 = xmin, point[1]
        p2 = xmax, point[1]
    elif orient == VERTICAL:
        p1 = point[0], ymin
        p2 = point[0], ymax
    else:
        raise ValueError("If this happens, something is really wrong.")

    return p1, p2


def draw_construction(visualisation, d, win_size_x, win_size_y, wait=False):
    for step in visualisation:

        if step['direction'] == HORIZONTAL or step['direction'] == VERTICAL:
            pr = step['point_range']
            point = step['point']
            p1, p2 = determine_line(pr, point, step['direction'], win_size_x, win_size_y)
        elif step['direction'] == INFINITE:
            p1 = step['point']
            p1 = p1[0], -win_size_y
            p2 = p1[0], win_size_y
        if p1 and p2:
            d.draw_line(p1, p2, color="black")
        if wait:
            d.wait_for_click()


def draw_search_range(search_range, d):
    d.draw_rectangle((search_range[0], search_range[2]), (search_range[1], search_range[3]), outline_color="black", fill_color="yellow")


def visualise(search_range, filename=None):

    exit_keys = ["Escape", 'q']
    build_keys = ['b']
    search_keys = ['s']
    coord_system = ['c']

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
    d.put_text_not_scaled("s -> search  ", (40, win_size_y - 50), size=9)
    d.put_text_not_scaled("q -> quit    ", (40, win_size_y - 30), size=9)

    tree_built = False
    kdtree = KDTreeVisualisation()

    pressed_key = d.get_pressed_key()
    while pressed_key not in exit_keys:

        if pressed_key in build_keys:
            kdtree.construct_balanced(points)
            tree_built = True
            draw_construction(kdtree.visualisation, d, win_size_x, win_size_y, wait=True)

        elif pressed_key in search_keys:
            if tree_built:
                kdtree.query(*search_range)

                draw_search_range(search_range, d)
                draw_construction(kdtree.visualisation, d, win_size_x, win_size_y)
                for p in points:
                    d.draw_point(p, radius=3, color="black")

                r = None
                for step in kdtree.query_visualisation:
                    if r:
                        d.remove(r)
                    if step['type'] == 'point':
                        d.draw_point(step['value'], radius=5, color="red")
                    if step['type'] == 'result_point':
                        d.draw_point(step['value'], radius=3, color="blue")
                    if step['type'] == 'rect':
                        p1, p2 = determine_rectangle(step['value'], win_size_x, win_size_y)
                        r = d.draw_rectangle(p1, p2)
                        draw_search_range(search_range, d)
                        draw_construction(kdtree.visualisation, d, win_size_x, win_size_y)
                        for p in points:
                            d.draw_point(p, radius=3, color="black")

                    d.wait_for_click()

        elif pressed_key in coord_system:
            d.draw_coordinate_system()

        pressed_key = d.get_pressed_key()

    d.shutdown()