__author__ = 'piotr'

from matplotlib import pyplot as plt

currentPoints = "D"
with open('../points'+currentPoints+'.txt') as inputFile:
    points = []
    for line in inputFile:
        [x, y] = line.strip().split(';')
        points.append([x, y])
    plt.plot(*zip(*points), marker='.', color='r', ls='', markersize=1)

minx = -1000
maxx = 1000

linex1 = minx
liney1 = 0.05*minx+0.05
linex2 = maxx
liney2 = 0.05*maxx+0.05

aDesc = "10^5 points of [-100;100]"
bDesc = "10^5 points of [-10^14;10^14]"
cDesc = '1000 points on circle of (X0,Y0)=(0,0) and R=100'
dDesc = "1000 points on the line going through [-1.0;0.0] and [1.0;0.1]"

plt.xlabel('X')
plt.ylabel('Y')
plt.title(dDesc)

withLine = False

if withLine:
    plt.plot([linex1, linex2], [liney1, liney2], 'b-', lw=1)
    plt.savefig('/home/piotr/Projects/go/lab1/images/points'+currentPoints+'WithLine.png')
else:
    plt.savefig('/home/piotr/Projects/go/lab1/images/points'+currentPoints+'.png')

