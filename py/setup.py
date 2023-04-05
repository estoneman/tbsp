from setuptools import setup, Extension
from Cython.Build import cythonize

ext_options = {"compiler_directives": {"profile": True, "language_level": 3}}

extensions = [Extension("edit_distance", ["edit_distance.pyx"])]
setup(
    ext_modules=cythonize(extensions, **ext_options)
)
