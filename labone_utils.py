import matplotlib.pyplot as plt
import pandas as pd


def build_plots(max_iterations, fitness_scores, funcs: list, criterion=('mutation', [0.001, 0.05, 0.1])):
    n_funcs = len(funcs)
    rows = int(n_funcs / 3) + 1
    fig, axes = plt.subplots(rows, 3, figsize=(15, 15))
    x = range(max_iterations)
    i = 0
    for row in axes:
        for ax in row:
            if i < n_funcs:
                ax.plot(x, fitness_scores[i], label=funcs[i].__name__)
                ax.set_xlabel(f'Criterion ({criterion[0]}) value: {criterion[1][i]}')
                i += 1
    plt.tight_layout()
    plt.show()


def create_dataframe(features: list, columns: list, data: list):
    df = pd.DataFrame(index=features, columns=columns, data=data)
    return df
