from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension(name="wrapper_sub", sources=["sub.pyx", "sub_core/sub.c"], language_level=3,
                )
setup(ext_modules=cythonize(ext))