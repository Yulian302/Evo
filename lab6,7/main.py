from genetic_programming import Operators, GeneticExpressionTree, TreeLinker

OPERATORS = {
    '+': Operators.ADD,
    '-': Operators.SUBTRACT,
    '*': Operators.MULTIPLY,
    '/': Operators.DIVIDE,
    'U': Operators.UNARY_SUBTRACTION,
    'P': Operators.POWER,
}

TERMINALS = ['a']

a_F_pairs = [
    [[3.4], 2.64],
    [[5.4], 65.04],
    [[6.7], 122.76],
    [[8.2], 206.16],
    [[9.12], 266.2176],
    [[10.25], 349.25],
    [[12.34], 529.7424],
    [[21.43], 1721.26],
    [[23.76], 2133.11],
    [[25.32], 2433.13]
]

genetic = GeneticExpressionTree(OPERATORS,
                                TERMINALS,
                                16,
                                2,
                                2,
                                TreeLinker.SUM,
                                0.6,
                                3,
                                0.1,
                                0.1
                                )

epochs = 2000
best_ge = genetic.train(a_F_pairs, 80, epochs)

validation_points = [10, 20, 30]
for val in validation_points:
    print(f"F({val})={genetic.evaluate_expression(best_ge, {'a': val})}")

restored_expression = genetic.restore_expr(best_ge)
print(restored_expression)
print(best_ge)
