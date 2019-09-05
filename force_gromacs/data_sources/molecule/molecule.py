from traits.api import HasTraits, Unicode, File

from force_bdss.api import DataValue


class Molecule(HasTraits):
    """Contains all input values for each molecule"""

    #: Human readable name for reference
    name = Unicode()

    #: Symbol referring to molecule in Gromacs input files
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
