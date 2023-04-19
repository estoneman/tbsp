"""Cython source builder"""
import os
import sys

from setuptools import setup, Extension
from Cython.Build import cythonize

ext_options = {"compiler_directives": {"profile": True, "language_level": 3}}

extensions = [Extension("edit_distance", ["py/edit_distance.pyx"])]
setup(
    ext_modules=cythonize(extensions, **ext_options),
    script_args=["build_ext", "--build-lib=py", "--build-temp=build"]
)
