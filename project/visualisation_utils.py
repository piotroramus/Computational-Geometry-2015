__author__ = 'piotr'


INFINITE = 0
HORIZONTAL, VERTICAL = 1, 2


def click_difference(point1, point2, epsilon):
    x_dist = abs(point1[0] - point2[0])
    y_dist = abs(point1[1] - point2[1])
    if x_dist + y_dist > epsilon:
        return True
    return False


def draw_points_with_mouse(scale_arguments, click_epsilon=0.1):

    d, win_size_x, win_size_y, x_ax, y_ax = scale_arguments
    points = []

    prev_point = None
    current_point = get_mouse_scaled(*scale_arguments)
    while not prev_point or click_difference(prev_point, current_point, click_epsilon):
        points.append(current_point)
        d.draw_point(current_point, radius=3, color="black")
        prev_point = current_point
        current_point = get_mouse_scaled(*scale_arguments)

    return points


def get_mouse_scaled(drawer, win_size_x, win_size_y, x_range, y_range):
        point = drawer.get_mouse_click()
        new_x = 2 * x_range * point[0] / win_size_x - x_range
        new_y = 2 * y_range * (win_size_y - point[1]) / win_size_y - y_range
        return new_x, new_y
