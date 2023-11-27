import random

T = {'a'}
ops = {'+', '-', '*', '/'}


class Node:
    def __init__(self, value):
        self.left = None
        self.data = value
        self.right = None


def evaluateExpressionTree(root):
    if root is None:
        return 0

    if root.left is None and root.right is None:
        return root.data

    left_sum = evaluateExpressionTree(root.left)

    right_sum = evaluateExpressionTree(root.right)

    if root.data == '+':
        return left_sum + right_sum

    elif root.data == '-':
        return left_sum - right_sum

    elif root.data == '*':
        return left_sum * right_sum

    else:
        return left_sum / right_sum


def generateRoot(gen, val):
    gen = list(map(lambda g: val if g == 'a' else g, gen))
    root = Node(gen[0])
    root.left = Node(gen[1])
    root.right = Node(gen[2])
    root.right.left = Node(gen[3])
    root.right.right = Node(gen[4])
    root.right.right.left = Node(gen[5])
    root.right.right.right = Node(gen[6])
    return root


def MSE(dataset):
    sum = 0
    for elem in dataset:
        sum += (elem[1] - elem[0]) ** 2
    return sum / len(dataset)


def mutation(head, tail, mut_prob):
    if random.random() < mut_prob:
        if random.random() > 0.5:
            tail_r = random.choice(range(len(tail)))
            tail[tail_r] = 'a'
        else:
            head_r = random.choice(range(len(head)))
            symb = head[head_r]
            combined = list(T) + list(ops)
            head[head_r] = random.choice(list(filter(lambda x: x != head[head_r], combined)))
    return head, tail


a_y = [
    (3.4, 2.64),
    (5.4, 65.04),
    (6.7, 122.76),
    (8.2, 206.16),
    (9.12, 266.2176),
    (10.25, 349.25),
    (12.34, 529.7424),
    (21.43, 1721.26),
    (23.76, 2133.11),
    (25.32, 2433.13),
]

head = ['*', 'a', '+', 'a', '/', 'a', 'a']
n = len(T)
tail_len = len(head) * (n - 1) + 1
tail = [random.choice(list(T)) for _ in range(tail_len)]
gen = head + tail
results = []
epochs = 100
it = 0
while it < epochs:
    for (a, y) in a_y:
        root = generateRoot(head, a)
        res = evaluateExpressionTree(root)
        results.append((a, y, res))
    accuracy = list(zip([res[2] for res in results], [y[1] for y in a_y]))
    mse = MSE(accuracy)
    print(f'MSE for epoch {it}: {mse}')

    # mutation
    head, tail = mutation(head, tail, 0.3)

    it += 1

# Print the results
# for (a, y, result) in results:
#     print(f"For a={a}, Expected y={y}, Computed y={result}")
