from force_bdss.api import BaseDataSource, DataValue, Slot

from force_gromacs.io.gromacs_topology_reader import (
    GromacsTopologyReader
)

from .chemical import Chemical


class ChemicalDataSource(BaseDataSource):
    """Class takes in all data required to define each
    separate chemical chemical in a Gromacs experiment. Gromacs topology
    files must be included for all species, however coordinate files
    are not necessary for atoms or molecules represented by single beads.
    """

    def run(self, model, parameters):

        reader = GromacsTopologyReader()

        data = reader.read(model.topology)

        charge = data[model.symbol]['charge']
        mass = data[model.symbol]['mass']

        chemical = Chemical(
            name=model.name,
            symbol=model.symbol,
            mass=mass,
            charge=charge,
            topology=model.topology,
            coordinate=model.coordinate
        )

        return [
            DataValue(type="CHEMICAL", value=chemical)]

    def slots(self, model):

        return (
            (
            ),
            (
                Slot(type="CHEMICAL",
                     description="Chemical chemical data object"),
            )
        )
