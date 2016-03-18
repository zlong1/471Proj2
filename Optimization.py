
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import math
import random
import pylab
import numpy as np


paths = [] # List for all points traversed for displaying on the graph

#The function to optimize
#np used over math to allow for lists to be passed in, making it easier to graph
def function(x, y):
    x2 = np.power(x, 2)
    y2 = np.power(y, 2)
    r2 = np.power(np.sqrt(x2 + y2), 2)
    z = np.sin(x2 + 3 * y2) / (.1 + r2) + (x2 + 5 * y2) * np.exp(1 - r2) / 2
    return z

def func(x,y):
    return math.pow(x,2) + math.pow(y,2)

# Basic hill climbing from a given point range, then climbs until it finds a hill within range, but like... minimized. So a slump? rut?? ditch??? UNHILL!?
def hill_climb_point(function_to_optimize, step_size, xmin, xmax, ymin, ymax, x, y):
    global paths
    currentPoint = (x, y, function_to_optimize(x, y))
    while True:
        oldPoint = currentPoint
        paths.append(oldPoint)
        for x in range(-1,2):
            for y in range(-1,2):
                newX = currentPoint[0] + (x * step_size)
                newY = currentPoint[1] + (y * step_size)
                newPoint = (newX, newY, function_to_optimize(newX, newY))
                # Check if newPoint is better, and is still within domain
                if (xmin <= newX <= xmax and ymin <= newY <= ymax and newPoint[2] < currentPoint[2]):
                    currentPoint = newPoint
        if currentPoint == oldPoint:
            return currentPoint

# Calls hill_climb_point with a random point
def hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax):
    global paths
    paths= []
    randX = random.uniform(xmin, xmax)
    randY = random.uniform(ymin, ymax)
    return hill_climb_point(function_to_optimize, step_size, xmin, xmax, ymin, ymax, randX, randY)

# Calls hill_climb once, then hill_climb_point num_restarts - 1 times with a new random point each time, returns best point
def hill_climb_random_restart(function_to_optimize, step_size, num_restarts, xmin, xmax, ymin, ymax):
    currentPoint = hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax)
    for i in range(num_restarts - 1):
        newPoint = hill_climb_point(function_to_optimize, step_size, xmin, xmax, ymin, ymax, random.uniform(xmin, xmax), random.uniform(ymin, ymax))
        if newPoint[2] < currentPoint[2]:
            currentPoint = newPoint
    return currentPoint

#Simulated annealing minimization, starts at max_temp and looks in range +- step_size for new points
#Moves to better point always, maybe moves to worse point anyway
def simulated_annealing(function_to_optimize, step_size, max_temp, xmin, xmax, ymin, ymax):
    global paths
    paths = []
    randX = random.uniform(xmin, xmax)
    randY = random.uniform(ymin, ymax)
    currentPoint = (randX, randY, function_to_optimize(randX, randY))
    temp = max_temp
    paths.append(currentPoint)
    unchangedCount = 0
    bestPoint = currentPoint

    #Continue until 100 passes without change, or temp is very very tiny. Latter was added because infinitely small
    #changes were being made and eventually temp got so small the probability was becoming inf instead of zero
    while unchangedCount != 100 and temp > .000000000000000000001:
        newX = random.uniform(max(xmin, currentPoint[0] - step_size), min(xmax, currentPoint[0] + step_size))
        newY = random.uniform(max(ymin, currentPoint[0] - step_size), min(ymax, currentPoint[0] + step_size))
        if newY < ymin:
            newY = ymin
        if newY > ymax:
            newY = ymax
        newPoint = (newX, newY, function_to_optimize(newX, newY))
        # Always move to better points
        if newPoint[2] < currentPoint[2]:
            currentPoint = newPoint
            unchangedCount = 0
            paths.append(currentPoint)
        # Sometimes move to worse
        else:
            probability = np.exp(-(newPoint[2] - currentPoint[2]) / temp)
            randVal = random.random()
            if probability >= randVal:
                currentPoint = newPoint
                unchangedCount = 0
                paths.append(currentPoint)
            else:
                unchangedCount += 1;
        temp *= .975
        if currentPoint[2] < bestPoint[2]:
            bestPoint = currentPoint
    return bestPoint

# Graphs the given optimization function with its args in list form ie graph(hill_climb_random_restart, (function,.001,100,-2.5,2.5,-2.5,2.5))
def graph(optimization_function, args):
    returnVal = optimization_function(*args)
    global paths
    xPoints = [point[0] for point in paths]
    yPoints = [point[1] for point in paths]
    zPoints = [point[2] for point in paths]

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(-2.5, 2.5, 0.1)
    Y = np.arange(-2.5, 2.5, 0.1)
    X, Y = np.meshgrid(X, Y)
    Z = function(X,Y)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, alpha=0.3, linewidth=0, antialiased=False)

    ax.scatter(xPoints, yPoints, zPoints)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()
    return returnVal

def main():
    print hill_climb(function,.001,-2.5,2.5,-2.5,2.5)
    print hill_climb_random_restart(function,.001,100,-2.5,2.5,-2.5,2.5)
    print simulated_annealing(function, .5, 100, -2.5, 2.5, -2.5, 2.5)

    #Graphs:
    #print graph(hill_climb, (function,.001,-2.5,2.5,-2.5,2.5))
    #print graph(hill_climb_random_restart, (function,.001,100,-2.5,2.5,-2.5,2.5))
    #print graph(simulated_annealing, (function, .5, 100, -2.5, 2.5, -2.5, 2.5))

main()