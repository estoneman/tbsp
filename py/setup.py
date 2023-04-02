from setuptools import setup
from Cython.Build import cythonize

ext_options = {"compiler_directives": {"profile": True, "language_level": 3},
               "annotate": True}
setup(
    ext_modules=cythonize("edit_distance.pyx", **ext_options)
)
