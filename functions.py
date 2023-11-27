import numpy as np
import math
import matplotlib.pyplot as plt


def rastrigina_func(vect, n=3):
    a = 10
    sum_ = 0
    for i in range(n):
        sum_ += vect[i] ** 2 - a * np.cos(2 * np.pi * vect[i])
    return a * n + sum_


def echli_function(vect, n=2):
    return -20 * np.exp(-0.2 * np.sqrt(0.5 * (vect[0] ** 2 + vect[1] ** 2))) - \
        np.exp(0.5 * (np.cos(2 * np.pi * vect[0]) + np.cos(2 * np.pi * vect[1]))) + np.e + 20


def himmelblau_function(vect, n=2):
    return (vect[0] ** 2 + vect[1] - 11) ** 2 + (vect[0] + vect[1] ** 2 - 7) ** 2


def izoma_func(vect, n=None):
    return -np.cos(vect[0]) * np.cos(vect[1]) * np.exp(-((vect[0] - np.pi) ** 2) + (vect[1] - np.pi) ** 2)


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
