import numpy as np
import matplotlib.pyplot as plt
import random


def isAdjacent(x1, y1, x2, y2):
    xv = abs(x1 - x2)
    yv = abs(y1 - y2)

    if xv + yv <= 1:
        return True
    else:
        return False


def isOutOfRange(x, y, max):
    if (x > max or y > max):
        return True
    if (x < 0 or y < 0):
        return True
    return False


def checkAdjacent(x, y, i, max):
    # check if (x[i], y[i]) is adjacent to any point in the path
    for j in range(i-2, -1, -1):
        if (isOutOfRange(x[i], y[i], max)):
            return i-1
        if (isAdjacent(x[i], y[i], x[j], y[j])):
            return j
    return i


def randomwalk2D(n, x, y, i, max):
    directions = ["UP", "DOWN", "LEFT", "RIGHT"]
    # Pick a direction at random
    step = random.choice(directions)
    # Move the object according to the direction
    if step == "RIGHT":
        x[i] = x[i - 1] + 1
        y[i] = y[i - 1]
    elif step == "LEFT":
        x[i] = x[i - 1] - 1
        y[i] = y[i - 1]

    elif step == "UP":
        x[i] = x[i - 1]
        y[i] = y[i - 1] + 1
    elif step == "DOWN":
        x[i] = x[i - 1]
        y[i] = y[i - 1] - 1

    adjacent = checkAdjacent(x, y, i, max)
    x[adjacent+1:] = np.zeros(n-adjacent-1)
    y[adjacent+1:] = np.zeros(n-adjacent-1)
    i = adjacent
    i += 1

    # Return all the x and y positions of the object
    return i


# x = np.zeros(50)
# y = np.zeros(50)
# randomwalk2D(50, x, y, 30)
# plt.plot(x, y)
# plt.show()
