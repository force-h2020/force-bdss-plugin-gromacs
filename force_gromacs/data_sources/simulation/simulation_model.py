from traits.api import Unicode, Bool, Int, File, Instance
from traitsui.api import View, Item

from force_bdss.api import (
    BaseDataSourceModel, BaseDriverEvent, VerifierError
)


class SimulationDataSourceModel(BaseDataSourceModel):
    """Class that inputs all required parameters for a single
    Gromacs simulation"""

    #: Name of simulation
    name = Unicode('simulation')

    #: Number of Molecules
    n_molecules = Int(1,
                      desc='Number of constituent molecules',
                      changes_slots=True, verify=True)

    #: Total number of fragments in simulation
    size = Int(1000)

    #: Whether or not to perform a dry run of Gromacs
    dry_run = Bool(True)

    #: Whether or not to perform a MPI run
    mpi_run = Bool(False)

    #: Number of processors for MPI run
    n_proc = Int(1)

    #: File path for Gromacs MARTINI paramters file
    martini_parameters = File(
        desc='File path for Gromacs MARTINI Parameter file')

    #: File path for Gromacs Energy minimisation parameters file
    md_min_parameters = File(
        desc='File path for Gromacs MD Parameter file')

    #: File path for Gromacs Production run parameters file
    md_prod_parameters = File(
        desc='File path for Gromacs MD Parameter file')

    #: Propagation channel for events from the SimulationDataSource
    driver_event = Instance(BaseDriverEvent)

    traits_view = View(
        Item('name'),
        Item("size"),
        Item('mpi_run'),
        Item("n_proc", visible_when='mpi_run'),
        Item('martini_parameters'),
        Item('md_min_parameters'),
        Item('md_prod_parameters'),
        Item("dry_run")
    )

    def _n_molecules_check(self):
        """Makes sure there is at least 1 Molecule type in the
        Simulation"""

        errors = []
        if self.n_molecules < 1:
            errors.append(
                VerifierError(
                    subject=self,
                    local_error="Number of molecule types must"
                                " be at least 1",
                    global_error="A SimulationDataSourceModel does not "
                                 "have enough molecular types defined"
                )
            )

        return errors

    def verify(self):
        """Overloads BaseDataSourceModel verify method to check the
        number of Molecules during a verify_workflow_event"""

        errors = super(SimulationDataSourceModel, self).verify()
        errors += self._n_molecules_check()

        return errors
