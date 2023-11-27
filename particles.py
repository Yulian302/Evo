from functions import *


def particles_method(func, n, n_particles: int, bounds_, epochs=100, w=0.7, phi_p=0.6, phi_g=0.6):
    particles = np.array([
        [np.random.uniform(bounds_[n_][0], bounds_[n_][1]) for n_ in range(n)] for _ in range(n_particles)
    ])
    v = np.zeros(shape=(n_particles, n))
    p = np.zeros(shape=(n_particles, n))
    best_overall = particles[0]
    for p_, i in zip(particles, range(n_particles)):
        p[i] = p_
        if func(p[i]) < func(best_overall):
            best_overall = p[i]
        v[i] = np.random.uniform(bounds_[0][0] - bounds_[0][1], bounds_[0][1] - bounds_[0][0])
    for _ in range(epochs):
        for particle, i in zip(particles, range(n_particles)):
            rp, rg = np.array([
                np.random.uniform(0, 1) for _ in range(n)
            ]), np.array([
                np.random.uniform(0, 1) for _ in range(n)
            ])
            v[i] = w * v[i] + phi_p * rp * (p[i] - particle) + phi_g * rg * (best_overall - particle)
            particle += v[i]
            if func(particle) < func(p[i]):
                p[i] = particle
                if func(p[i]) < func(best_overall):
                    best_overall = p[i]
    return np.round(best_overall), func(best_overall)


bounds = [(-5, 5), (-5, 5)]
solution = particles_method(echli_function, 2, 10, bounds, epochs=40)
print(solution)
