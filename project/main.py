from project.kdtree_visualisation import visualise as visualise_kdtree
from project.quadtree_visualisation import visualise as visualise_quadtree
from project.tests.execution_time_tests import test
import sys


if __name__ == "__main__":

    test()

    search_range = -5, 5, -5, 5

    if len(sys.argv) > 1:
        if sys.argv[1] == 'kdtree':
            visualise_kdtree(search_range)
        elif sys.argv[1] == 'qtree':
            visualise_quadtree(search_range)
