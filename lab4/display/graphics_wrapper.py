import time

from lab4.display.graphics import GraphWin, Point, Line, Circle, Text
from lab4.point import Point as PointStruct

__author__ = 'lewap'


class Drawer:
    window = None

    def __init__(self, title, axes_sizes, window_sizes=(700, 700), frame_buffer=(5, 5)):
        self.title = title
        self.axis_x_size = axes_sizes[0]
        self.axis_y_size = axes_sizes[1]
        self.window_x_size = window_sizes[0]
        self.window_y_size = window_sizes[1]
        self.frame_x_buffer = frame_buffer[0]
        self.frame_y_buffer = frame_buffer[1]

    def start(self):
        self.window = GraphWin(self.title, self.window_x_size, self.window_y_size)  # runs graphic window

    def wait_for_click(self):
        self.window.getMouse()

    def wait_for_key_pressed(self):
        self.window.getKey()

    def get_mouse_click(self):
        result = self.window.getMouse()
        return PointStruct(result.getX(), result.getY())

    @staticmethod
    def wait_seconds(seconds):
        time.sleep(seconds)

    def shutdown(self):
        if self.window is not None:
            self.window.close()

    def draw_coordinate_system(self, scale_sizes=None, scale_line_percentage_length=0.01, color="black"):
        if scale_sizes is None:
            divisor = 10
            scale_sizes = (self.axis_x_size / divisor, self.axis_y_size / divisor)
        scale_lines_half_lengths = (
            scale_line_percentage_length * self.axis_x_size / 2,
            scale_line_percentage_length * self.axis_y_size / 2
        )
        self.draw_line((-self.axis_x_size, 0), (self.axis_x_size, 0), color=color)
        self.draw_line((0, -self.axis_y_size), (0, self.axis_y_size), color=color)

        x, y = 0, 0
        while x <= self.axis_x_size:
            a, b = (x, -scale_lines_half_lengths[1]), (x, scale_lines_half_lengths[1])
            self.draw_line(a, b, color=color)
            x += scale_sizes[0]

        x, y = 0, 0
        while x >= -self.axis_x_size:
            a, b = (x, -scale_lines_half_lengths[1]), (x, scale_lines_half_lengths[1])
            self.draw_line(a, b, color=color)
            x -= scale_sizes[0]

        x, y = 0, 0
        while y <= self.axis_y_size:
            a, b = (-scale_lines_half_lengths[0], y), (scale_lines_half_lengths[0], y)
            self.draw_line(a, b, color=color)
            y += scale_sizes[1]

        x, y = 0, 0
        while y >= -self.axis_y_size:
            a, b = (-scale_lines_half_lengths[0], y), (scale_lines_half_lengths[0], y)
            self.draw_line(a, b, color=color)
            y -= scale_sizes[1]

        self.put_text(format_number(scale_sizes[0]), (scale_sizes[0], -scale_lines_half_lengths[1]))
        self.put_text(format_number(scale_sizes[1]), (scale_lines_half_lengths[0], scale_sizes[1]))

    def draw_pixel(self, pixel, color="red"):
        scaled = self.scale_coordinates_to_window_size(pixel)
        p = Point(scaled[0], scaled[1])
        p.setOutline(color)
        p.draw(self.window)
        return p

    def draw_line(self, start_point, end_point, color="red", width=1):
        scaled_start = self.scale_coordinates_to_window_size(start_point)
        scaled_end = self.scale_coordinates_to_window_size(end_point)
        line = Line(Point(scaled_start[0], scaled_start[1]), Point(scaled_end[0], scaled_end[1]))
        line.setWidth(width)
        line.setOutline(color)
        line.draw(self.window)
        return line

    def draw_point(self, point, radius=2, color="red"):
        scaled = self.scale_coordinates_to_window_size(point)
        p = Circle(Point(scaled[0], scaled[1]), radius)
        p.setOutline(color)
        p.setFill(color)
        p.draw(self.window)
        return p

    def put_text(self, content, point, size=7, color="black"):
        scaled = self.scale_coordinates_to_window_size(point)
        text = Text(Point(scaled[0] + size, scaled[1] + size), content)
        text.setSize(size)
        text.setTextColor(color)
        text.draw(self.window)
        return text

    @staticmethod
    def remove(drawable):
        drawable.undraw()

    @staticmethod
    def set_color_of_(drawable, color):
        drawable.setOutline(color)
        drawable.setFill(color)

    def scale_coordinates_to_window_size(self, coordinates):
        x, y = coordinates[0], coordinates[1]
        window_x_extremum = self.window_x_size / 2 - self.frame_x_buffer
        window_y_extremum = self.window_y_size / 2 - self.frame_y_buffer
        scaled_x = window_x_extremum * (x / self.axis_x_size + 1) + self.frame_x_buffer
        scaled_y = window_y_extremum * (-y / self.axis_y_size + 1) + self.frame_y_buffer

        return round(scaled_x), round(scaled_y)


def format_number(number):
    return "{0:.1f}".format(number)