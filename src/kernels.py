import os
import numpy as np
from numba.pycc import CC

cc = CC('kernels')

output_dir = '{}/dist'.format(os.path.abspath('..'))
cc.output_dir = output_dir


@cc.export('square', 'f8(f8)')
def square(x):
    return x ** 2


@cc.export('squarearr', 'f8[:](f8[:])')
def square_array(arr):
    return np.square(arr)


cc.compile()
