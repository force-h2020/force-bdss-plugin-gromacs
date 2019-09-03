from traits.api import HasTraits, Unicode, Float, File

from force_bdss.api import DataValue


class Chemical(HasTraits):
    """Contains all input values for each chemical"""

    name = Unicode()

    symbol = Unicode()

    mass = Float()

    charge = Float()

    topology = File()

    coordinate = File()

    def get_data_values(self):
        """Return a list containing all DataValues stored in class"""

        return [
            DataValue(type="NAME", value=self.name),
            DataValue(type="MASS", value=self.mass),
            DataValue(type="CHARGE", value=self.charge),
            DataValue(type="SYMBOL", value=self.symbol),
            DataValue(type="TOPOLOGY", value=self.topology),
            DataValue(type="COORDINATE", value=self.coordinate)
        ]
