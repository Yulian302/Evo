import random
import time
import numpy as np
from labone_utils import *


# %%funcs
def echli_function(x, y):
    return -20 * np.exp(-0.2 * np.sqrt(0.5 * (x ** 2 + y ** 2))) - \
        np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y))) + np.e + 20


def himmelblau_function(x, y):
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


def rastrigina_function(x, y):
    a_ = 10
    return 2 * a_ + x ** 2 - a_ * np.cos(2 * np.pi * x) + y ** 2 - a_ * np.cos(2 * np.pi * y)


def izoma_func(x, y):
    return -np.cos(x) * np.cos(y) * np.exp(-((x - np.pi) ** 2) + (y - np.pi) ** 2)


def calculate_average_fitness(population, func):
    fitness_values = [func(x, y) for x, y in population]

    average_fitness = sum(fitness_values) / len(fitness_values)

    return average_fitness


def calculate_neighboring_avg_fitness_values(populations, func):
    neighboring_avg_fitness = []

    for i in range(1, len(populations) - 1):
        prev_population = populations[i - 1]
        current_population = populations[i]
        next_population = populations[i + 1]

        avg_fitness_prev = calculate_average_fitness(prev_population, func)
        avg_fitness_current = calculate_average_fitness(current_population, func)
        avg_fitness_next = calculate_average_fitness(next_population, func)

        neighboring_avg_fitness.append((avg_fitness_prev, avg_fitness_current, avg_fitness_next))

    return neighboring_avg_fitness


def calculate_distance(individual1, individual2):
    x1, y1 = individual1
    x2, y2 = individual2
    distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance


def genetic_algorithm(func, population_size, num_generations, mutation_rate, crossover_rate, *,
                      crossover_type='one_dot', parents_selection='panmixia', replacement_strategy='ZV', stop='IT'):
    population = []
    min_vals = []
    for _ in range(population_size):
        x = random.uniform(ab1[0], ab1[1])
        y = random.uniform(ab2[0], ab2[1])
        population.append((x, y))

    if stop != 'IT':
        num_generations = 99999999999999

    for generation in range(num_generations):
        fitness_values = [func(x, y) for x, y in population]
        new_population = []

        if parents_selection == 'inbriding':
            parents = random.choices(population, weights=fitness_values, k=population_size)
        elif parents_selection == 'outbriding':
            parents = random.choices(population, k=population_size)
        elif parents_selection == 'panmixia':
            parents = random.choices(population + new_population, k=population_size)
        elif parents_selection == 'selective':
            parents = []
            while len(parents) < population_size:
                parent1, parent2 = random.choices(population, weights=fitness_values, k=2)
                if parent1 != parent2:
                    parents.extend([parent1, parent2])
        else:
            raise Exception("Selection method is unknown!")

        for i in range(0, population_size - 1, 2):
            if random.random() < crossover_rate:
                if crossover_type == 'one_dot':
                    crossover_point = random.randint(0, 1)
                    child1 = parents[i][:crossover_point] + parents[i + 1][crossover_point:]
                    child2 = parents[i + 1][:crossover_point] + parents[i][crossover_point:]
                elif crossover_type == 'two_dot':
                    point1 = random.randint(0, 1)
                    point2 = random.randint(point1, 1)
                    child1 = parents[i][:point1] + parents[i + 1][point1:point2] + parents[i][point2:]
                    child2 = parents[i + 1][:point1] + parents[i][point1:point2] + parents[i + 1][point2:]
                else:
                    raise Exception("Wrong crossover type!")
            else:
                child1 = parents[i]
                child2 = parents[i + 1]

            if random.random() < mutation_rate:
                mutation_index = random.randint(0, 1)
                if mutation_index == 0:
                    child1 = random.uniform(ab1[0], ab1[1]), child1[1]
                else:
                    child1 = child1[0], random.uniform(ab2[0], ab2[1])

            if random.random() < mutation_rate:
                mutation_index = random.randint(0, 1)
                if mutation_index == 0:
                    child2 = random.uniform(ab1[0], ab1[1]), child2[1]
                else:
                    child2 = child2[0], random.uniform(ab2[0], ab2[1])

            new_population.extend([child1, child2])

        if replacement_strategy == 'ZV':
            population = new_population
        elif replacement_strategy == 'VV':
            population.extend(random.sample(new_population, population_size - len(population)))
        elif replacement_strategy == 'EV':
            combined_population = list(zip(population, fitness_values))
            combined_population.extend(list(zip(new_population, [func(x, y) for x, y in new_population])))
            combined_population.sort(key=lambda x: x[1])
            # top 10% as elite individuals
            elite_size = int(0.1 * population_size)
            elites = [ind[0] for ind in combined_population[:elite_size]]
            population = random.sample(elites, elite_size)
            population.extend(random.sample(new_population, population_size - elite_size))
        else:
            raise Exception("New population selection method is wrong!")

        if stop == 'VC':
            distances_new_population = [calculate_distance(new_population[i], new_population[i + 1]) for i in
                                        range(len(new_population) - 1)]

            if all(distance < dist_threshold for distance in distances_new_population[-5:]):
                break

        if stop == 'VF':
            fitness_values_population = [func(x, y) for x, y in population]
            fitness_values_new_population = [func(x, y) for x, y in new_population]

            neighboring_avg_fitness_values = calculate_neighboring_avg_fitness_values([population, new_population],
                                                                                      func)
            if all(
                    abs(fitness1 - fitness2) < dist_threshold for fitness1, fitness2 in
                    neighboring_avg_fitness_values[-20:]):
                break

        best = sorted(list(zip(population, fitness_values)), key=lambda x: x[1])[0]
        min_vals.append(best[1])

    best_solution = min(population, key=lambda x: func(x[0], x[1]))
    best_fitness = func(best_solution[0], best_solution[1])
    fitness_vals.append(min_vals)

    print("Best Solution:", best_solution)
    print("Best Fitness:", best_fitness)
    return best_solution, best_fitness


eps = 0.005
ab1, ab2 = (-5, 5), (-5, 5)
pop_size = abs(ab1[0] - ab1[1]) // eps
dist_threshold = 1
fitness_vals = []

funcs = [echli_function, himmelblau_function, rastrigina_function]
mutations = [0.001, 0.05, 0.1]
type_ = ['one_dot', 'two_dot']
selectings_ = ['inbriding', 'outbriding', 'panmixia', 'selective']
formations = ['ZV', 'VV', 'EV']
features = ["IT", "VC", "VF"]
columns = ["X", "Y", "Z", "Time"]
for m in range(len(funcs)):
    res_ = []
    func_res = []
    for i in range(len(features)):
        start = time.time()
        func_res.append(genetic_algorithm(funcs[m], int(pop_size), 300, 0.1, 0.8, crossover_type='one_dot',
                                          parents_selection='panmixia',
                                          replacement_strategy='EV', stop='IT'))
        res = time.time() - start
        res_.append(res)
    df = create_dataframe(features, columns,
                          [(func_res[q][0][0], func_res[q][0][1], func_res[q][1], res_[q]) for q in
                           range(len(features))])
    print(df)

# genetic_algorithm(echli_function, int(pop_size), 300, 0.05, 0.8, crossover_type='two_dot',
#                   parents_selection="panmixia",
#                   replacement_strategy='ZV', stop='IT')
# genetic_algorithm(echli_function, int(pop_size), 300, 0.05, 0.8, crossover_type='two_dot',
#                   parents_selection="panmixia",
#                   replacement_strategy='VV', stop='IT')


# %% plotting
# build_plots(300, fitness_vals, [echli_function, izoma_func, himmelblau_function],
#             ('population formation', ['EV', 'ZV', 'VV']))
