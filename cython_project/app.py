import pyximport

pyximport.install()
from fib_python import fact_py
from fib_c import fact_c
import time

start = time.time()
print(fact_py(10))
end = time.time() - start
print(end)

start = time.time()
print(fact_c(10))
end = time.time() - start
print(end)
