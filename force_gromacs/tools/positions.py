import numpy as np


def molecular_positions(atom_coord, n_site, masses, mode='molecule',
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
    mode: str, optional, default: 'molecule'
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
