import numpy as np


def batch_process(array1, array2, function, size=None,
                  shape=None, n_batch=None):
    """Perform a linear algebra operation involving two arrays
    in batch. Currently only supports up to 3D arrays

    Parameters
    ----------
    array1: array_like of float
        Input array of up to 2 dimensions
    array2: array_like of float
        Input array of up to 2 dimensions
    function: <object: callable>
        Callable method to perform on each pairwise combination
        of elements in array1 and array2
    shape: tuple of int, optional
        Shape of return matrix
    size: int, optional
        Size of batch to perform
    n_batch: int, optional
        Number of batches to perform

    Returns
    -------
    matrix: array_like of float
        Result of function(array1, array2)
    """

    # Assert dimensions of arrays are equal
    assert array1.ndim == array2.ndim == 2

    # Assert function is callable
    assert callable(function)

    # Form empty matrix to return with given shape if provided
    if shape is not None:
        matrix = np.zeros(shape)
    else:
        matrix = np.zeros((array1.shape[0],
                           array2.shape[0]))

    # Calculate number of batches based on either size or n_batch
    # arguments
    if size is not None:
        n_batch = array1.shape[0] // size
    else:
        assert n_batch is not None

    sub_arrays = np.array_split(array1, n_batch)
    start = 0
    end = 0

    # Cycle through each batch array in sub_arrays and perform
    # function on sub section
    for sub_array in sub_arrays:
        end += sub_array.shape[0]
        matrix[start:end] = function(sub_array, array2)
        start += sub_array.shape[0]

    return matrix
