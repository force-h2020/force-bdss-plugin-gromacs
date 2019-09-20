import numpy as np


def batch_process(array1, array2, function, size=None, n_batch=None):
    """Perform a linear algebra operation involving two arrays
    in batch"""

    matrix = np.zeros((array1.shape[0],
                       array2.shape[0]))

    if size is not None:
        n_batch = array1.shape[0] // size

    else:
        assert n_batch is not None

    sub_arrays = np.array_split(array1, n_batch)

    start = 0
    end = 0
    for sub_array in sub_arrays:
        end += sub_array.shape[0]
        matrix[start:end] = function(sub_array, array2)
        start += sub_array.shape[0]

    return matrix
