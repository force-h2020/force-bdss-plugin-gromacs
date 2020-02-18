import logging

from force_gromacs.chemicals.gromacs_fragment import GromacsFragment
from force_gromacs.chemicals.gromacs_particle import GromacsParticle

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

    def _parse_line(self, line):
        """Separate each value from the line"""
        file_line = line.split(self._comment)[0]
        file_line = file_line.split()

        return file_line

    def _parse_atom_line(self, line):
        """Parse line in gromacs molecule file that refers to an atom"""
        file_line = self._parse_line(line)

        index = int(file_line[0])
        element = file_line[1]
        mol_label = file_line[3]
        at_label = file_line[4]
        at_index = int(file_line[5])
        charge = float(file_line[6])
        mass = float(file_line[7])

        return index, element, mol_label, at_label, at_index, charge, mass

    def _parse_bond_line(self, line):
        """Parse line in gromacs molecule file that refers to bond
        between two atoms"""
        file_line = self._parse_line(line)

        atom_1 = int(file_line[0])
        atom_2 = int(file_line[1])

        return atom_1, atom_2

    def _get_data(self, file_lines):
        """ Load data for each target molecule type in Gromacs topology

        Parameters
        ----------
        file_lines : list of str
            List containing lines in topology file as strings

        Returns
        -------
        fragments : list of GromacsFragment
            List of GromacsFragment instances representing molecular fragment
        """

        mol_sections = self._get_molecule_sections(file_lines)

        fragments = []

        for section in mol_sections:

            # Get symbols that correspond to each molecule type
            symbol = section[1].split()[0]

            fragment = GromacsFragment(
                symbol=symbol
            )

            # Find file location of atom list for target molecule
            atom_indices = [index + 1 for index, line
                            in enumerate(section) if "atoms" in line]

            # Read the name, charge and mass of each atom/bead, which should
            # be included at indices 4, 6 and 7 respectively
            for atoms_index in atom_indices:
                for line in section[atoms_index:]:
                    if line.startswith('['):
                        break
                    else:
                        (_, element, _, at_label,
                         at_index, charge, mass) = self._parse_atom_line(line)
                        fragment.particles.append(
                            GromacsParticle(
                                index=at_index,
                                id=at_label,
                                element=element,
                                charge=charge,
                                mass=mass)
                        )

            # Find file location of atom list for target molecule
            bond_indices = [index + 1 for index, line
                            in enumerate(section) if "bonds" in line]

            # Read the atom indices of each bond
            for bonds_index in bond_indices:
                for line in section[bonds_index:]:
                    if line.startswith('['):
                        break
                    else:
                        bond = self._parse_bond_line(line)
                        fragment.bonds.append(bond)

            fragments.append(fragment)

        return fragments

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
            fragments = self._get_data(file_lines)
        except Exception as e:
            log.exception('unable to load data from "{}"'.format(file_path))
            raise e

        for fragment in fragments:
            fragment.topology = file_path

        return fragments
