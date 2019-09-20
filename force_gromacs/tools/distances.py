import numpy as np
from functools import partial

from .utilities import (
    batch_process
)


def minimum_image(d_array, pbc_box):
    """Mutates d_array to yield the minimum signed value of each
    element, based on periodic boundary conditions given by pbc_box

    Parameters
    ---------
    d_array: array_like of float
        Array of elements in n dimenions, where the last axis
        corresponds to a vector with periodic boundary conditions
        enforced by values in pbc_box
    pbc_box:  array_like of floats
        Vector containing maximum signed value for each element
        in d_array
    """

    assert d_array.shape[-1] == pbc_box.shape[-1]

    # Obtain minimum image distances based on rectangular
    # prism geometry
    for i, dim in enumerate(pbc_box):
        d_array[..., i] -= dim * np.array(
            2 * d_array[..., i] / dim, dtype=int
        )


def pairwise_difference_matrix(array1, array2, pbc_box=None):
    """Build matrix containing pairwise vector differences between
    each entry in array1 and array2. Enforces minimum image periodic
    boundary conditions given by pbc_box if supplied as an argument"""

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


def distance_matrix(coord, cell_dim, mode='r'):
    """Calculate squared radial distances between each pairwise
    combination of elements in coordinate array

    Parameters
    ----------
    coord:  array_like of floats
        Positions of a set particles in 3 dimensions
    cell_dim:  array_like of floats
        Simulation cell dimensions in 3 dimensions
    mode: str, optional
        Method of calculation, either 'r' for euclidean
        distance, 'r2' for squared euclidean distance, or
        'vector' for displacement along each dimension vector

    Returns
    -------
    distance_matrix: array_like of floats
        Distance matrix for each pairwise particle interaction
    """

    assert mode in ['r', 'r2', 'vector']

    if mode == 'r':
        # Calculate the pairwise euclidean differences between each
        # element in coord
        return euclidean_distance(
            coord, coord, pbc_box=cell_dim
        )

    if mode == 'r2':
        # Calculate the pairwise euclidean differences between each
        # element in coord
        return squared_euclidean_distance(
            coord, coord, pbc_box=cell_dim
        )

    if mode == 'vector':
        # Calculate pairwise vector differences between each element
        # in coord
        return pairwise_difference_matrix(
            coord, coord, pbc_box=cell_dim
        )


def batch_distance_matrix(coord, cell_dim, mode='r', n_batch=1):
    """Uses batch_process function in force_gromacs.tools.utilities to
    performs distance_matrix in batches to alleviate memory.
    Currently only returns the squared radial distances, not the full
    pairwise distance matrices.

    Parameters
    ----------
    coord:  array_like of floats
        Positions of a set particles in 3 dimensions
    cell_dim:  array_like of floats
        Simulation cell dimensions in 3 dimensions
    mode: str, optional
        Method of calculation, either 'r' for euclidean
        distance, 'r2' for squared euclidean distance, or
        'vector' for displacement along each dimension vector
    n_batch: int, optional
        Number of batches to run in serial

    Returns
    -------
    distances: array_like of floats
        Distance matrix for each pairwise particle interaction
    """

    assert mode in ['r', 'r2', 'vector']

    if mode == 'r':
        # Create a partial function that only takes in 2 arguments
        function = partial(euclidean_distance,
                           pbc_box=cell_dim)

        # Calculate the pairwise euclidean differences between each
        # element in coord
        return batch_process(coord, coord, function, n_batch=n_batch)

    if mode == 'r2':
        # Create a partial function that only takes in 2 arguments
        function = partial(squared_euclidean_distance,
                           pbc_box=cell_dim)

        # Calculate the squared pairwise euclidean differences between
        # each element in coord
        return batch_process(coord, coord, function, n_batch=n_batch)

    elif mode == 'vector':
        # Create a partial function that only takes in 2 arguments
        function = partial(
            pairwise_difference_matrix, pbc_box=cell_dim
        )

        # Provide an expected shape of the return matrix to handle
        # 3D vector
        shape = (coord.shape[0], coord.shape[0], coord.shape[1])

        # Calculate the vector differences between each element in coord
        return batch_process(
            coord, coord, function, shape=shape, n_batch=n_batch
        )
