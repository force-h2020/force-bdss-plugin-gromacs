import numpy as np
from functools import partial

from .utilities import (
    batch_pairwise
)


def minimum_image(d_array, pbc_box):
    """Mutates d_array to yield the minimum signed value of each
    element, based on periodic boundary conditions given by pbc_box

    Parameters
    ---------
    d_array: array_like of float
        Array of elements in n dimensions, where the last axis
        corresponds to a vector with periodic boundary conditions
        enforced by values in pbc_box
    pbc_box: array_like of floats
        Vector containing maximum signed value for each element
        in d_array
    """

    assert d_array.shape[-1] == pbc_box.shape[-1]
    assert d_array.dtype == pbc_box.dtype

    # Obtain minimum image distances based on rectangular
    # prism geometry
    for i, dim in enumerate(pbc_box):
        d_array[..., i] -= dim * np.rint(
            d_array[..., i] / dim
        )


def pairwise_difference_matrix(array1, array2, pbc_box=None):
    """Build matrix containing pairwise vector differences between
    each entry in array1 and array2. Enforces minimum image periodic
    boundary conditions given by pbc_box if supplied as an argument

    Parameters
    ----------
    array1: array_like of float
        Input array of n dimensions
    array2: array_like of float
        Input array of n dimensions
    pbc_box: array_like of floats, optional
        Vector containing maximum signed value for each element
        in distance array

    Returns
    -------
    d_array: array_like of floats
        Displacements between each pairwise combination of elements
        in array1 and array2
    """

    # Both arrays must share the same vector dimension, n_depth
    assert array1.shape[-1] == array2.shape[-1]

    n_array1 = array1.shape[0]
    n_array2 = array2.shape[0]
    n_depth = array1.shape[-1]

    # Create two n_array1 x n_array2 x n_depth matrices
    # to calculate cartesian distances between each element
    d_array = np.zeros((n_array1, n_array2, n_depth))

    # Calculate signed distance matrices for each pairwise configuration
    # along each dimension
    for index in range(n_depth):
        # Use numpy subtract to create broadcasted arrays for each
        # dimension - note, we use slices to keep both subarrays 2D
        d_array[..., index] = np.subtract(
            array1[..., index: index + 1],
            array2.T[index: index + 1]
        )

    if pbc_box is not None:
        # Calculate difference matrix based on minimum image
        minimum_image(d_array, pbc_box)

    return d_array


def squared_euclidean_distance(array1, array2, pbc_box=None):
    """Calculate squared euclidean distances between each pairwise
    combination of elements in array1 and array2

    Parameters
    ----------
    array1: array_like of float
        Input array of up to 2 dimensions
    array2: array_like of float
        Input array of up to 2 dimensions
    pbc_box:  array_like of floats
        Vector containing maximum signed value for each element
        in distance array

    Returns
    -------
    r2_matrix: array_like of floats
        Squared euclidean distances for each pairwise particle
        interaction
    """

    # Calculate vector differences
    d_array = pairwise_difference_matrix(
        array1, array2, pbc_box=pbc_box
    )

    # Calculate squared euclidean distances
    r2_matrix = np.sum(d_array**2, axis=-1)

    return r2_matrix


def euclidean_distance(array1, array2, pbc_box=None):
    """Calculate euclidean distances between each pairwise
    combination of elements in array1 and array2

    Parameters
    ----------
    array1: array_like of float
        Input array of up to 2 dimensions
    array2: array_like of float
        Input array of up to 2 dimensions
    pbc_box:  array_like of floats
        Vector containing maximum signed value for each element
        in distance array

    Returns
    -------
    r_matrix: array_like of floats
        Euclidean distances for each pairwise particle
        interaction
    """

    return np.sqrt(
        squared_euclidean_distance(
            array1, array2, pbc_box=pbc_box
        )
    )


def distance_matrix(coord, cell_dim, metric='euclidean'):
    """Calculate distances between each pairwise
    combination of elements in coordinate array. Can either return
    euclidean distance, squared euclidean distance or vector
    displacements, depending on 'mode'.

    Parameters
    ----------
    coord:  array_like of floats
        Positions of a set particles in 3 dimensions
    cell_dim:  array_like of floats
        Simulation cell dimensions in 3 dimensions
    metric: str, optional, default: 'euclidean'
        Method of calculation, either 'euclidean' for euclidean
        distance, 'sqeuclidean' for squared euclidean distance, or
        'vector' for displacement along each dimension vector

    Returns
    -------
    distance_matrix: array_like of floats
        Distance matrix for each pairwise particle interaction
    """

    assert metric in ['euclidean', 'sqeuclidean', 'vector']

    if metric == 'euclidean':
        # Calculate the pairwise euclidean differences between each
        # element in coord
        return euclidean_distance(
            coord, coord, pbc_box=cell_dim
        )

    if metric == 'sqeuclidean':
        # Calculate the pairwise euclidean differences between each
        # element in coord
        return squared_euclidean_distance(
            coord, coord, pbc_box=cell_dim
        )

    if metric == 'vector':
        # Calculate pairwise vector differences between each element
        # in coord
        return pairwise_difference_matrix(
            coord, coord, pbc_box=cell_dim
        )


def batch_distance_matrix(coord, cell_dim, metric='euclidean',
                          batch_size=50):
    """Uses batch_pairwise function in force_gromacs.tools.utilities to
    performs distance_matrix in batches to alleviate memory.

    Parameters
    ----------
    coord:  array_like of floats
        Positions of a set particles in 3 dimensions
    cell_dim:  array_like of floats
        Simulation cell dimensions in 3 dimensions
    metric: str, optional, default: 'euclidean'
        Method of calculation, either 'euclidean' for euclidean
        distance, 'sqeuclidean' for squared euclidean distance, or
        'vector' for displacement along each dimension vector
    batch_size : int, optional, default: 50
        Sample size parameter of each batch.

    Returns
    -------
    distances: array_like of floats
        Distance matrix for each pairwise particle interaction
    """

    assert metric in ['euclidean', 'sqeuclidean', 'vector']

    if metric == 'euclidean':
        # Create a partial function that only takes in 2 arguments
        function = partial(euclidean_distance,
                           pbc_box=cell_dim)

        # Calculate the pairwise euclidean differences between each
        # element in coord
        return batch_pairwise(coord, coord, function,
                              batch_size=batch_size)

    if metric == 'sqeuclidean':
        # Create a partial function that only takes in 2 arguments
        function = partial(squared_euclidean_distance,
                           pbc_box=cell_dim)

        # Calculate the squared pairwise euclidean differences between
        # each element in coord
        return batch_pairwise(coord, coord, function,
                              batch_size=batch_size)

    elif metric == 'vector':
        # Create a partial function that only takes in 2 arguments
        function = partial(
            pairwise_difference_matrix, pbc_box=cell_dim
        )

        # Provide an expected shape of the return matrix to handle
        # 3D vector
        shape = (coord.shape[0], coord.shape[0], coord.shape[1])

        # Calculate the vector differences between each element in coord
        return batch_pairwise(
            coord, coord, function, shape=shape, batch_size=batch_size
        )
