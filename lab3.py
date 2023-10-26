import random
import time
from labone_utils import *

from functions import *

ab1, ab2 = (-5, 5), (-5, 5)


def symbiotic_algorithm(func, population_size, eco_size, max_iter=100, max_fit_eval=100, stop='IT', bfs=None,
                        tolerance=0.0005):
    ecosystem = [(random.uniform(ab1[0], ab1[1]), random.uniform(ab2[0], ab2[1])) for _ in range(population_size)]
    organisms = random.choices(ecosystem, k=eco_size)
    num_iter = 0
    i = 0
    organism_fits = []
    num_fit_eval = 0
    while True:
        previous_population = list(organisms)
        fitness = [func(x, y) for x, y in organisms]
        best_organism_idx = fitness.index(min(fitness))
        best_organism = organisms[best_organism_idx]
        # mutualism
        x_i = organisms[i]
        x_j = random.choice(organisms[:i] + organisms[i + 1:])
        x_j_idx = organisms.index(x_j)
        mutual_vector = ((x_i[0] + x_j[0]) / 2, (x_i[1] + x_j[1]) / 2)
        if not bfs:
            bf1 = random.choice([1, 2])
            bf2 = random.choice([1, 2])
        else:
            bf1 = bfs[0]
            bf2 = bfs[1]

        x_i_new = (x_i[0] + random.random() * (best_organism[0] - mutual_vector[0] * bf1),
                   x_i[1] + random.random() * (best_organism[1] - mutual_vector[1] * bf1))
        x_j_new = (x_j[0] + random.random() * (best_organism[0] - mutual_vector[0] * bf2),
                   x_j[1] + random.random() * (best_organism[1] - mutual_vector[1] * bf2))
        organism_fits.append(func(*x_i_new))
        organism_fits.append(func(*x_j_new))
        x_i_new_fit = func(*x_i_new)
        x_j_new_fit = func(*x_j_new)
        num_fit_eval += 2
        # check if new organisms are better (if so, then substitute)
        if x_i_new_fit < func(*x_i_new) and x_i_new_fit < func(*x_j_new):
            organisms[i] = x_i_new
            organisms[x_j_idx] = x_j_new
        else:
            x_i_new, x_j_new = None, None
        # commensalism
        x_j = random.choice(organisms[:i] + organisms[i + 1:])
        x_i_new = (x_i[0] + random.uniform(-1, 1) * (best_organism[0] - x_j[0]),
                   x_i[1] + random.uniform(-1, 1) * (best_organism[1] - x_j[1]))
        organism_fits.append(func(*x_i_new))
        num_fit_eval += 1
        if func(*x_i_new) < func(*x_i):
            organisms[i] = x_i_new
        else:
            x_i_new = None
        # parasitism
        x_j = random.choice(organisms[:i] + organisms[i + 1:])
        x_j_idx = organisms.index(x_j)
        r = random.choice([0, 1])
        if r == 0:
            parasite_vector = (x_i[0] + random.uniform(-1, 1), x_i[1])
        else:
            parasite_vector = (x_i[0], x_i[1] + random.uniform(-1, 1))

        parasite_fitness = func(*parasite_vector)
        organism_fits.append(parasite_fitness)
        num_fit_eval += 1

        if func(*parasite_vector) < func(*x_j):
            organisms[x_j_idx] = parasite_vector

        # VC
        if stop == 'VC':
            xs = [x for x, y in organisms]
            ys = [y for x, y in organisms]
            if all(abs(a - b) < tolerance for a, b in zip(xs, xs[1:])) and all(
                    abs(a - b) < tolerance for a, b in zip(ys, ys[1:])):
                return min(organisms, key=lambda organism: func(*organism))

        # VF
        elif stop == 'VF':
            current_population = organisms
            previous_average = sum(func(x, y) for x, y in previous_population) / len(previous_population)
            current_average = sum(func(x, y) for x, y in current_population) / len(current_population)

            if abs(current_average - previous_average) < tolerance:
                return min(organisms, key=lambda organism: func(*organism))

        if i == eco_size - 1:
            if stop == 'IT' and num_iter > max_iter:  # or num_fit_eval > max_fit_eval:
                return min(organisms, key=lambda organism: func(*organism))
            else:
                num_iter += 1
                i = 0
        i += 1


funcs = [echli_function, himmelblau_function, rastrigina_function]
features = ['IT', 'VC', 'VF']
columns = ['X', 'Y', 'Z', 'Time']

for m in range(len(funcs)):
    func_res = []
    times = []
    for i in range(len(features)):
        start = time.time()
        func_res.append(
            symbiotic_algorithm(funcs[m], population_size=20, eco_size=5, max_iter=100, max_fit_eval=999999999,
                                stop='IT', tolerance=0.000001))
        times.append(time.time() - start)
    df = create_dataframe(features, columns,
                          [(func_res[q][0], func_res[q][1], funcs[m](func_res[q][0], func_res[q][1]), times[q]) for q in
                           range(len(features))])
    print(df)
