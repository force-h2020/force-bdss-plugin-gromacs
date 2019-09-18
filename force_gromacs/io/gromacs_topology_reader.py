import logging

from traits.api import ReadOnly

from .base_file_reader import BaseFileReader

log = logging.getLogger(__name__)


class GromacsTopologyReader(BaseFileReader):
    """Class parses Gromacs file and returns data required for
    each molecular type listed.
    """

    # --------------------
    # Protected Attributes
    # --------------------

    #: Character representing a _comment in a Gromacs topology file
    _comment = ReadOnly(';')

    # ------------------
    #     Defaults
    # ------------------

    def __ext_default(self):
        """Default extension for this reader subclass"""
        return 'itp'

    # ------------------
    #  Private Methods
    # ------------------

    def _remove_comments(self, file_lines):
        """Removes comments and whitespace from parsed topology
        file lines"""

        file_lines = [line.split(self._comment)[0] for line in file_lines
                      if not line.startswith(self._comment)]

        file_lines = [line.strip() for line in file_lines
                      if not line.isspace()]

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
            raise IOError('Gromacs topology file does not include any'
                          ' molecule types')
        mol_sections = []
        start_indices = mol_indices
        end_indices = mol_indices[1:] + [None]

        # Extract the relevant lines in the topology file that correspond
        # to each molecule
        for start, end in zip(start_indices, end_indices):
            mol_sections.append(file_lines[start:end])

        return mol_sections

    def _get_data(self, file_lines):
        """ Load data for each target molecule type in Gromacs topology

        Parameters
        ----------
        file_lines : list of str
            List containing lines in topology file as strings

        Returns
        -------
        atoms : list of str
            List of atoms in each target molecular type
        charges : list of int
            List of electronic charges corresponding to each target molecular
            type
        masses : list of float
            List of atomic masses corresponding to each target molecular type
        """

        mol_sections = self._get_molecule_sections(file_lines)

        symbols = []
        atoms = []
        charges = []
        masses = []

        for section in mol_sections:

            # Get symbols that correspond to each molecule type
            symbol = section[1].split()[0]

            # Find file location of atom list for target molecule
            atom_indices = [index + 1 for index, line
                            in enumerate(section) if "atoms" in line]

            atoms_index = atom_indices[0]

            # Read the name, charge and mass of each atom/bead, which should
            # be included at indices 4, 6 and 7 respectively
            atom = []
            charge = 0
            mass = 0
            for line in section[atoms_index:]:
                if line.startswith('['):
                    break
                else:
                    file_line = line.split(self._comment)[0]
                    file_line = file_line.split()

                    atom.append(file_line[4])
                    charge += float(file_line[6])
                    mass += float(file_line[7])

            symbols.append(symbol)
            atoms.append(atom)
            charges.append(charge)
            masses.append(mass)

        return symbols, atoms, charges, masses

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
        except (IndexError, IOError) as e:
            log.exception('unable to load data from "{}"'.format(file_path))
            raise e

        data = {
            symbol: {
                'atoms': atom,
                'charge': charge,
                'mass': mass
            }
            for symbol, atom, charge, mass in zip(*iterator)
        }

        return data
