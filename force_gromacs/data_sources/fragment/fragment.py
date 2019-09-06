from traits.api import HasTraits, Unicode, File

from force_bdss.api import DataValue


class Fragment(HasTraits):
    """Contains all input values for each molecular fragment. A
    fragment is defined as a part of a molecule that may become
    dissociated (i.e - an ion) and therefore requires its own set
    of chemical / structural information"""

    #: Human readable name for reference
    name = Unicode()

    #: Symbol referring to fragment in Gromacs input files
    symbol = Unicode()

    #: Gromacs topology '.itp' file
    topology = File()

    #: Gromacs coordinate '.gro' file
    coordinate = File()

    def get_data_values(self):
        """Return a list containing all DataValues stored in class"""

        return [
            DataValue(type="NAME", value=self.name),
            DataValue(type="SYMBOL", value=self.symbol),
            DataValue(type="TOPOLOGY", value=self.topology),
            DataValue(type="COORDINATE", value=self.coordinate)
        ]
