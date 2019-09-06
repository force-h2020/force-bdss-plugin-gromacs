from traits.api import (
    HasTraits, Unicode, File, Int, List, Float, Property, Dict,
    cached_property
)

from force_bdss.api import DataValue

from force_gromacs.io.gromacs_topology_reader import (
    GromacsTopologyReader
)


class Fragment(HasTraits):
    """Contains all input values for each molecular fragment. A
    fragment is defined as a part of a fragment that may become
    dissociated (i.e - an ion) and therefore requires its own set
    of chemical / structural information"""

    # --------------------
    #  Required Attributes
    # --------------------

    #: Symbol referring to fragment in Gromacs input files
    symbol = Unicode()

    #: Gromacs topology '.itp' file
    topology = File()

    #: Gromacs coordinate '.gro' file
    coordinate = File()

    # --------------------
    #  Regular Attributes
    # --------------------

    #: Human readable name for reference
    name = Unicode()

    #: Stoichiometric number of molecular fragment
    number = Int(1)

    # --------------------
    #     Properties
    # --------------------

    #: Parsed Gromacs topology data of fragment
    _data = Property(Dict, depends_on='topology')

    #: List of atoms in Gromacs topology '.itp' file
    atoms = Property(List(Unicode), depends_on='_data')

    #: Molecular mass in Gromacs topology '.itp' file
    mass = Property(Float, depends_on='_data')

    #: Molecular charge in Gromacs topology '.itp' file
    charge = Property(Float, depends_on='_data')

    # --------------------
    #  Private Attributes
    # --------------------

    #: Gromacs topology '.itp' file reader
    _reader = GromacsTopologyReader()

    @cached_property
    def _get__data(self):
        data = self._reader.read(self.topology)
        return data[self.symbol]

    def _get_atoms(self):
        if self._data is not None:
            return self._data['atoms']

    def _get_mass(self):
        if self._data is not None:
            return self._data['mass']

    def _get_charge(self):
        if self._data is not None:
            return self._data['charge']

    def get_data_values(self):
        """Return a list containing all DataValues stored in class"""

        return [
            DataValue(type="NAME", value=self.name),
            DataValue(type="SYMBOL", value=self.symbol),
            DataValue(type="ATOMS", value=self.atoms),
            DataValue(type="MASS", value=self.mass),
            DataValue(type="CHARGE", value=self.charge),
            DataValue(type="TOPOLOGY", value=self.topology),
            DataValue(type="COORDINATE", value=self.coordinate)
        ]
