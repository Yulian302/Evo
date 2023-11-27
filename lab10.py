import numpy as np
import time
from labone_utils import create_dataframe
import itertools
from functions import *
import random


def fractal_optimization(func, n, n_hyperspheres=10, temp=100, epochs=100):
    def form_pairs(arr):
        all_pairs = list(itertools.combinations(arr, 2))
        np.random.shuffle(all_pairs)
        return all_pairs

    def generate_offsprings(parent, r, alpha):
        offsprings = []
        for _ in range(7):
            k = random.choice(range(n))
            random_vect = parent.copy()
            for n_ in range(n):
                if n_ != k:
                    random_vect[n_] = random.uniform(parent[n_] - r, parent[n_] + r)
            sum_ = sum([(random_vect[n_] - parent[n_]) ** 2 for n_ in range(n) if n_ != k])
            random_vect[k] = parent[k] + random.uniform(-1, 1) * (r ** 2 - sum_)
            offsprings.append(random_vect)
        return np.array(offsprings)

    bounds = [(-5, 5), (-5, 5), (-5, 5)]  # Update with your bounds

    t = 1
    p_t = np.random.uniform(bounds[0][0], bounds[0][1], size=(n_hyperspheres, n))
    fitness = np.array([func(p) for p in p_t])
    r = 1 / n_hyperspheres
    pv = np.array([])

    for _ in range(epochs):
        for j in range(n_hyperspheres):
            r = r / (t + 1)
            offsprings = generate_offsprings(p_t[j], r, 1)  # Adjust alpha if needed
            pv = np.concatenate((pv.reshape(-1, n), offsprings, [p_t[j]]))

        selected_pairs = form_pairs(pv)[:2 * n]
        pc = []
        for pair in selected_pairs:
            r = random.choice([-1, 1])
            q = random.randint(0, n - 1)
            a, b = pair[0], pair[1]
            c = np.where(np.arange(n) == q, (a + b) / 2, (r == -1) * a + (r == 1) * b)
            pc.append(c)

        pc = np.array(pc)
        pv = pv[np.argsort([func(sol) for sol in pv])]

        # Exploring new solutions
        f_pv_avg = np.average([func(sol) for sol in pv])
        worst_pairs = np.array(form_pairs(pv[-n * 6:]))

        p_w = []
        for w in worst_pairs.reshape(-1, n):
            rnd_coord_idx = random.choice(range(n))
            deltas = np.zeros(n)
            delta = np.random.uniform(
                w[rnd_coord_idx] - ((bounds[rnd_coord_idx][1] - bounds[rnd_coord_idx][0]) / n),
                w[rnd_coord_idx] + ((bounds[rnd_coord_idx][1] - bounds[rnd_coord_idx][0]) / n)
            )
            deltas[rnd_coord_idx] = delta
            w[rnd_coord_idx] += delta
            if func(w) > f_pv_avg or np.random.uniform(0, 1) <= np.exp(-np.min(deltas) / temp):
                p_w.append(w)

        p_w = np.array(p_w)
        p_t = np.concatenate((pv, p_w, pc))
        temp /= 2
        t += 1

    best_solution = p_t[np.argmin([func(elem) for elem in p_t])]
    return np.round(best_solution, 5), np.round(func(best_solution), 5)


funcs = [[echli_function, 2], [himmelblau_function, 2], [rastrigina_func, 3]]
features = ['E1', 'E2', 'E3']
features_vals = [10, 20, 30]
columns = ['Result', 'Time']

for m in range(len(funcs)):
    func_res = []
    times = []
    for i in range(len(features)):
        start = time.time()
        func_res.append(
            fractal_optimization(funcs[m][0], funcs[m][1], n_hyperspheres=features_vals[m], temp=100, epochs=20)
        )
        times.append(time.time() - start)

    df = create_dataframe(features, columns, [(func_res[q], times[q]) for q in range(len(features))])
    print(df)
