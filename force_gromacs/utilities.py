import numpy as np


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


def create_molecule_coord(atom_coord, n_site, masses, mode='molecule',
                          com_sites=None):
    """
    Returns XYZ array of molecular positions from array of atoms"

    Parameters
    ----------
    atom_coord:  array_like of floats
        Positions of particles in 3 dimensions
    n_site:  int
        Number of atomic sites per molecule
    masses:  array_like of float
        Masses of all atomic sites in g mol-1
    mode: list of int, optional
        Mode of calculation, either 'molecule' or 'sites':
        if `molecule`, molecular centre of mass is used. Otherwise, if
        'sites', only atoms with corresponding indices given by com_sites
        are used.
    com_sites: int or list of int, optional
        List of atomic sites to use in center of mass calculation

    Returns
    -------
    mol_coord:  array_like of floats
        Positions of molecules in 3 dimensions
    """

    # Calculate the expecded number of molecules in mol_coord
    n_mol = atom_coord.shape[0] // n_site

    # Create an empty array containing molecular coordinates
    mol_coord = np.zeros((n_mol, 3))

    assert mode in ['molecule', 'sites']

    # Use centre of mass of molecule as molecular position
    if mode == 'molecule':
        for i in range(3):
            mol_coord[:, i] = np.sum(
                np.reshape(
                    atom_coord[:, i] * masses, (n_mol, n_site)
                ), axis=1
            )
            mol_coord[:, i] *= n_mol / masses.sum()

        return mol_coord

    # Convert integer com_sites input into a list
    if isinstance(com_sites, int):
        com_sites = [com_sites]

    assert len(com_sites) < n_site

    # Use single atom as molecular position
    if len(com_sites) == 1:
        mol_list = np.arange(n_mol) * n_site + int(com_sites[0])
        for i in range(3):
            mol_coord[:, i] = atom_coord[mol_list, i]

    # Use centre of mass of a group of atoms within molecule as
    # molecular position
    elif len(com_sites) > 1:
        mol_list = np.arange(n_mol) * n_site
        mol_list = mol_list.repeat(len(com_sites))
        mol_list += np.tile(com_sites, n_mol)

        for i in range(3):
            mol_coord[:, i] = np.sum(
                np.reshape(
                    atom_coord[mol_list, i] * masses[mol_list],
                    (n_mol, len(com_sites))
                ), axis=1
            )
            mol_coord[:, i] *= n_mol / masses[mol_list].sum()

    return mol_coord
