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

    #: Topology reader that can be used to parse '.itp' files
    reader = GromacsTopologyReader()

    def run(self, model, parameters):
        """Simply wraps all user input in a `Molecule` object for further
        processing. Consequently, it is expected that either this method
        can be overloaded by a subclass to perform more specific actions,
        of additional `DataSource` objects can perform this in the next
        `ExecutionLayer`"""

        molecule = Molecule(
            name=model.name,
            symbol=model.symbol,
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
