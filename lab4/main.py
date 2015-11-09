__author__ = 'piotr'

from lab4.display.graphics_wrapper import Drawer
from lab4.point import Point

def get_mouse_scaled(drawer, win_size_x, win_size_y, x_range, y_range):
        point = drawer.get_mouse_click()
        new_x = 2 * x_range * point[0] / win_size_x - x_range
        new_y = 2 * y_range * (win_size_y - point[1]) / win_size_y - y_range
        return new_x, new_y


def orient(a, b, c):
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)


def classify(points):

    #go counterclockwise
    max_y = max(points, key=lambda p: p.y)


def monotonic(points):
    pass


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

    points = []
    prev_point = None
    current_point = get_mouse_scaled(*scale_arguments)

    while not prev_point or click_difference(prev_point, current_point, click_epsilon):
        d.draw_point(current_point, color="blue")
        points.append(current_point)
        prev_point = current_point
        current_point = get_mouse_scaled(*scale_arguments)

        d.draw_line(current_point, prev_point)

    d.draw_line(points[-1], points[0])

    d.wait_for_key_pressed()
    d.shutdown()


if __name__ == "__main__":

    #counterclockwise -> det > 0

    x_ax = 10
    y_ax = 10
    click_epsilon = 0.01
    draw()