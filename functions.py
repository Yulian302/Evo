import numpy as np
import math
import matplotlib.pyplot as plt


def echli_function(x_, y_):
    return -20 * np.exp(-0.2 * np.sqrt(0.5 * (x_ ** 2 + y_ ** 2))) - \
        np.exp(0.5 * (np.cos(2 * np.pi * x_) + np.cos(2 * np.pi * y_))) + np.e + 20


def himmelblau_function(x, y):
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


def rastrigina_function(x, y):
    a_ = 10
    return 2 * a_ + x ** 2 - a_ * np.cos(2 * np.pi * x) + y ** 2 - a_ * np.cos(2 * np.pi * y)


def izoma_func(x, y):
    return -np.cos(x) * np.cos(y) * np.exp(-((x - np.pi) ** 2) + (y - np.pi) ** 2)


def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def build_plot(x_, y_):
    plt.plot(x_, y_)
    plt.ylim(-5, 5)
    plt.show()


def distance_between_individuals(individual1, individual2):
    x1, y1 = individual1
    x2, y2 = individual2
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance
