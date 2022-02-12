cdef extern from "sub_core/sub.h":
    int sub(int a, int b)

# 然后 Cython 可以直接调用
def sub_with_c(a, b):
    return sub(a, b)