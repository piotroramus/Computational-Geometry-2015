__author__ = 'piotr'

from segments_io import *
from point import Point
from utils import *
from sweeping import sweep


def test_algorithm():
    number_of_tests = 4
    for i in range(1, number_of_tests + 1):
        input_file = "alg_test/test_lines" + str(i) + ".txt"
        expected_output_file = "alg_test/expected_output" + str(i) + ".txt"
        test_algorithm_from_files(i, input_file, expected_output_file)


def test_algorithm_from_files(test_num, input_lines, expected_output_file):

    print("==================")
    print("TEST NUMBER " + str(test_num))
    expected_intersections = []
    with open(expected_output_file, 'r') as expected_output:
        for line in expected_output:
            (x, y) = line.split()
            expected_intersections.append(Point(float(x), float(y)))

    lines = read_lines_from_file(input_lines)
    segments = tuple_to_segments(lines)
    (intersections, _) = sweep(segments)

    for (seg1, seg2, point) in intersections:
        assert point in expected_intersections
        expected_intersections.remove(point)

    assert len(expected_intersections) == 0

    print("PASSED")
    print("==================")