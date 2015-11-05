from display.graphics import *


def main():
    win = GraphWin('Back and Forth', 300, 300)
    # win.yUp() # make right side up coordinates!

    rect = Rectangle(Point(200, 90), Point(220, 100))
    rect.setFill("blue")
    rect.draw(win)
    time.sleep(1)

    cir1 = Circle(Point(40, 100), 25)
    cir1.setFill("yellow")
    cir1.draw(win)
    time.sleep(1)
    rect.undraw()

    cir2 = Circle(Point(150, 125), 25)
    cir2.setFill("red")
    cir2.draw(win)
    time.sleep(1)

    line = Line(Point(150, 125), Point(10, 10))
    # line.setFill("yellow")
    line.draw(win)
    time.sleep(1)

    for i in range(46):
        cir1.move(5, 0)
        time.sleep(.05)

    for i in range(46):
        cir1.move(-5, 0)
        time.sleep(.05)

        # win.promptClose(win.getWidth()/2, 20)


main()