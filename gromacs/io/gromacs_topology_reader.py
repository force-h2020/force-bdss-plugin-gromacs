import logging

from traits.api import HasTraits, ReadOnly

log = logging.getLogger(__name__)


class GromacsTopologyReader(HasTraits):
    """  Class parses Gromacs file and returns data required for
    each molecular type listed in the symbols input argument.
    """

    # --------------------
    # Protected Attributes
    # --------------------

    #: Character representing a _comment in a Gromacs topology file
    _comment = ReadOnly(';')

    #: Extension of accepted file types
    _ext = ReadOnly('itp')

    # ------------------
    #  Private Methods
    # ------------------

    def _read_file(self, gromacs_file):
        """Simple file loader"""

        self.check_file_types(gromacs_file)

        with open(gromacs_file, 'r') as infile:
            file_lines = infile.readlines()

        return file_lines

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

    def check_file_types(self, file_path):
        """ Raise exception if specified Gromacs file does not have
        expected format"""

        space_check = file_path.isspace()
        ext_check = not file_path.endswith(f'.{self._ext}')

        if space_check or ext_check:
            raise IOError(
                '{} not a valid Gromacs file type'.format(
                    file_path))

    def read(self, gromacs_file):
        """ Open Gromacs topology file and return processed data

        Parameters
        ----------
        topology : str
            File path of Gromacs topology file

        Returns
        -------
        data : dict ('size': [list of int], 'mass': [list of floats])
            Dictionary containing data extracted and processed by
            handler. Keys 'size' refers to the number of atoms in each
            molecule and 'masses' the mass in atomic units.
        """

        try:
            file_lines = self._read_file(gromacs_file)
        except IOError as e:
            log.exception('unable to open "{}"'.format(gromacs_file))
            raise e

        file_lines = self._remove_comments(file_lines)

        try:
            iterator = self._get_data(file_lines)
        except (IndexError, IOError) as e:
            log.exception('unable to load data from "{}"'.format(gromacs_file))
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
