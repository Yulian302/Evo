import random
from functions import *
import time
from labone_utils import *
import numpy as np


def is_within_range(point, bounds):
    is_within_range_ = True
    for i in range(len(point)):
        if not (bounds[i][0] <= point[i] <= bounds[i][1]):
            is_within_range_ = False
    return is_within_range_


def deformed_stars_method(func, bounds, n, tr_n, vertices=3, k=3, alpha=30, epochs=100, stop='IT', tolerance=0.00005):
    triangle, new_triangle = None, None
    triangles = np.asarray(
        [np.array([[random.uniform(bounds[n_][0], bounds[n_][1]) for n_ in range(n)] for v_ in range(vertices)]) for i
         in range(tr_n)])
    e = 0
    while e < epochs:
        new_triangles = []
        for triangle, t in zip(triangles, range(tr_n)):
            min_vertice = np.argmin([func(p, n=n) for p in triangle])
            new_vertice = (1 / (k - 1)) * (k * min_vertice - np.mean(triangle, axis=0))
            new_triangle = np.array([new_vertice,
                                     (1 / k) * (k - 1) * triangle[1] + new_vertice,
                                     (1 / k) * (k - 1) * triangle[2] + new_vertice])

            i, k_, l_ = random.sample(range(vertices), 3)
            rotated_triangle = triangle.copy()
            rotated_triangle[k_] = triangle[k_] * np.cos(alpha) - triangle[l_] * np.sin(alpha)
            rotated_triangle[l_] = triangle[k_] * np.sin(alpha) + triangle[l_] * np.cos(alpha)

            shrinked_triangle = triangle.copy()
            for i in range(vertices):
                if i == min_vertice:
                    continue
                shrinked_triangle[i] = (k * triangle[min_vertice] + shrinked_triangle[i]) / (1 + k)
            new_triangles.extend([new_triangle, rotated_triangle, shrinked_triangle])

        new_triangles = np.array([t for t in new_triangles if all(is_within_range(vertex, bounds) for vertex in t)])
        fitness_sorted = np.argsort(np.array([func(np.mean(p, axis=0), n=n) for p in new_triangles]))
        triangles = new_triangles[fitness_sorted][:tr_n]
        if stop == 'VC':
            end = False
            for tr in triangles:
                if np.all(np.linalg.norm(tr[:, np.newaxis, :] - tr[:, :, np.newaxis], axis=0) < tolerance):
                    end = True
            if end:
                break
        elif stop == 'VF':
            if np.abs(np.mean([func(v_) for v_ in triangle]) - np.mean([func(v_) for v_ in new_triangle])) < tolerance:
                break
        else:
            e += 1

    # F = np.array([func(*t[v_]) for t in triangles for v_ in range(vertices)])
    triangles_fl = triangles.flatten().reshape(-1, n)
    fitness = [func(p) for p in triangles_fl]
    min_fitness_idx = np.argmin(fitness)
    best_solution = triangles_fl[min_fitness_idx]
    best_fitness = fitness[min_fitness_idx]

    return np.round(best_solution, 5), round(best_fitness, 3)


funcs = [[echli_function, 2], [himmelblau_function, 2], [rastrigina_func, 9]]
features = ['IT', 'VC', 'VF']
tols_ = [0, 0.2, 0.00003]
feature_vals = [3, 4, 5]
bounds_ = [[(-5, 5), (-5, 5)], [(-5, 5), (-5, 5)],
           [(-5, 5), (-5, 5), (-5, 5), (-5, 5), (-5, 5), (-5, 5), (-5, 5), (-5, 5), (-5, 5)]]
columns = ['Result', 'Time']
for m in range(len(funcs)):
    func_res = []
    times = []
    for i in range(len(features)):
        start = time.time()
        func_res.append(deformed_stars_method(funcs[m][0], bounds=bounds_[m],
                                              n=funcs[m][1],
                                              tr_n=10,
                                              vertices=3,
                                              epochs=40,
                                              stop=features[m],
                                              tolerance=0.0003
                                              ))
        times.append(time.time() - start)
    df = create_dataframe(features, columns,
                          [(func_res[q], times[q]) for q in
                           range(len(features))])
    print(df)
