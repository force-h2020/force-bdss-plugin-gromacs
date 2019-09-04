from force_bdss.api import BaseDataSource, DataValue, Slot

from force_gromacs.io.gromacs_topology_reader import (
    GromacsTopologyReader
)

from .molecule import Molecule


class MoleculeDataSource(BaseDataSource):
    """Class takes in all data required to define each
    separate molecule molecule in a Gromacs experiment. Gromacs topology
    files must be included for all species, however coordinate files
    are not necessary for atoms or molecules represented by single beads.
    """

    def run(self, model, parameters):

        reader = GromacsTopologyReader()

        data = reader.read(model.topology)

        charge = data[model.symbol]['charge']
        mass = data[model.symbol]['mass']

        molecule = Molecule(
            name=model.name,
            symbol=model.symbol,
            mass=mass,
            charge=charge,
            topology=model.topology,
            coordinate=model.coordinate
        )

        return [
            DataValue(type="MOLECULE", value=molecule)]

    def slots(self, model):

        return (
            (
            ),
            (
                Slot(type="MOLECULE",
                     description="Gromacs Molecule data object"),
            )
        )
