from abc import ABC, abstractmethod


class Courier(ABC):
    WEEKLY_WORK_HOURS = 40
    SEED = 0

    def __init__(self, velocity: float, salary: float):
        self.id = None
        self.velocity = velocity
        self.salary = salary
        self.current_packages_weight = 0
        self.current_packages_volume = 0
        self.packages = list()

    def eval_salary_for_hours(self, hours: float):
        return self.salary * hours / Courier.WEEKLY_WORK_HOURS

    @abstractmethod
    def eval_full_expenses(self, distance: float, hours: float):
        pass

    @abstractmethod
    def is_package_suitable(self, package):
        pass

    def add_packages(self, packages) -> int:
        added = 0
        for package in packages:
            if self.is_package_suitable(package):
                if self.is_enough_space(package):
                    self.packages.append(package)
                    self.current_packages_volume += package.volume
                    self.current_packages_weight += package.weight
                    added += 1
                else:
                    print(f'Out of space for courier {self.id}. Skipping...')
            else:
                print(f'Current package is not suitable for courier with id {self.id}. Skipping...')
        return added

    @abstractmethod
    def is_enough_space(self, package):
        pass


class CarCourier(Courier):
    FUEL_PRICE = 54  # uah for 1 liter
    MAX_PACKAGES_WEIGHT = 240.0
    MAX_PACKAGES_VOLUME = float(8 * 50 * 50 * 40)
    CAR_FUEL_CONSUMPTION = 6.5  # avg
    SEED = 0

    def __init__(self, velocity: float, salary: float):
        super().__init__(velocity, salary)
        self.id = int('2' + str(CarCourier.SEED))
        CarCourier.SEED += 1

    # def is_space_enough(self, package):
    #     current_volume =

    def is_package_suitable(self, package):
        return package.weight <= CarCourier.MAX_PACKAGES_WEIGHT and \
            package.volume <= CarCourier.MAX_PACKAGES_VOLUME

    def is_enough_space(self, package):
        return self.current_packages_weight \
            + package.weight <= CarCourier.MAX_PACKAGES_WEIGHT \
            and self.current_packages_volume + package.volume <= CarCourier.MAX_PACKAGES_VOLUME

    # distance in km
    @staticmethod
    def eval_fuel_consumption(distance: float):
        fuel_for_one_km = CarCourier.CAR_FUEL_CONSUMPTION / 100
        return distance * fuel_for_one_km * CarCourier.FUEL_PRICE

    def eval_full_expenses(self, distance: float, hours: float):
        return self.eval_salary_for_hours(hours) + CarCourier.eval_fuel_consumption(distance)

    def __repr__(self):
        return f'Car Courier: {self.id} -> {self.packages}'


class PedestrianCourier(Courier):
    MAX_PACKAGES_WEIGHT = 30.0
    MAX_PACKAGES_VOLUME = float(50 * 50 * 40)
    SEED = 0

    def __init__(self, velocity: float, salary: float):
        super().__init__(velocity, salary)
        self.id = int('1' + str(PedestrianCourier.SEED))
        PedestrianCourier.SEED += 1

    def eval_full_expenses(self, distance: float, hours: float):
        return self.eval_salary_for_hours(hours)

    def is_package_suitable(self, package):
        return (package.weight <= PedestrianCourier.MAX_PACKAGES_WEIGHT and
                package.volume <= PedestrianCourier.MAX_PACKAGES_WEIGHT)

    def is_enough_space(self, package):
        return self.current_packages_weight \
            + package.weight <= PedestrianCourier.MAX_PACKAGES_WEIGHT \
            and self.current_packages_volume + package.volume <= PedestrianCourier.MAX_PACKAGES_VOLUME

    def __repr__(self):
        return f'Pedestrian Courier: {self.id} -> {self.packages}'


def generate_couriers(n_pedestrian, n_car, pedestrian_vel, car_vel, pedestrian_salary, car_salary) -> list[Courier]:
    couriers = []
    for _ in range(n_pedestrian):
        couriers.append(PedestrianCourier(pedestrian_vel, pedestrian_salary))
    for _ in range(n_car):
        couriers.append(CarCourier(car_vel, car_salary))
    return couriers
