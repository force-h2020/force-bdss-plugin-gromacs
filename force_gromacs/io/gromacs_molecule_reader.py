import logging

from .base_file_reader import BaseFileReader

log = logging.getLogger(__name__)


class GromacsMoleculeReader(BaseFileReader):
    """Class parses Gromacs molecule topology (.itp) file and
    returns data required for each molecular type listed.
    """
    # ------------------
    #     Defaults
    # ------------------

    def __ext_default(self):
        """Default extension for this reader subclass"""
        return 'itp'

    def __comment_default(self):
        """Default extension for this reader subclass"""
        return ';'

    # ------------------
    #  Private Methods
    # ------------------

    def _remove_comments(self, file_lines):
        """If any in-line comments exists, then truncate
        line at point of comment"""

        file_lines = super()._remove_comments(file_lines)

        file_lines = [line.split(self._comment)[0].strip()
                      for line in file_lines]

        return file_lines

    def _get_molecule_sections(self, file_lines):
        """ Find file location and molecule type of each section

        Parameters
        ----------
        file_lines : list of str
            List containing lines in topology file as strings

        Returns
        -------
        mol_sections : list of str
            List containing relevant lines of topology file for
            each molecule in self.symbols
        """

        # Get indices for beginning of sections of all molecule types
        # in topology
        mol_indices = [index for index, line in enumerate(file_lines)
                       if "moleculetype" in line]

        if len(mol_indices) == 0:
            raise IOError(
                'Gromacs topology file does not include any'
                ' molecule types'
            )
        mol_sections = []
        start_indices = mol_indices
        end_indices = mol_indices[1:] + [None]

        # Extract the relevant lines in the topology file that correspond
        # to each molecule
        for start, end in zip(start_indices, end_indices):
            mol_sections.append(file_lines[start:end])

        return mol_sections

    def _parse_atom_line(self, line):

        file_line = line.split(self._comment)[0]
        file_line = file_line.split()

        index = int(file_line[0])
        symbol = file_line[1]
        mol_label = file_line[3]
        at_label = file_line[4]
        charge = float(file_line[6])
        mass = float(file_line[7])

        return index, symbol, mol_label, at_label, charge, mass

    def _get_data(self, file_lines):
        """ Load data for each target molecule type in Gromacs topology

        Parameters
        ----------
        file_lines : list of str
            List containing lines in topology file as strings

        Returns
        -------
        mol_symbols : list of str
            List of atoms in each target molecular type
        mol_atoms : list of list of str
            List of atoms in each target molecular type
        mol_charges : list of list of int
            List of electronic charges corresponding to each target molecular
            type
        mol_masses : list of list of float
            List of atomic masses corresponding to each target molecular type
        """

        mol_sections = self._get_molecule_sections(file_lines)

        mol_symbols = []
        mol_atoms = []
        mol_charges = []
        mol_masses = []

        for section in mol_sections:

            # Get symbols that correspond to each molecule type
            symbol = section[1].split()[0]

            # Find file location of atom list for target molecule
            atom_indices = [index + 1 for index, line
                            in enumerate(section) if "atoms" in line]

            atoms_index = atom_indices[0]

            # Read the name, charge and mass of each atom/bead, which should
            # be included at indices 4, 6 and 7 respectively
            atoms = []
            charges = []
            masses = []
            for line in section[atoms_index:]:
                if line.startswith('['):
                    break
                else:
                    (_, _, _,
                     at_label, charge, mass) = self._parse_atom_line(line)

                    atoms.append(at_label)
                    charges.append(charge)
                    masses.append(mass)

            mol_symbols.append(symbol)
            mol_atoms.append(atoms)
            mol_charges.append(charges)
            mol_masses.append(masses)

        return mol_symbols, mol_atoms, mol_charges, mol_masses

    # ------------------
    #   Public Methods
    # ------------------

    def read(self, file_path):
        """ Open Gromacs topology file located at `file_path` and return
         processed data

        Parameters
        ----------
        file_path : str
            File path of Gromacs topology file

        Returns
        -------
        data : dict
            Dictionary containing data (including constituent atoms, mass
            and charge) extracted from Gromacs topology file. Keys refer
            to the symbol of each
            molecular species.
        """

        try:
            file_lines = self._read_file(file_path)
        except IOError as e:
            log.exception('unable to open "{}"'.format(file_path))
            raise e

        file_lines = self._remove_comments(file_lines)

        try:
            iterator = self._get_data(file_lines)
        except Exception as e:
            log.exception('unable to load data from "{}"'.format(file_path))
            raise e

        data = {
            symbol: {
                'atoms': atoms,
                'charges': charges,
                'masses': masses
            }
            for symbol, atoms, charges, masses in zip(*iterator)
        }

        return data

    def _read(self, file_path):

        try:
            file_lines = self._read_file(file_path)
        except IOError as e:
            log.exception('unable to open "{}"'.format(file_path))
            raise e

        file_lines = self._remove_comments(file_lines)

        try:
            molecules = self._get_molecules(file_lines)
        except Exception as e:
            log.exception('unable to load data from "{}"'.format(file_path))
            raise e

        return molecules
