from functools import reduce
from operator import add


class Route:
    """
    distances: [1.5, 2.3, 4.5]
    directions: ['r', 'l', 'b']
    r - right
    l - left
    t - top
    b - bottom
    """

    def __init__(self, distances: list[float], directions: list[str]):
        if len(distances) != len(directions):
            raise Exception('Number of distances not same as directions!')
        self.route: list[tuple] = list(zip(distances, directions))

    def eval_distance(self):
        return reduce(lambda acc, pair: tuple(map(add, acc, pair)), self.route)

    def __repr__(self):
        return f'Route: {self.route}'


def generate_routes(distances: list[float], directions: list[float]) -> list[Route]:
    if len(distances) != len(directions):
        raise Exception('Number of distances not same as directions!')
    routes = []
    for dist, dir_ in zip(distances, directions):
        routes.append(Route(dist, dir_))
    return routes


class Address:
    def __init__(self, address_name: str, route: Route):
        self.name = address_name
        self.route = route

    def __repr__(self):
        return f'Address: {self.name}, dist: {self.route.eval_distance()}'


def generate_addresses(addresses: list[str], routes: list[Route]):
    return [Address(name, route) for name, route in zip(addresses, routes)]
