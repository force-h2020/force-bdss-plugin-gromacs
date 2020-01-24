from traits.api import Unicode, Bool, Int, File, Instance
from traitsui.api import View, Item

from force_bdss.api import (
    BaseDataSourceModel, BaseDriverEvent, VerifierError
)

from force_gromacs.notification_listeners.driver_events import (
    SimulationProgressEvent)


class SimulationDataSourceModel(BaseDataSourceModel):
    """Class that inputs all required parameters for a single
    Gromacs simulation"""

    # --------------------
    #  Required Attributes
    # --------------------

    #: Name of simulation
    name = Unicode('simulation')

    #: Number of Molecules
    n_molecule_types = Int(
        1, desc='Number of types of constiuent molecules',
        changes_slots=True, verify=True)

    #: Total number of fragments in simulation
    size = Int(1000)

    #: Whether or not to overwrite existing simulation data
    ow_data = Bool(False)

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

    # --------------------
    #        View
    # --------------------

    traits_view = View(
        Item('name'),
        Item("size"),
        Item('mpi_run'),
        Item("n_proc", visible_when='mpi_run'),
        Item('martini_parameters'),
        Item('md_min_parameters'),
        Item('md_prod_parameters'),
        Item("ow_data", label='Overwrite simulation data'),
        Item("dry_run")
    )

    # --------------------
    #   Private Methods
    # --------------------

    def _n_molecule_types_check(self):
        """Makes sure there is at least 1 Molecule type in the
        Simulation"""

        errors = []
        if self.n_molecule_types < 1:
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

    # --------------------
    #    Public Methods
    # --------------------

    def verify(self):
        """Overloads BaseDataSourceModel verify method to check the
        number of Molecules during a verify_workflow_event"""

        errors = super(SimulationDataSourceModel, self).verify()
        errors += self._n_molecule_types_check()

        return errors

    def notify_bash_script(self, bash_script):
        """Notify the construction of a bash script for a Gromacs
        simulation. Assigns an `SimulationProgressEvent` to the
        `event` attribute. By doing so it can be picked
        up by the `Workflow` and passed onto any
        `NotificationListeners` present.

        Parameters
        ----------
        bash_script: str
            A string containing the constructed
            bash script to run a Gromacs simulation.
        """
        self.event = SimulationProgressEvent(
            bash_script=bash_script
        )
