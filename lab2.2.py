from functions import *
import random
import time
from lab2 import x, y

n_lambda = 20
F = 1
CR = 0.7
start = time.time()
best_solution = differential_evolution(echli_function, n_lambda, F, CR,
                                       max_generations=300, stop='iteration', stop_value=0.05)
res = time.time() - start
print(f'Time in seconds: {res}')
print(f'Best solution: {best_solution}, f(x, y): {echli_function(best_solution[0], best_solution[1])}')
