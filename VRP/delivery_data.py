import random


def opposite_direction(direction: str):
    match direction:
        case 'r':
            return 'l'
        case 'l':
            return 'r'
        case 't':
            return 'b'
        case 'b':
            return 't'


def generate_directions(dirs_list: list[str], n_directions):
    result = [random.choice(dirs_list)]
    for _ in range(1, n_directions):
        last_direction = result[-1]
        possible_directions = [d for d in dirs_list if d != opposite_direction(last_direction)]
        result.append(random.choice(possible_directions))
    return result


def generate_distances(n_dists):
    return [random.uniform(0.1, 3) for _ in range(n_dists)]


def generate_packages_infos(n_infos):
    return [
        [random.randint(1, 60), tuple(random.randint(1, 40) for _ in range(3))] for _ in range(n_infos)
    ]


def generate_street_name():
    prefixes = ['Maple', 'Oak', 'Cedar', 'Pine', 'Main', 'Elm', 'Broad', 'High', 'Park', 'Sunset']
    suffixes = ['Street', 'Avenue', 'Boulevard', 'Lane', 'Court', 'Drive', 'Place', 'Circle']
    street_name = random.choice(prefixes) + ' ' + random.choice(suffixes) + str(random.randint(1, 100))
    return street_name


n_packages = 30
n_nodes = 15
packages_info = generate_packages_infos(n_packages)
distances = [
    generate_distances(n_nodes) for _ in range(n_packages)
]
dirs = ['r', 'l', 't', 'b']
directions = [generate_directions(dirs, n_nodes) for _ in range(len(distances))]
# street_names = [
#     'Konovaltsya 9/19',
#     'Franka 20/12',
#     'Symonenka 30/23',
#     'Banderi 30/20',
# ]
street_names = [
    generate_street_name() for _ in range(n_packages)
]
