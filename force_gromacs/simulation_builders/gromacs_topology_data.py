from traits.api import HasStrictTraits, List, File, Dict, Str, Int

from force_gromacs.io.gromacs_molecule_reader import (
    GromacsMoleculeReader
)


class GromacsTopologyData(HasStrictTraits):
    """Container class for information relating to the
    simulation chemical topologies. These describe the molecular
    models included within the system.

    Note: we presume all forcefield parameters for each molecular fragment
    are contained within seperate '.itp' files"""

    #: List of Gromacs include molecule topology files (.itp) containing
    #: forcefield model information for each fragment
    molecule_files = List(File)

    #: Data referring to each fragment species used in this
    #: simulation. These include the keys corresponding to models
    #: provided in the given topology files
    fragment_ledger = Dict(Str, Int)

    # --------------------
    #  Private Attributes
    # --------------------

    #: Reader required to parse .itp files
    _reader = GromacsMoleculeReader()

    # --------------------
    #    Public Methods
    # --------------------

    def add_molecule_file(self, molecule_file):
        """Adds topology file to topology_files list if not
        already included"""
        if molecule_file not in self.molecule_files:
            self.molecule_files.append(molecule_file)

    def remove_molecule_file(self, molecule_file):
        """Removes topology file from topology_files list if present"""
        if molecule_file in self.molecule_files:
            self.molecule_files.remove(molecule_file)

    def add_fragment(self, symbol, number=0):
        """Adds fragment symbol and number to `fragment_ledger` if not
        already included. Else adds number particles to the existing
        total"""
        if symbol not in self.fragment_ledger:
            self.fragment_ledger[symbol] = number

    def remove_fragment(self, symbol):
        """Removes fragment symbol and number from `fragment_ledger` if
        present"""
        self.fragment_ledger.pop(symbol, None)

    def edit_fragment_number(self, symbol, number):
        """Adds `number` particles to the `fragment_ledger` entry
        represented by `symbol`. If the number of particles becomes
        less than 1, remove the fragment from the ledger"""

        self.fragment_ledger[symbol] += number

        if self.fragment_ledger[symbol] < 1:
            self.remove_fragment(symbol)

    def verify(self):
        """Checks that each file listed in `itp_files` is readable and that
        each fragment in the `fragment_ledger` is referenced in at least
        one topology"""

        # Build cache of fragment types included in topology files
        fragment_cache = []

        for molecule_file in self.molecule_files:
            try:
                data = self._reader.read(molecule_file)
            except IOError:
                return False
            fragment_cache.extend(list(data.keys()))

        # Check that all fragments in ledger are represented
        for symbol in self.fragment_ledger.keys():
            if symbol not in fragment_cache:
                return False

        return True
