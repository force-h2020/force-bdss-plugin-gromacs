from force_bdss.api import BaseDataSource, DataValue, Slot

from .gromacs_fragment import GromacsFragment


class FragmentDataSource(BaseDataSource):
    """Class takes in all data required to define each
    separate molecular fragment in a Gromacs experiment. Gromacs topology
    files must be included for all species, however coordinate files
    are not necessary for atoms or molecules represented by single beads.
    """

    def run(self, model, parameters):
        """Simply wraps all user input in a `GromacsFragment` object for further
        processing. Consequently, it is expected that either this method
        can be overloaded by a subclass to perform more specific actions,
        of additional `DataSource` objects can perform this in the next
        `ExecutionLayer`"""

        fragment = GromacsFragment(
            name=model.name,
            symbol=model.symbol,
            topology=model.topology,
            coordinate=model.coordinate
        )

        return [
            DataValue(type="FRAGMENT", value=fragment)]

    def slots(self, model):
        return (
            (
            ),
            (
                Slot(type="FRAGMENT",
                     description="Gromacs GromacsFragment data object"),
            )
        )
