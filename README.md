# Cython Tutorial

## 引子

1. 本期视频旨在教授大家如何使用cython 并且提供一个实战项目
2. 实战的重点--- python导入C++ 代码 （不讲述 python代码优化）

## 观前提示

1.  up主废话较多 请适倍速观看 
2.  up主吐字不清  请适倍速观看
3.  up主并非研究编译原理这一课题，加之cython的教程少之又少  所以可能讲的都是错的 请轻喷up主



## $0 什么是Cython

1. Cython 与 Cpython的 区别 

```txt
CPython -- JavaPython -- RustPython === 解释器 
如果你安装过python3 --从源码级别的安装 -- PyObject * 
Cython 是一门语言（语法 变量 作用于 语法特性 == ） 
```

2. Cython能用来干嘛？ **https://www.cnblogs.com/traditional/p/13196509.html**

```txt

    1. 因为某些需求导致不得不编写一些多重嵌套的循环，而这些循环如果用 C 语言来实现会快几百倍，但是不熟悉 C 或者不知道 Python 如何与 C 进行交互。

    2. 因为 Python 解释器的性能原因，如果将 CPython 解释器换成 PyPy，或者干脆换一门语言，比如 Julia，将会得到明显的性能提升，可是换不得。因为你的项目组规定只能使用 Python 语言，解释器只能 CPython。

    3. Python 是一门动态语言，但你希望至少在数字计算方面，能够加入可选的静态类型，这样可以极大的加速运算效果。因为单纯的数字相加不太需要所谓的动态性，尤其是当你的程序中出现了大量的计算逻辑时。

    4. 对于一些计算密集型的部分，你希望能够写出一些超越 Numpy、Scipy、Pandas 的算法。

    *** 5. 你有一些已经用 C、C++ 实现的库，你想直接在 Python 内部更好地调用它们，并且不使用 ctypes、cffi 等模块。

    6. 也许你听说过 Python 和 C 可以无缝结合，通过 C 来为 Python 编写扩展模块，将 Python 代码中性能关键的部分使用 C 进行重写，来达到提升性能的效果。但是这需要你对 Python 解释器有很深的了解，熟悉底层的 Python/C API，而这是一件非常痛苦的事情。

```

 Cython 原理 （纯瞎扯）

```
  Cython编译器是一种 源到源 的编译器，并且生成的扩展模块也是经过高度优化的，因此 Cython 生成的 C 代码编译得到的扩展模块 比 手写的 C 代码编译得到的扩展模块 运行的要快并不是一件稀奇的事情。因为 Cython 生成的 C 代码是经过高度精炼，所以大部分情况下比手写所使用的算法更优，而且 Cython 生成的 C 代码支持所有的通用 C 编译器，生成的扩展模块同时支持许多不同的 Python 版本。
```

中文   = 英语  =  法语



## $1 安装 Cython

```环境
OS : Linux Mint --- debian系 
pip install cython
cython -v
```



## $2 包装一个cython函数 



add.pyx 

```python
def add(a, b):
    """这是add模块"""
    cdef double x = 1.1
    cdef char y = 3

    return a + b + x

```



setup.py

```python
from distutils.core import setup
from Cython.Build import cythonize

# 我们说构建扩展模块的过程分为两步: 1. 将 Cython 代码翻译成 C 代码; 2. 根据 C 代码生成扩展模块
# 而第一步要由 cython 编译器完成, 通过 cythonize; 第二步要由 distutils 完成, 通过 distutils.core 下的 setup
setup(ext_modules=cythonize("add.pyx", language_level=3))
```

python setup.py build 

main.py

```python 
import add
print(add.add(2, 3))

```

尽管你删除了 .pyx 代码还是可以运行 原因在于调用的是一个.so

## $3 调用一个C文件

dir : sub_core

```c
// sub.h
int sub(int a , int b);
```

```c
// sub.c
#include "sub.h"

int sub(int a , int b){
    return a - b ;
}
```

sub.pyx

```cython
cdef extern from "sub_core/sub.h":
    int sub(int a, int b)

# 然后 Cython 可以直接调用
def sub_with_c(a, b):
    return sub(a, b)

```

setup.py

```python
from distutils.core import setup, Extension
from Cython.Build import cythonize

ext = Extension(name="wrapper_sub", sources=["sub.pyx", "sub_core/sub.c"], language_level=3,
                )
setup(ext_modules=cythonize(ext))
```

```python
# main
import wrapper_sub
print(wrapper_sub.sub_with_c(2, 3))


```



## $4 Cython语法

 其实没有特别的语法 Python怎么用的 Cython就怎么用 

```python
def sub_with_c(a, b):
    cdef int ret = sub(a, b) # 这一行会更快 原因在于静态类型
    # ret = sub(a, b)

    return ret
```

```python
import cython
cdef extern from "sub_core/sub.h":
    int sub(int a, int b)

# 然后 Cython 可以直接调用

@cython.infer_types(True)
def sub_with_c(a, b):
    cdef ret = sub(a, b) # 这一行会更快 原因在于静态类型
    # ret = sub(a, b)
    return ret
```

你也可以加上装饰器 让它自动推断 ～ 

### 如何定义指针变量 引用和解引用 

```cython
cdef double a
cdef double *b = NULL
cdef double *c, *d
```

解引用 

```cython 
cdef int a  = 10 
cdef int *p = &a 
x = p[0] # x = 10 
print(x)
```

### cdef cpdef def的区别

cdef 不能被外部所调用 

```python
cdef list f1():
    return []
```

def 用来构建python与cython的桥梁 

cpdef用来构建 cdef 和 def的桥梁  

### inline

```cython
cpdef inline unsigned long rec(int n):
    if n == 1:
        return 1
    return rec(n - 1) * n
```

-- cpdef不支持闭包

### 声明并使用结构体、共同体、枚举

```cython
struct mycpx {
    float a;
    float b;
};

union uu {
    int a;
    short b, c;
};
====================================
cdef struct mycpx:
    float real
    float imag
    
cdef union uu:
    int a
    short b, c
   
# 你也可以写成这样 
ctypedef struct mycpx:
    float real
    float imag
    
ctypedef union uu:
    int a
    short b, c
    
    
# 创建 =====
# 此时我们相当于为结构体和共同体起了一个别名叫：mycpx、uu
cdef mycpx zz  # 此时的 zz 就是一个 mycpx 类型的变量
# 当然无论结构体是使用 cdef 声明的还是 ctypedef 声明的，变量 zz 的声明都是一样的

# 但是变量的赋值方式有以下几种
# 1. 创建的时候直接赋值
cdef mycpx a = mycpx(1, 2)
# 也可以支持关键字的方式，但是注意关键字参数要在位置参数之后
cdef mycpx b = mycpx(real=1, imag=2)

# 2. 声明之后，单独赋值
cdef mycpx c
c.real = 1
c.imag = 2
# 这种方式会麻烦一些，但是可以更新单个字段

# 3. 通过Python中的字典赋值
cdef mycpx d = {"real": 1, "imag": 2}
# 显然这是使用Cython的自动转换完成此任务，它涉及更多的开销，不建议用此种方式。


```



### 结构体嵌套

```c
// example 
struct girl{
    char *where;

    struct _info {
        char *name;
        int age;
        char *gender;
    } info;
};

```



```cython
ctypedef struct _info:
    char *name
    int age
    char *gender

ctypedef struct girl:
    char *where
    _info info  # 创建一个info成员，类型是_info

cdef girl g = girl(where="sakura sou", info=_info("mashiro", 16, "female"))
print(g.where)
print(g.info.name)
print(g.info.age)
print(g.info.gender)
```



枚举 

```cython
cdef enum my_enum1:
    RED = 1
    YELLOW = 3
    GREEN = 5

cdef enum my_enum2:
    PURPLE, BROWN
```

### 使用 ctypedef 给类型起别名

```cython
ctypedef list LIST  # 给list起一个别名

# 参数是一个LIST类型
def f(LIST v):
    print(v)
```

**拓展** https://www.cnblogs.com/traditional/p/13246471.html

### cinit 和 init

```cython
cdef class A:
    cdef:
        unsigned int n
        double *array  # 一个数组，存储了double类型的变量

    def __cinit__(self, n):
        self.n = n
        # 在C一级进行动态分配内存
        self.array = <double *>malloc(n * sizeof(double))
        if self.array == NULL:
            raise MemoryError()
            
    def __dealloc__(self):
        """如果进行了动态内存分配，也就是定义了 __cinit__，那么必须要定义 __dealloc__
        否则在编译的时候会抛出异常：Storing unsafe C derivative of temporary Python reference
        然后我们释放掉指针指向的内存
        """
        if self.array != NULL:
            free(self.array)
```

cinit 是 C 级别的内存分配  相当于直接接触malloc级别的初始化 

init 是python级别的内存分配 

**所以 __cinit__ 是用来进行 C  一级内存的动态分配的，另外我们说如果在 __cinit__ 通过 malloc 进行了内存分配，那么必须要定义 __dealloc__  函数将指针指向的内存释放掉。当然即使我们不释放也没关系，只不过可能发生内存泄露（雾），但是 __dealloc__  这个函数是必须要被定义，它会在实例对象回收时被调用。**

**这个时候可能有人好奇了，那么 __cinit__ 和 __init__ 函数有什么区别呢？区别还是蛮多的，我们细细道来。**

**首先它们只能通过 def 来定义，另外在不涉及 malloc  动态分配内存的时候， __cinit__ 和 __init__ 是等价的。然而一旦涉及到 malloc，那么动态分配内存只能在  __cinit__ 中进行，如果这个过程写在了 __init__ 函数中，比如将我们上面例子的 __cinit__ 改为 __init__  的话，你会发现 self 的所有变量都没有设置进去、或者说设置失败，并且其它的方法若是引用了 self.array，那么还会导致丑陋的段错误。**

**还有一点就是，__cinit__ 函数会在 __init__ 函数之前调用，我们实例化一个扩展类的时候，参数会先传递给 __cinit__，然后 __cinit__ 再将接收到的参数原封不动的传递给 __init__。**



## $5 包装C 文件

### 声明外部的 C 函数以及给类型起别名

**extern 块中最常见的声明是 C 函数和 typedef，这些声明几乎可以直接写在 Cython 中，只需要做一下修改：**

**1. 将 typedef 变成 ctypedef**

**2. 删除类似于 restrict、volatile 等不必要、以及不支持的关键字**

**3. 确保函数的返回值和对应类型的声明在同一行**

**4. 删除行尾的分号**

##  

header.h

```c
#define M_PI 3.1415926
#define MAX(a, b) ((a) >= (b) ? (a) : (b))
double hypot(double, double);
typedef int integral;
typedef double real;
void func(integral, integral, real);
real *func_arrays(integral[], integral[][10], real **);
```



```cython
cdef extern from "header.h":
    double M_PI
    float MAX(float a, float b)
    double hypot(double x, double y)
    ctypedef int integral
    ctypedef double real
    void func(integral a, integral b, real c)
    real *func_arrays(integral[] i, integral[][10] j, real **k)
```

 

###  声明并包装 C 结构体、共同体、枚举



header_name

```c
struct struct_name {
    struct_members
};  // 创建变量的时候通过 "struct struct_name 变量" 的方式

union union_name {
    union_members
};

enum enum_name {
    enum_members
};
```

```cython
cdef extern from "header_name":
    struct struct_name: 
        struct_members  # 创建变量的时候通过 "cdef struct_name 变量" 的方式
    
    union struct_name:
        union_members
    
    enum struct_name:
        enum_members
```

### 引入源文件

```cython
# .c
int func(int a, int b) {
    return a + b;
}

# ================================= # 

cdef extern from "source.c":
    # 注意：这个 func 不能直接被 Python 调用，因为它是 C 的函数
    # 并且我们说 Cython 不会自动创建包装器，需要我们手动创建
    int func(int a, int b)

def py_func(int a, int b):
    return func(a, b)
```



## $6 实战

### 最终演示

仓库地址 ：https://github.com/Herrtian/PicoscenesToolbox



新建一个项目 并且 将parsingcore clone下来 

git clone  https://gitlab.com/wifisensing/rxs_parsing_core.git



setup.py

```python
# setup.py 
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

import numpy
from Cython.Build import cythonize
from setuptools import find_packages, setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension


def find_files(root, ext):
    ret = list()
    if os.path.exists(root):
        for file in os.listdir(root):
            if file.endswith(ext):
                ret.append(os.path.join(root, file))
    return ret


EXTENSIONS = []


class Build(build_ext):
    def build_extensions(self):
        if self.compiler.compiler_type in ['unix', 'mingw32']:
            for e in self.extensions:
                if e.name == "picoscenes":
                    e.extra_compile_args = ['-std=c++2a', '-Wno-attributes',
                                            '-O3']
        if self.compiler.compiler_type in ["msvc"]:
            for e in self.extensions:
                if e.name == "picoscenes":
                    e.extra_compile_args = ['/std:c++latest']
        super(Build, self).build_extensions()


pico_root = "./rxs_parsing_core"
pico_generated = os.path.join(pico_root, 'interpolationAndCSDRemoval/generated')
pico_include = os.path.join(pico_root, 'interpolationAndCSDRemoval')
pico_source = find_files(pico_root, '.cxx') + find_files(pico_generated, '.cpp')
pico_extension = Extension(
    "picoscenes", ["./picoscenes.pyx"] + pico_source,
    include_dirs=[numpy.get_include(), pico_include],
    define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
)
if os.path.exists(pico_root):
    EXTENSIONS.append(pico_extension)

setup(
    packages=find_packages(),
    install_requires=['numpy'],
    python_requires='>=3',
    ext_modules=cythonize(
        EXTENSIONS,
        compiler_directives={'language_level': 3, 'binding': False}
    ),
    cmdclass={'build_ext': Build},
)


```



picoscenes.pyx

### 导入部分

```cython

# distutils: language = c++
import struct

from libc.stdio cimport (fopen, fread, fclose, fseek, ftell, printf, FILE,
SEEK_END, SEEK_SET, SEEK_CUR)
from libc.stdint cimport (uint8_t, uint16_t, uint32_t, uint64_t,
int8_t, int16_t, int32_t, int64_t)
from libc.stdlib cimport malloc, realloc, free
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.complex cimport complex as ccomplex

import numpy as np

```

```cython
cdef extern from "<optional>" namespace "std" nogil:
    cdef cppclass optional[T]:...
        ...
```

c++17 的语法 

### cxx文件导入

```cython
cdef extern from "rxs_parsing_core/ModularPicoScenesFrame.hxx":
    # ModularPicoScenesFrame.hxx
    cdef packed struct ieee80211_mac_frame_header_frame_control_field:
        uint16_t version
        uint16_t type
        uint16_t subtype
        uint16_t toDS
        uint16_t fromDS
        uint16_t moreFrags
        uint16_t retry
        uint16_t power_mgmt
        uint16_t more
        uint16_t protect
        uint16_t order
        
        ...
```



packed 修饰 --- 涉及到 bit field 位运算的时候导入

### 扩展类

**cppclass**关键字声明Cython扩展类RxSBasicSegment，这是告诉Cython编译器正在封装的外部代码是C++代码 并且名字一致 

```cython
cdef cppclass RxSBasicSegment:
    const RxSBasic & getBasic() const
```



项目地址 ： **https://github.com/Herrtian/PicoscenesToolbox**

教程地址 ： **https://github.com/Herrtian/CythonTutorial/tree/master**





