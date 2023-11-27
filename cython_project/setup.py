from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Cython Sample',
    version='1.0',
    ext_modules=cythonize(['main.pyx', 'fib_c.pyx'], compiler_directives={'language_level': "3"}),
    requires=['wheel']
)
