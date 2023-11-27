def fact_c(n):
    if n == 1:
        return 1
    return n * fact_c(n - 1)
