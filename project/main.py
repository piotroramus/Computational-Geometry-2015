from project.kdtree_visualisation import visualise as visualise_kdtree
from project.quadtree_visualisation import visualise as visualise_quadtree


if __name__ == "__main__":

    # execution_time_test()

    search_range = -5, 5, -5, 5

    kdtree = True
    if kdtree:
        visualise_kdtree(search_range)
    else:
        visualise_quadtree(search_range)