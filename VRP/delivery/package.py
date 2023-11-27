from operator import mul
from VRP.delivery.route import Route
from functools import reduce


class Package:
    # weight in kilos
    # params in cm
    def __init__(self, weight: float, params: tuple, address: Route):
        self.weight = weight
        self.params = params
        self.address = address

    @property
    def volume(self):
        return reduce(mul, self.params)

    def __repr__(self):
        return f'Package: {self.weight}kg {[str(param) + "cm" for param in self.params]} -> {self.address}'


def generate_package_system(packages_info: tuple[float, (float, float, float)],
                            routes: list[Route]) -> list[Package]:
    if len(packages_info) != len(routes):
        raise Exception("Each package must have one route")
    packages_system = []
    for (weight, params), route in zip(packages_info, routes):
        packages_system.append(Package(weight, params, route))
    return packages_system
