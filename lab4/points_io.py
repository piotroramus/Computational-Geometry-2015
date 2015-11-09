__author__ = 'piotr'


def write_points_to_file(points, filename):
    with open(filename, 'w') as f:
        for point in points:
            f.write(str(point[0]) + "," + str(point[1]) + "\n")


def read_points_from_file(filename):
    points = []
    with open(filename) as f:
        for line in f:
            x, y = line.split(',')
            points.append((float(x), float(y)))
    return points
