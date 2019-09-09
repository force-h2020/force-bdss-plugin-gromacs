import numpy as np

from traits.api import Int, List, on_trait_change
from traitsui.api import View, Item, ListEditor

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

    # ------------------
    #       View
    # ------------------

    def default_traits_view(self):
        """Provides view with display information for fragment_numbers
        trait"""
        list_editor = ListEditor(mutable=False)
        return View(
            Item('n_fragments'),
            Item('fragment_numbers', editor=list_editor)
        )

    def _fragment_numbers_default(self):
        return [1] * self.n_fragments

    @on_trait_change('n_fragments')
    def update_fragment_numbers(self):
        """Updates length of fragment_numbers list to equal
        n_fragments"""

        n = self.n_fragments - len(self.fragment_numbers)

        if n > 0:
            self.fragment_numbers += [1] * n
        elif n < 0:
            self.fragment_numbers = self.fragment_numbers[:n]

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
