from pprint import pprint
from delivery.courier import *
from delivery.package import generate_package_system
from delivery.route import generate_routes, generate_addresses
from delivery_data import *
from vrp import VRPSolution
import numpy as np
import matplotlib.pyplot as plt

# per month
PEDESTRIAN_COURIER_SALARY = 15000
CAR_COURIER_SALARY = 13000


def generate_report(solution):
    with open('./data.txt', 'w') as f:
        f.write(str(zip(str(solution.packages), str(solution.addresses))))
        f.write(str(solution.couriers))


def visualize_routes(routes):
    x, y = 0, 0
    positions = [(x, y)]

    for route in routes:
        if isinstance(route, tuple):
            distance, direction = route
            if direction == 'r':
                x += distance
            elif direction == 'l':
                x -= distance
            elif direction == 't':
                y += distance
            elif direction == 'b':
                y -= distance
            positions.append((x, y))
        elif isinstance(route, float):
            x += route
            positions.append((x, y))
    labels = ['' for _ in range(len(positions))]
    labels[0] = 'A'
    labels[-1] = 'B'
    x_values, y_values = zip(*positions)
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b')

    for label, (x, y) in zip(labels, positions):
        plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.title('Route Visualization')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.show()


def main():
    n_pedestrian_couriers = 5
    n_car_couriers = 4
    routes = generate_routes(distances, directions)
    packages = generate_package_system(packages_info, routes)
    couriers = generate_couriers(n_pedestrian_couriers, n_car_couriers, 5.0,
                                 40.0, PEDESTRIAN_COURIER_SALARY, CAR_COURIER_SALARY)

    addresses_ = generate_addresses(street_names, routes)

    vrp_solution = VRPSolution(couriers, packages, addresses_)
    print('Initial random population')
    pprint(vrp_solution.current_solution)
    vrp_solution.run_optimization(max_temp=10000, min_temp=10, num_iterations=5000)
    generate_report(vrp_solution)
    visualize_routes(vrp_solution.packages[0].address.route)


if __name__ == '__main__':
    main()
