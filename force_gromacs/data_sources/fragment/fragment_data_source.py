from force_bdss.api import BaseDataSource, DataValue, Slot

from force_gromacs.io.gromacs_molecule_reader import GromacsMoleculeReader


class FragmentDataSource(BaseDataSource):
    """Class takes in all data required to define each
    separate molecular fragment in a Gromacs experiment. Gromacs topology
    files must be included for all species, however coordinate files
    are not necessary for atoms or molecules represented by single beads.
    """

    _reader = GromacsMoleculeReader()

    def run(self, model, parameters):
        """Simply wraps all user input in a `GromacsFragment` object for further
        processing. Consequently, it is expected that either this method
        can be overloaded by a subclass to perform more specific actions,
        of additional `DataSource` objects can perform this in the next
        `ExecutionLayer`"""

        fragments = self._reader.read(
            model.topology
        )

        index = [
            index for index, fragment in enumerate(fragments)
            if fragment.symbol == model.symbol
        ][0]

        fragment = fragments[index]

        if model.name:
            fragment.name = model.name

        if model.coordinate:
            fragment.coordinate = model.coordinate

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
