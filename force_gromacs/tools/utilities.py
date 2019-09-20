import numpy as np


def batch_process(array1, array2, function, batch_size=50,
                  shape=None):
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
    batch_size : int, optional, default: 50
        Sample size of each array for a batch.
    shape: tuple of int, optional
        Shape of return matrix

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

    # Calculate number of batches based on batch_size
    n_samples = min(array1.shape[0], array2.shape[0])
    n_batches = int(np.ceil(n_samples / batch_size))

    sub_arrays1 = np.array_split(array1, n_batches)
    sub_arrays2 = np.array_split(array2, n_batches)

    # Cycle through each batch array in sub_arrays and perform
    # function on sub section
    start1 = 0
    end1 = 0
    for sub_array1 in sub_arrays1:
        end1 += sub_array1.shape[0]

        start2 = 0
        end2 = 0
        for sub_array2 in sub_arrays2:
            end2 += sub_array2.shape[0]

            matrix[start1: end1,
                   start2: end2] = function(sub_array1, sub_array2)

            start2 += sub_array2.shape[0]
        start1 += sub_array1.shape[0]

    return matrix
