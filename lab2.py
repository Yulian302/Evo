import random
import time
from functions import *
import numpy as np

x = [-5, 5]
y = [-5, 5]

j = 0


def evolutionary_strategy(goal, func, n_lambda_, mu_, type_='lambda_mu', max_generations=100, stop='iteration',
                          sigma=0.1, threshold=None):
    # parents
    population = [[random.choice(range(a[0], a[1])) for _ in range(n_lambda_)] for a in [x, y]]
    # children

    global j
    if stop != 'iteration':
        max_generations = np.inf
    min_vals = []
    n_child = []
    prev_average_values = [0] * n_lambda_
    while j < max_generations:
        children = []
        mean = 0
        for n in population:
            children_n = []
            for p in range(len(n)):
                children_parent = []
                for c in range(mu_):
                    child = n[p] + np.random.normal(mean, sigma)
                    children_parent.append(child)
                children_n.append(children_parent)
            children.append(children_n)
        # fitness
        # parents
        zipped_parents = list(zip(population[0], population[1]))
        f_parents = [func(par_x, par_y) for par_x, par_y in zipped_parents]
        zipped_ch = list(zip(children[0], children[1]))
        f_children = [func(c[0][i], c[1][i]) for c in zipped_ch for i in range(len(c[0]))]
        f_children = [f_children[i:i + mu_] for i in range(0, len(f_children), mu_)]
        if func.__name__ == 'izoma_func':
            population = []
        else:
            if j == 0:
                population = [(x_, y_) for x_, y_ in zip(population[0], population[1])] + list(population[2:])
        if type_ == 'lambda_plus_mu':
            for p_n in range(len(f_parents)):
                mixed = [f_parents[p_n]] + f_children[p_n]
                if goal == 'min':
                    best_two = sorted(mixed)[:2]
                else:
                    best_two = sorted(mixed)[-2:]

                indexes = [mixed.index(best) for best in best_two]
                for i in range(len(indexes)):
                    if indexes[i] == 0:
                        population.append(zipped_parents[f_parents.index(mixed[0])])
                    else:
                        population.append((zipped_ch[p_n][0][indexes[i] - 1], zipped_ch[p_n][1][indexes[i] - 1]))

        else:
            for p_n in range(len(f_parents)):
                if goal == 'min':
                    best_two = sorted(f_children[p_n])[:2]
                else:
                    best_two = sorted(f_children[p_n])[-2:]
                indexes = [f_children[p_n].index(best) for best in best_two]

                population.append((zipped_ch[p_n][0][indexes[0]], zipped_ch[p_n][1][indexes[0]]))
                population.append((zipped_ch[p_n][0][indexes[1]], zipped_ch[p_n][1][indexes[1]]))
        min_vals.append(min([func(el[0], el[1]) for el in population]))
        n_child.append(len(population))

        current_average_values = [(sum(coord) / len(coord)) for coord in zip(*population)]

        if stop == 'VC':
            distances = []
            for i in range(len(population)):
                for j in range(i + 1, len(population)):
                    distance = euclidean_distance(population[i], population[j])
                    distances.append(distance)
            if all(dist > threshold for dist in distances):
                break
        elif stop == 'VF':
            differences = [abs(current_average_values[i] - prev_average_values[i]) for i in
                           range(len(current_average_values))]
            if all(diff > threshold for diff in differences):
                break

        prev_average_values = current_average_values
        j += 1
    # build_plot(range(1, len(min_vals) + 1), min_vals)
    # build_plot(N_child, min_vals)
    print(f'Population: {population}')
    f_pop = [func(p[0], p[1]) for p in population]
    if goal == 'min':
        idx = f_pop.index(min(f_pop))
    else:
        idx = f_pop.index(max(f_pop))
    print(f'X: {population[idx][0]},Y: {population[idx][1]}')
    print(f'Value: {func(population[idx][0], population[idx][1])}')


n_lambda = 20
mu = 7
start = time.time()
evolutionary_strategy('min', izoma_func, n_lambda, mu, type_='lambda_mu', max_generations=100,
                      stop='VC', sigma=0.1, threshold=0.05)
res = time.time() - start
print(f'Time is sec: {res}')
