import random
from functions import *


def simulated_annealing(func, n, n_cycles_, m_cycles_, c_, t_, beta_, bounds):
    x_init = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(n)]
    x_init.append(func(x_init, n))
    # n cycles
    for i in range(n_cycles_):
        # m challenges
        for j in range(m_cycles_):
            # new vector
            new_vector = [el + random.random() - 0.5 for el in x_init[:-1]]
            new_vector = [max(min(el, bounds[i][1]), bounds[i][0]) for i, el in enumerate(new_vector)]
            f_new = func(new_vector, n)
            delta_f = abs(f_new - x_init[-1])

            if f_new < x_init[-1]:
                x_init = [*new_vector, f_new]
            else:
                r_ = random.uniform(0, 1)
                P = math.exp(-1 * delta_f / (c_ * t_))
                if r_ < P:
                    x_init = [*new_vector, f_new]

        t_ *= beta_

    return x_init[:-1], func(x_init, n=n)


def rossenblock(vect, n):
    sum_ = 0
    for i in range(n - 1):
        sum_ += 100 * (vect[i + 1] - vect[i] ** 2) ** 2 + (1 - vect[i]) ** 2
    return sum_


t = 100
c = 0.001
beta = 0.99
n_cycles = 500
m_cycles = 400
bounds = [(-5, 5), (-5, 5)]
bounds_rossenblock = [(-5.12, 5.12), (-5.12, 5.12), (-5.12, 5.12), (-5.12, 5.12), (-5.12, 5.12)]
res = simulated_annealing(himmelblau_function, bounds=bounds_rossenblock, n=2, n_cycles_=n_cycles, m_cycles_=m_cycles,
                          c_=c,
                          t_=t,
                          beta_=beta)
print(res)
