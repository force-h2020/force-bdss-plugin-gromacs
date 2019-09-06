import copy

from force_bdss.api import BaseDataSource, DataValue, Slot

from force_gromacs.data_sources.molecule import (
    Molecule
)


class MoleculeDataSource(BaseDataSource):
    """Class that collates a set of molecular `Fragment` instances into
    a single chemical `Molecule`.
    """

    def _make_local_parameter_copy(self, parameters):
        """Makes a local copy of any `parameter.value` attributes being
         passed into the DataSource."""
        for parameter in parameters:
            parameter.value = copy.copy(parameter.value)

    def _assign_stoichiometry(self, model, parameters):
        """Assign stoichiometric number to each `Fragment` present in
        parameters"""

        fragments = [parameter.value for parameter in parameters
                     if parameter.type == 'FRAGMENT']

        for number, fragment in zip(model.fragment_numbers, fragments):
            fragment.number = number

    def run(self, model, parameters):
        """Takes in all constituent fragments and assigns stoichiometric
        numbers to produce a Molecule object"""

        self._make_local_parameter_copy(parameters)

        self._assign_stoichiometry(model, parameters)

        fragments = [parameter.value for parameter in parameters
                     if parameter.type == 'FRAGMENT']

        molecule = Molecule(
            fragments=fragments
        )

        return [DataValue(type='MOLECULE', value=molecule)]

    def slots(self, model):

        input_slots = tuple(
                Slot(description=f"Molecular fragment {index + 1} data",
                     type="FRAGMENT") for index in range(model.n_fragments)
            )

        return (
            input_slots,
            (
                Slot(description=f"Molecule for a simulation",
                     type="MOLECULE"),
            )
        )
