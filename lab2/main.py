__author__ = 'piotr'

import random
import math
import time
from matplotlib import pyplot as plt
from primitives import *
from plots import *
import solvers_no_animation
import matplotlib.animation as manimation



def generate_points_A(n, lowerBound, upperBound):
    points = []
    for i in range(n):
        x = random.uniform(lowerBound, upperBound)
        y = random.uniform(lowerBound, upperBound)
        points.append(Point(x, y, 'b'))
    return points


def generate_points_B(n, x0, y0, R):
    points = []
    for i in range(n):
        alpha = random.uniform(0, 2*math.pi)
        x = R*math.cos(alpha) + x0
        y = R*math.sin(alpha) + y0
        points.append(Point(x, y, 'b'))
    return points


def generate_points_C(n, vertices):

    points = []
    for i in range(n):
        edge = random.randint(0, len(vertices)-1)
        point1 = vertices[edge]
        point2 = vertices[(edge+1) % len(vertices)]
        x = random.uniform(point1.x, point2.x)
        y = random.uniform(point1.y, point2.y)
        points.append(Point(x, y, 'b'))

    return points


def generate_points_D(bottomLeft, bottomRight, topLeft, topRight, perAxPoints, perDiagonalPoints):

    points = [bottomLeft, bottomRight, topLeft, topRight]

    ax_points = [[bottomLeft, bottomRight], [bottomLeft, topLeft]]
    for vertex_pair in ax_points:
        for i in range(perAxPoints):
            point1 = vertex_pair[0]
            point2 = vertex_pair[1]
            x = random.uniform(point1.x, point2.x)
            y = random.uniform(point1.y, point2.y)
            points.append(Point(x, y, 'b'))

    diagonal_points = [[bottomLeft, topRight], [bottomRight, topLeft]]
    index = 0
    for vertex_pair in diagonal_points:
        index += 1
        for i in range(perDiagonalPoints):
            point1 = vertex_pair[0]
            point2 = vertex_pair[1]
            x = random.uniform(point1.x, point2.x)
            y = x if index == 1 else -x + point2.y
            points.append(Point(x, y, 'b'))

    return points


def generate():

    A = generate_points_A(n=100, lowerBound=-100, upperBound=100)
    B = generate_points_B(n=100, x0=0, y0=0, R=10)

    vertexA = Point(-10, 10, 'b')
    vertexB = Point(-10, -10, 'b')
    vertexC = Point(10, -10, 'b')
    vertexD = Point(10, 10, 'b')
    C = generate_points_C(100, [vertexA, vertexB, vertexC, vertexD])

    D = generate_points_D(bottomLeft=Point(0, 0, 'b'),
                          bottomRight=Point(10, 0, 'b'),
                          topLeft=Point(0, 10, 'b'),
                          topRight=Point(10, 10, 'b'),
                          perAxPoints=25,
                          perDiagonalPoints=20)

    return (A, B, C, D)


def save_result_to_file(points, filename):
    with open(filename, 'w') as f:
        for point in points:
            f.write(str(point.x) + ',' + str(point.y))
            f.write('\n')


def orient(a, b, c):
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)


def dist(a, b):
    return (a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y)


def takeFurthest(points, relativePoint):
    max_dist = dist(relativePoint, points[0])
    max_point = points[0]
    for point in points[1:]:
        current_dist = dist(relativePoint, point)
        if current_dist > max_dist:
            max_dist = current_dist
            max_point = point
    return max_point


def takeFurthestByY(points):
    max_point = points[0]
    for point in points[1:]:
        if point.y > max_point.y:
            max_point = point
    return max_point


def qsort(points, relativePoint, epsilon):
    if not points:
        return []
    else:
        pivot = points[0]
        equals = [x for x in points[1:] if abs(orient(relativePoint, x, pivot)) <= epsilon]
        less   = [x for x in points     if orient(relativePoint, x, pivot) > epsilon]
        more   = [x for x in points[1:] if orient(relativePoint, x, pivot) < -epsilon]
        if equals:
            equals.append(pivot)
            pivot = takeFurthest(equals, relativePoint)
        return qsort(less, relativePoint, epsilon) + [pivot] + qsort(more, relativePoint, epsilon)


def find_min(points):
    min_point = points[0]
    for point in points:
        if point.y < min_point.y:
            min_point = point
        elif point.y == min_point.y:
            if point.x < min_point.x:
                min_point = point
    return Point(min_point.x, min_point.y, 'r')


def graham_solver(input_points, epsilon=0):

    if len(input_points) < 3:
        return input_points

    min_point = find_min(input_points)
    plot.add(min_point)
    plot.step()
    input_points.remove(min_point)

    points = qsort(input_points, min_point, epsilon)

    p1 = points.pop(0)
    p1.color = 'r'
    p2 = points.pop(0)
    p2.color = 'r'
    stack = [min_point, p1, p2]

    plot.add_all(stack)
    line_stack = [Line(min_point.x, min_point.y, p1.x, p1.y, 'r'),
                  Line(p1.x, p1.y, p2.x, p2.y, 'r')]
    plot.add_all(line_stack)
    plot.step()

    last_point = min_point
    for current_point in points:
        while orient(stack[-2], stack[-1], current_point) <= epsilon:
            stack.pop()
            line_stack.pop()
            plot.add_all(stack)
            plot.add_all(line_stack)
            plot.step()

        last_point = current_point
        line_stack.append(Line(current_point.x, current_point.y, stack[-1].x, stack[-1].y, 'r'))
        current_point.color = 'r'
        stack.append(current_point)
        plot.add_all(stack)
        plot.add_all(line_stack)
        plot.step()

    line_stack.append(Line(min_point.x, min_point.y, last_point.x, last_point.y, 'r'))
    plot.add_all(stack)
    plot.add_all(line_stack)
    plot.step()

    return stack


def find_point_with_min_angle(points, reference_point, epsilon):
    result = reference_point
    for r in points:
        t = orient(reference_point, result, r)
        if t < epsilon or (abs(t) <= epsilon) and dist(reference_point, r) > dist(reference_point, result):
            result = r
    return result


def jarvis_solver(input_points, epsilon=0):

    if len(input_points) < 3:
        return input_points

    min_point = find_min(input_points)
    plot.add(min_point)
    plot.step()
    stack = [min_point]
    lines_stack = []
    next_point = find_point_with_min_angle(input_points, stack[0], epsilon)
    next_point.color = 'r'
    stack.append(next_point)
    lines_stack.append(Line(stack[-1].x, stack[-1].y, stack[-2].x, stack[-2].y, 'r'))
    plot.add_all(lines_stack)
    plot.step()

    while next_point != stack[0]:
        next_point = find_point_with_min_angle(input_points, stack[-1], epsilon)
        next_point.color = 'r'
        stack.append(next_point)
        lines_stack.append(Line(stack[-1].x, stack[-1].y, stack[-2].x, stack[-2].y, 'r'))

        plot.add_all(stack)
        plot.add_all(lines_stack)
        plot.step()

    return stack


def draw_static():
    data = [
            {"label": "A", "data": A},
            {"label": "B", "data": B},
            {"label": "C", "data": C},
            {"label": "D", "data": D}
            ]

    fig = plt.gcf()
    fig.set_size_inches(6, 6)

    for d in data:
        start = time.time()
        solvers_no_animation.jarvis_solver(points)
        end = time.time()
        jarvis_execution_time = end - start

        start = time.time()
        solvers_no_animation.graham_solver(points)
        end = time.time()
        graham_execution_time = end - start

        print 'Graham execution time for points', d['label'], ':', graham_execution_time
        print 'Jarvis execution time for points', d['label'], ':', jarvis_execution_time

        graham_solution = graham_solver(d['data'], epsilon = 0)
        save_result_to_file(graham_solution, 'graham'+d['label']+'.txt')

        plott = Plot()

        for p in d['data']:
            # pts.append([p.x, p.y])
            p.color = 'b'

        plott.add_all(d['data'])

        s = []
        f = graham_solution[0]
        for p in graham_solution[1:]:
            s.append(Line(f.x, f.y, p.x, p.y, 'r'))
            f = p

        pts = []
        for p in graham_solution:
            p.color = 'r'
            pts.append(p)

        first_point = graham_solution[0]
        last_point = graham_solution[-1]
        s.append(Line(first_point.x, first_point.y, last_point.x, last_point.y, 'r'))
        plott.add_all(s)
        plott.add_all(pts)
        plott.draw()
        plt.savefig('/home/piotr/Projects/go/lab2/images/graham_'+d['label']+'.png')


def animate(points, jarvis=False):

    pts = []
    for p in points:
        pts.append([p.x, p.y])

    solution = jarvis_solver(points, epsilon=0) if jarvis else graham_solver(points, epsilon=0)

    plt.scatter(*zip(*pts))

    fig = plt.gcf()
    fig.set_size_inches(6, 6)

    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title='Convex Hull', artist='PO',)
    writer = FFMpegWriter(metadata=metadata)

    ani = plot.draw(interval=interval)
    ani.save('/home/piotr/Projects/go/lab2/images/A_jarvis.mp4', writer=writer, extra_args=['-vcodec', 'libx264'])
    plot.show()


plot = AnimatedPlot()
plt.xlabel('X')
plt.ylabel('Y')

interval = 400

(A, B, C, D) = generate()
points = A
animate(points, jarvis=False)

# draw_static()