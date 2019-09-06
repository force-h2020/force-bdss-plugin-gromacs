from traits.api import Int, List, on_trait_change

from force_bdss.api import BaseDataSourceModel, VerifierError


class MoleculeDataSourceModel(BaseDataSourceModel):
    """Class containing all fragments to create for a single Gromacs
    `Molecule` object"""

    #: Number of molecular fragments
    n_fragments = Int(1,
                      desc='Number of constituent fragments',
                      changes_slots=True, verify=True)

    #: Stoichiometric numbers of each molecular fragment
    fragment_numbers = List(
        Int, desc='Stoichiometric numbers of each fragment in molecule'
    )

    def _fragment_numbers_default(self):
        return [1 for _ in range(self.n_fragments)]

    @on_trait_change('n_fragments')
    def update_fragment_numbers(self):
        """Updates length of fragment_numbers list to equal
        n_fragments"""
        while len(self.fragment_numbers) != self.n_fragments:
            if len(self.fragment_numbers) < self.n_fragments:
                self.fragment_numbers.append(1)
            else:
                self.fragment_numbers = self.fragment_numbers[:-1]

    def _n_fragments_check(self):
        """Makes sure there is at least 1 molecular fragment in
        the Ingredient"""

        errors = []
        if self.n_fragments < 1:
            errors.append(
                VerifierError(
                    subject=self,
                    local_error="Number of molecular fragments must"
                                " be at least 1",
                    global_error="An IngredientDataSource does not "
                                 "have enough molecular fragments defined"
                )
            )

        return errors

    def verify(self):
        """Overloads BaseDataSourceModel verify method to check the
        number of Molecules during a verify_workflow_event"""

        errors = super(MoleculeDataSourceModel, self).verify()
        errors += self._n_fragments_check()

        return errors
