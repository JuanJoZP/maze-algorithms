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


def checkAdjacent(x, y, i):
    # check if (x[i], y[i]) is adjacent to any point in the path
    for j in range(i-2, -1, -1):
        if (isAdjacent(x[i], y[i], x[j], y[j])):
            return j
    return i


def randomwalk2D(n):
    # [0, 0, 0, ... ,0]
    x = np.zeros(n)
    y = np.zeros(n)
    directions = ["UP", "DOWN", "LEFT", "RIGHT"]
    i = 1
    count = 0
    while i < n:
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

        adjacent = checkAdjacent(x, y, i)
        print(step)
        print(x)
        print(y)
        print("ad", adjacent)
        print("i", i)
        x[adjacent+1:] = np.zeros(n-adjacent-1)
        y[adjacent+1:] = np.zeros(n-adjacent-1)
        print(x)
        print(y)
        i = adjacent
        i += 1

    # Return all the x and y positions of the object
    return x, y


x_data, y_data = randomwalk2D(100)
plt.title("2D Random Walk in Python")
plt.plot(x_data, y_data)
plt.show()
