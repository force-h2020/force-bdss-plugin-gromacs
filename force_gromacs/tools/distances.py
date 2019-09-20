import numpy as np
from functools import partial

from .utilities import batch_process


def minimum_image(d_coord, cell_dim):
    """Mutates d_coord to yield the minimum distance between
    coordinates, based on periodic boundary conditions with cell_dim
    dimensions

    Parameters
    ---------
    d_coord: array_like of float
        Array of distances in multiple dimensions between coordinates,
        where the last axis corresponds to each dimension
    cell_dim:  array_like of floats
        Simulation cell dimensions in 3 dimensions
    """

    assert d_coord.shape[-1] == cell_dim.shape[-1]

    # Obtain minimum image distances based on rectangular
    # prism geometry
    for i, dim in enumerate(cell_dim):
        d_coord[..., i] -= dim * np.array(
            2 * d_coord[..., i] / dim, dtype=int
        )


def pairwise_difference_matrix(array1, array2):
    """Build matrix containing pairwise vector differences between
    each entry in array1 and array2."""

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

    return d_array


def distance_matrix(coord1, coord2, cell_dim, distances=True):
    """Calculate distance vector matrix between two sets
    of coordinates

    Parameters
    ----------
    coord1:  array_like of floats
        Positions of a set particles in 3 dimensions
    coord2:  array_like of floats
        Positions of a set particles in 3 dimensions
    cell_dim:  array_like of floats
        Simulation cell dimensions in 3 dimensions
    distances: bool, optional
        Whether or not to return pairwise difference matricies
        alongside squared radial distance

    Returns
    -------
    r2_coord: array_like of floats
        Radial distance squared between each particle
    d_coord: array_like of floats
        Displacement along each axis between each particle
    """

    # Calculate the pairwise differences between each element in
    # coord1 and coord2
    d_coord = pairwise_difference_matrix(coord1, coord2)

    # Calculate difference matrix based on minimum image
    minimum_image(d_coord, cell_dim)

    # Calculate squared radial distances
    r2_coord = np.sum(d_coord**2, axis=-1)

    if distances:
        return r2_coord, d_coord
    else:
        return r2_coord


def batch_distance_matrix(coord1, coord2, cell_dim, n_batch=1):
    """Uses batch_process function in force_gromacs.tools.utilities to
    performs distance_matrix in batches to alleviate memory.
    Currently only returns the squared radial distances, not the full
    pairwise distance matrices.

    Parameters
    ----------
    coord1:  array_like of floats
        Positions of a set particles in 3 dimensions
    coord2:  array_like of floats
        Positions of a set particles in 3 dimensions
    cell_dim:  array_like of floats
        Simulation cell dimensions in 3 dimensions
    n_batch: int, optional
        Number of batches to run in serial

    Returns
    -------
    r2_coord: array_like of floats
        Radial distance squared between each particle
    """
    function = partial(distance_matrix, cell_dim=cell_dim,
                       distances=False)

    r2_coord = batch_process(coord1, coord2,
                             function, n_batch=n_batch)

    return r2_coord
