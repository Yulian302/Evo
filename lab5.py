from functions import *
import time
import random
from labone_utils import *

ab1 = [-5, 5]
ab2 = [-5, 5]


def calculate_neighbour_source_v(source, random_source, a):
    x_v = source[0] + (source[0] - random_source[0]) * random.uniform(-a, a)
    y_v = source[1] + (source[1] - random_source[1]) * random.uniform(-a, a)
    return (x_v, y_v)


def calculate_profit(point, func):
    return func(*point)


def bees_optimization(func, m, ab1, a=0.1, max_iterations=100, tolerance=0.00001, stop='IT'):
    # bees-scouts
    bees_scouts = [(ab1[0] + random.random() * (ab1[1] - ab1[0]), ab1[0] + random.random() * (ab1[1] - ab1[0])) for _ in
                   range(m)]
    previous_population = []
    if stop != 'IT':
        max_iterations = 99999999999999
    for _ in range(max_iterations):
        previous_population = list(bees_scouts)
        # bees-workers
        for i in range(len(bees_scouts)):
            k = random.choice(range(len(bees_scouts)))
            x_k = bees_scouts[k]
            v_ij = calculate_neighbour_source_v(bees_scouts[i], x_k, a)
            v_i_fit = calculate_profit(v_ij, func)
            x_i_fit = calculate_profit(bees_scouts[i], func)
            chosen = v_ij if v_i_fit < x_i_fit else bees_scouts[i]
            bees_scouts[i] = chosen

        # onlooker-bees
        total_fitness = sum(calculate_profit(bees_scout, func) for bees_scout in bees_scouts)
        onlooker_bees = []

        for i in range(len(bees_scouts)):
            p = calculate_profit(bees_scouts[i], func) / total_fitness
            if random.random() < p:
                onlooker_bees.append(bees_scouts[i])

        for i in range(len(onlooker_bees)):
            k = random.choice(range(len(bees_scouts)))
            x_k = bees_scouts[k]
            v_i = calculate_neighbour_source_v(onlooker_bees[i], x_k, a)
            x_i_fit = calculate_profit(onlooker_bees[i], func)
            v_i_fit = calculate_profit(v_i, func)
            chosen_new = v_i if x_i_fit < v_i_fit else onlooker_bees[i]
            onlooker_bees[i] = chosen_new
        if stop == 'VC':
            try:
                fitness_change = abs(func(*chosen) - func(*chosen_new))
            except:
                fitness_change = 99
            if fitness_change < tolerance:
                break
        elif stop == 'VF':
            current_population = bees_scouts
            previous_average = sum(func(x, y) for x, y in previous_population) / len(previous_population)
            current_average = sum(func(x, y) for x, y in current_population) / len(current_population)

            if abs(current_average - previous_average) < tolerance:
                break

    best_solution = min(bees_scouts, key=lambda x: calculate_profit(x, func))
    best_fitness = calculate_profit(best_solution, func)
    return best_solution, best_fitness


n = 2
M = 40
funcs = [echli_function, himmelblau_function, rastrigina_function]
features = ['IT', 'VC', 'VF']
columns = ['X', 'Y', 'Z', 'Time']

for m in range(len(funcs)):
    func_res = []
    times = []
    for i in range(len(features)):
        start = time.time()
        func_res.append(bees_optimization(funcs[i], M, ab1, a=0.7, max_iterations=100, stop=features[i],
                                          tolerance=0.00001))
        times.append(time.time() - start)
    df = create_dataframe(features, columns,
                          data=[(func_res[q][0][0], func_res[q][0][1], func_res[q][1], times[q]) for q in
                                range(len(features))])
    print(df)
