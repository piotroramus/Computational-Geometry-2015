__author__ = 'piotr'

import random


def generate_random_lines(n, min_x, max_x, min_y, max_y):

    if min_x > max_x:
        raise ValueError('Max x cannot be lower than Min x')
    if min_y > max_y:
        raise ValueError('Max y cannot be lower than Min y')

    lines = []
    for i in range(n):
        x1 = random.uniform(min_x, max_x)
        x2 = random.uniform(min_x, max_x)
        y1 = random.uniform(min_y, max_y)
        y2 = random.uniform(min_y, max_y)
        lines.append([(x1, y1), (x2, y2)])

    return lines


def read_lines_from_file(filename):

    lines = []
    with open(filename) as f:
        for line in f:
            if not line.startswith('#'):
                (x1, y1, x2, y2) = line.split()
                lines.append([(float(x1), float(y1)), (float(x2), float(y2))])

    return lines


def write_lines_to_file(lines, filename):

    with open(filename, 'w') as f:
        f.write('#x1 y1 x2 y2\n')
        for line in lines:
            f.write(str(line[0][0]) + " " + str(line[0][1]) + ' ')
            f.write(str(line[1][0]) + " " + str(line[1][1]) + '\n')