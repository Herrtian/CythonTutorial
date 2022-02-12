from distutils.core import setup
from Cython.Build import cythonize

# 我们说构建扩展模块的过程分为两步: 1. 将 Cython 代码翻译成 C 代码; 2. 根据 C 代码生成扩展模块
# 而第一步要由 cython 编译器完成, 通过 cythonize; 第二步要由 distutils 完成, 通过 distutils.core 下的 setup
setup(ext_modules=cythonize("add.pyx", language_level=3))