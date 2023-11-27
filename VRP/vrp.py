import random
from pprint import pprint
from itertools import cycle
import math
from VRP.delivery.courier import CarCourier, Courier
from VRP.delivery.package import Package
from VRP.delivery.route import Address


class VRPSolution:
    def __init__(self, couriers, packages, addresses):
        self.couriers = couriers
        self.packages = packages
        self.addresses = addresses
        self.current_solution = self.initialize_solution()

    def initialize_solution(self):
        initial_solution = []
        available_couriers = list(self.couriers)
        cyclic_iterator = cycle(available_couriers)
        for package, address in zip(self.packages, self.addresses):
            if not available_couriers:
                # print("No available couriers to assign more packages. Skipping remaining packages.")
                break
            courier = next(cyclic_iterator)
            initial_solution.append(courier)
            courier.add_packages([package])

        return initial_solution

    @staticmethod
    def calculate_cost(solution: dict[Courier:[Package, Address]]):
        total_cost = 0

        for courier in solution:
            for package in courier.packages:
                dist = package.address.eval_distance()[0]
                if courier.CAR_FUEL_CONSUMPTION:
                    total_cost += courier.eval_full_expenses(dist, dist / courier.velocity)
                else:
                    total_cost += courier.eval_full_expenses(None, dist / courier.velocity)
        return total_cost

    def get_neighboring_solution(self, current_solution):
        new_solution = current_solution.copy()
        courier1, courier2 = random.sample(list(new_solution), 2)

        if courier1 not in new_solution or courier2 not in new_solution:
            # print("Invalid couriers selected for swapping. Skipping...")
            return new_solution
        if len(courier1.packages) == 0 or len(courier2.packages) == 0:
            # print("Courier without packages. Skipping")
            return new_solution

        package1 = random.choice(courier1.packages)
        package2 = random.choice(courier2.packages)

        if (courier1.is_package_suitable(package2)
            * courier2.is_package_suitable(package1)
            * courier1.is_enough_space(package2)
            * courier2.is_enough_space(package1)) == 0:
            # print("Package swap not suitable for couriers. Skipping...")
            return new_solution

        try:
            courier1.packages.remove(package1)
            courier2.packages.remove(package2)
            courier1.add_packages([package2])
            courier2.add_packages([package1])
        except:
            pass
        return new_solution

    def simulated_annealing(self, t_max, t_min, num_iterations):
        current_solution = self.current_solution
        best_solution = current_solution
        temperature = t_max
        for iteration in range(num_iterations):
            new_solution = self.get_neighboring_solution(current_solution)
            delta_cost = VRPSolution.calculate_cost(new_solution) - VRPSolution.calculate_cost(current_solution)
            if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / temperature):
                current_solution = new_solution
            if VRPSolution.calculate_cost(current_solution) < VRPSolution.calculate_cost(best_solution):
                best_solution = current_solution
            temperature = t_max - ((t_max - t_min) * iteration) / num_iterations
            if iteration % 100 == 0:
                print(
                    f'Best solution on epoch {iteration}: {VRPSolution.calculate_cost(best_solution)}, \
                    delta: {delta_cost}')

        print(f'Best solution')
        pprint(best_solution)
        return best_solution

    def run_optimization(self, max_temp, min_temp, num_iterations):
        best_solution = self.simulated_annealing(max_temp, min_temp, num_iterations)
        print("Best Solution Cost:", VRPSolution.calculate_cost(best_solution))
