import pandas as pd
import random


class Ant:
    def __init__(self, start_city):
        self.start_city = start_city
        self.route = [start_city]
        self.visited_cities = {start_city}
        self.distance = 0.0

    def add_city(self, city):
        self.route.append(city)
        self.visited_cities.add(city)

    def has_unvisited_cities(self):
        return len(self.visited_cities) < len(distance_matrix)

    def calculate_ant_distance(self, distance_matrix):
        self.distance = 0.0
        for i in range(len(self.route) - 1):
            current_city = self.route[i]
            next_city = self.route[i + 1]
            self.distance += distance_matrix[current_city][next_city]

    @property
    def path(self):
        return self.route


def update_pheromone(ants, pheromone, method, rho, min_pheromone, max_pheromone, q0=None):
    best_ant = min(ants, key=lambda ant: ant.distance)
    best_distance = best_ant.distance

    for i in range(len(pheromone)):
        for j in range(len(pheromone[i])):
            pheromone[i][j] *= (1.0 - rho)  # Pheromone evaporation

            if i != j:
                if method == "acs" or method == "mmas":
                    pheromone[i][j] += rho * best_distance / best_ant.distance  # Global update

                pheromone[i][j] = max(min_pheromone, min(max_pheromone, pheromone[i][j]))  # Pheromone bounds

    return pheromone


def aco(distance_matrix, num_ants, iterations, pheromone_evaporation, alpha, beta, method="acs", q0=None,
        min_pheromone=1e-6, max_pheromone=8.0, rho=0.05, start_city=6):
    pheromone = [[1.0] * len(distance_matrix) for _ in range(len(distance_matrix))]

    best_distance = float('inf')
    best_path = None

    for _ in range(iterations):
        ants = generate_ants(num_ants, distance_matrix, pheromone, alpha, beta, start_city=start_city, q0=q0,
                             method=method)

        for ant in ants:
            if ant.distance < best_distance:
                best_distance = ant.distance
                best_path = ant.path

        pheromone = update_pheromone(ants, pheromone, method=method, rho=pheromone_evaporation,
                                     min_pheromone=min_pheromone,
                                     max_pheromone=max_pheromone)
        evaporate_pheromone(pheromone, pheromone_evaporation)

    return best_distance, best_path


def select_next_city(ant, pheromone, alpha_, beta_, q0=None):
    current_city = ant.address[-1]  # Get the current city of the ant
    unvisited_cities = [city for city in range(len(pheromone)) if city not in ant.visited_cities]

    # Calculate the probability of selecting each unvisited city
    probabilities = []
    total_probability = 0.0

    if q0 is not None and 0 <= q0 <= 1:
        # ACS
        if random.random() < q0:
            for city in unvisited_cities:
                pheromone_level = pheromone[current_city][city]
                distance = 1.0 / distance_matrix[current_city][city]
                probability = (pheromone_level ** alpha_) * (distance ** beta_)
                probabilities.append(probability)
                total_probability += probability
        else:
            for city in unvisited_cities:
                pheromone_level = pheromone[current_city][city]
                distance = 1.0 / distance_matrix[current_city][city]
                probability = (pheromone_level ** alpha_) * (distance ** beta_)
                probabilities.append(probability)
                total_probability += probability
    else:
        # AC method (default)
        for city in unvisited_cities:
            pheromone_level = pheromone[current_city][city]
            distance = 1.0 / distance_matrix[current_city][city]
            probability = (pheromone_level ** alpha_) * (distance ** beta_)
            probabilities.append(probability)
            total_probability += probability

    # Normalize the probabilities
    normalized_probabilities = [prob / total_probability for prob in probabilities]

    # Choose the next city based on the probabilities
    selected_city = random.choices(unvisited_cities, weights=normalized_probabilities)[0]

    return selected_city


def calculate_ant_distance(ant, distance_matrix):
    total_distance = 0.0
    for i in range(len(ant.address) - 1):
        current_city = ant.address[i]
        next_city = ant.address[i + 1]
        total_distance += distance_matrix[current_city][next_city]
    ant.distance = total_distance


def generate_ants(num_ants, distance_matrix, pheromone, alpha, beta, start_city, q0=None, method="default"):
    ants = []

    for _ in range(num_ants):
        ant = Ant(start_city)
        while ant.has_unvisited_cities():
            next_city = select_next_city(ant, pheromone, alpha, beta, q0)
            ant.add_city(next_city)
        calculate_ant_distance(ant, distance_matrix)
        ants.append(ant)

    return ants


def evaporate_pheromone(pheromone, evaporation_rate):
    # Pheromone evaporation
    for i in range(len(pheromone)):
        for j in range(len(pheromone[i])):
            pheromone[i][j] *= (1 - evaporation_rate)


# Algorithm parameters
distance_matrix = []

cities_df = pd.read_csv('lab4.csv', sep=';')
for c in range(1, 26):
    distance_matrix.append(cities_df[str(c)].values)

num_ants = 100
iterations = 100
pheromone_evaporation = 0.00001
alpha = 0.3
beta = 2.0

best_distance, best_path = aco(distance_matrix, num_ants, iterations, pheromone_evaporation, alpha, beta,
                               method="acs", start_city=6)
print("Shortest path (AS):", best_path)
print("Shortest distance:", best_distance)

best_distance, best_path = aco(distance_matrix, num_ants, iterations, pheromone_evaporation, alpha, beta,
                               method="acs", q0=0.1, start_city=6)
print("Shortest path (ACS):", best_path)
print("Shortest distance:", best_distance)

best_distance, best_path = aco(distance_matrix, num_ants, iterations, pheromone_evaporation, alpha, beta,
                               method="mmas", start_city=6, min_pheromone=1e-6, max_pheromone=8.0, rho=0.05)
print("Shortest path (MMAS):", best_path)
print("Shortest distance:", best_distance)
