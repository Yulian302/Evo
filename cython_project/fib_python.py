def fact_py(n):
    if n == 1:
        return 1
    return n * fact_py(n - 1)
