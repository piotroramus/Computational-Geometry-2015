from project.kdtree_visualisation import visualise as visualise_kdtree
from project.quadtree_visualisation import visualise as visualise_quadtree
import sys


def print_help():
    print("Program usage: " + sys.argv[0] + " kdtree|qtree [x1 x2 y1 y2]")

if __name__ == "__main__":

    search_range = -5, 5, -5, 5
    use_kd = True

    if len(sys.argv) == 2 or len(sys.argv) == 6:
        if sys.argv[1] == 'kdtree':
            use_kd = True
        elif sys.argv[1] == 'qtree':
            use_kd = False
        else:
            print_help()
    else:
        print_help()

    if len(sys.argv) == 6:
        try:
            x1 = float(sys.argv[2])
            x2 = float(sys.argv[3])
            y1 = float(sys.argv[4])
            y2 = float(sys.argv[5])
            search_range = x1, x2, y1, y2
        except ValueError:
            print_help()
    else:
        print_help()

    if use_kd:
        visualise_kdtree(search_range)
    else:
        visualise_quadtree(search_range)
