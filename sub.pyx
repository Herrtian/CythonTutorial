import cython
cdef extern from "sub_core/sub.h":
    int sub(int a, int b)

# 然后 Cython 可以直接调用
@cython.infer_types(True)
def sub_with_c(a, b):
    cdef int ret = sub(a, b)  # 这一行会更快 原因在于静态类型
    # ret = sub(a, b)
    return ret
