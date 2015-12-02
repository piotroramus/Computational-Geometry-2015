from lab4.display.graphics_wrapper import Drawer
from project.quadtree import QuadTreeVisualisation, BoundaryVisualisation
from project.visualisation_utils import draw_points_with_mouse
import pprint

__author__ = 'piotr'


def draw_construction(visualisation, points, d, win_size_x, win_size_y, wait=False):

    pp = pprint.PrettyPrinter(indent=3)
    pp.pprint(visualisation)

    b = None
    points_raw = points
    points_inserted = []
    active_point = None
    segments = []

    v = iter(visualisation)
    for step in v:
        if step['type'] == 'boundary':
            boundary = step['value']
            p1 = boundary.x1, boundary.y1
            p2 = boundary.x2, boundary.y2
            b = d.draw_rectangle(p1, p2)
            draw_segments(segments, d)
            draw_points(d, points_raw, points_inserted, active_point)
        elif step['type'] == 'bedges':
            segment1, segment2 = step['value']
            segments.append(segment1)
            segments.append(segment2)
            draw_segments(segments, d)
        elif step['type'] == 'point_insert':
            point = step['value']
            active_point = point
            points_raw.remove(point)
            draw_points(d, points_raw, points_inserted, active_point)
        elif step['type'] == 'point_inserted':
            point = step['value']
            points_inserted.append(point)
            draw_points(d, points_raw, points_inserted, active_point)

        if b:
            d.wait_for_click()
            d.remove(b)
            b = None

        if wait:
            d.wait_for_click()

    d.draw_point(active_point, radius=3, color='green')
    return segments


def draw_points(d, points_raw, points_inserted, active_point=None):
    for p in points_raw:
        d.draw_point(p, radius=2, color="black")
    for p in points_inserted:
        d.draw_point(p, radius=3, color='green')
    if active_point:
        d.draw_point(active_point, radius=3, color='red')


def draw_search_range(search_range, d):
    d.draw_rectangle((search_range[0], search_range[2]), (search_range[1], search_range[3]), outline_color="black", fill_color="yellow")


def draw_segments(segments, d):
    for s in segments:
        d.draw_line(s[0], s[1])


def print_help(d, win_size_y):
    d.put_text_not_scaled("b -> build      ", (40, win_size_y - 90), size=9)
    d.put_text_not_scaled("f -> fast build ", (40, win_size_y - 70), size=9)
    d.put_text_not_scaled("s -> search     ", (40, win_size_y - 50), size=9)
    d.put_text_not_scaled("q -> quit       ", (40, win_size_y - 30), size=9)


def redraw_query_points(d, result_points, points):
    for p in points:
        d.draw_point(p, radius=3, color="green")
    for p in result_points:
        d.draw_point(p, radius=3, color=d.color(69, 23, 162))


def redraw_tree(d, result_point, points, segments):
    redraw_query_points(d, result_point, points)
    draw_segments(segments, d)


def visualise(search_range, filename=None):

    exit_keys = ["Escape", 'q']
    build_keys = ['b']
    search_keys = ['s']
    coord_system = ['c']
    fast_build = ['f']

    x_ax = 10
    y_ax = 10

    d = Drawer("QuadTree", axes_sizes=(x_ax, y_ax), window_sizes=(600, 600))
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

    print_help(d, win_size_y)

    tree_built = False

    minbound = -x_ax - 1
    maxbound = x_ax + 1
    boundary = BoundaryVisualisation(minbound, maxbound, minbound, maxbound)
    qtree = QuadTreeVisualisation(boundary)
    segments = []

    pressed_key = d.get_pressed_key()
    while pressed_key not in exit_keys:

        if pressed_key in build_keys:
            qtree.construct(points)
            tree_built = True
            segments = draw_construction(qtree.visualisation, points, d, win_size_x, win_size_y, wait=True)

        elif pressed_key in fast_build:
            qtree.construct(points)
            tree_built = True
            for step in qtree.visualisation:
                if step['type'] == 'bedges':
                    segment1, segment2 = step['value']
                    segments.append(segment1)
                    segments.append(segment2)

            redraw_tree(d, [], points, segments)

        elif pressed_key in search_keys:
            if tree_built:
                qtree.query(*search_range)

                draw_search_range(search_range, d)
                redraw_tree(d, [], points, segments)
                d.wait_for_click()

                b = None
                result_points = []
                for step in qtree.query_visualisation:
                    if step['type'] == 'point':
                        point = step['value']
                        result_points.append(point)
                        d.draw_point(point, radius=3, color=d.color(69, 23, 162))
                    elif step['type'] == 'boundary':
                        boundary = step['value']
                        p1 = boundary.x1, boundary.y1
                        p2 = boundary.x2, boundary.y2
                        draw_search_range(search_range, d)
                        b = d.draw_rectangle(p1, p2)
                        redraw_query_points(d, result_points, points)
                        draw_segments(segments, d)
                    elif step['type'] == 'boundary_separate':
                        boundary = step['value']
                        p1 = boundary.x1, boundary.y1
                        p2 = boundary.x2, boundary.y2
                        draw_search_range(search_range, d)
                        d.draw_rectangle(p1, p2, fill_color=d.color(135, 74, 74))
                        print_help(d, win_size_y)
                        redraw_query_points(d, result_points, points)
                        # for p in points:
                        #     d.draw_point(p, radius=3, color="green")
                        draw_segments(segments, d)
                    if b:
                        d.wait_for_click()
                        d.remove(b)
                        b = None
                    d.wait_for_click()

        elif pressed_key in coord_system:
            d.draw_coordinate_system()

        pressed_key = d.get_pressed_key()

    d.shutdown()