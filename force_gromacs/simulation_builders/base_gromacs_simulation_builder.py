from force_gromacs.simulation_builders.gromacs_topology_data import GromacsTopologyData
from traits.api import (
    HasTraits, Str, Int, Bool, Instance, Directory,
    File, provides
)

from force_gromacs.pipelines.gromacs_pipeline import GromacsPipeline
from force_gromacs.simulation_builders.i_simulation_builder import (
    ISimulationBuilder
)


@provides(ISimulationBuilder)
class BaseGromacsSimulationBuilder(HasTraits):
    """Class that creates a GromacsPipeline object for a specific
    simulation"""

    # --------------------
    #  Required Attributes
    # --------------------

    #: Reference name of simulation
    name = Str()

    #: Particle size of simulation
    size = Int()

    #: Location to create simulation file tree in. (By default,
    #: the current working directory)
    directory = Str('.')

    #: Location of MARTINI bead parameter file
    martini_parameters = Str()

    #: Whether or not to perform an MPI parallel run
    mpi_run = Bool(False)

    #: Number of processors required for MPI run
    n_proc = Int(1)

    #: Whether or not to perform a dry run
    dry_run = Bool(True)

    # --------------------
    #  Regular Attributes
    # --------------------

    #: Current data to be included in human readable topology file
    topology_data = Instance(GromacsTopologyData)

    #: Base folder for simulation data
    folder = Directory()

    #: Output coordinate file name
    coord_file = File()

    #: Output binary file name
    binary_file = File()

    #: Output topology file name
    top_file = File()

    #: Output energy file name
    energy_file = File()

    #: Output trajectory file name
    traj_file = File()

    #: Output log file name
    log_file = File()

    #: Output state file name
    state_file = File()

    # --------------------
    #  Private Attributes
    # --------------------

    #: GromacsPipeline object to be constructed. Kept as a private
    #: attribute, since should only be obtained as a completed instance
    #: via `build_pipeline`
    _pipeline = Instance(GromacsPipeline)

    # --------------------
    #      Defaults
    # --------------------

    def _topology_data_default(self):
        return GromacsTopologyData()

    def _folder_default(self):
        return '/'.join([self.directory, self.name])

    def _coord_file_default(self):
        return self.name + '_coord.gro'

    def _binary_file_default(self):
        return self.name + '_topol.tpr'

    def _top_file_default(self):
        return self.name + '_topol.top'

    def _energy_file_default(self):
        return self.name + '_ener.edr'

    def _traj_file_default(self):
        return self.name + '_traj'

    def _log_file_default(self):
        return self.name + '_md.log'

    def _state_file_default(self):
        return self.name + '_state.cpt'

    def __pipeline_default(self):
        return GromacsPipeline(dry_run=self.dry_run)

    # --------------------
    #    Public Methods
    # --------------------

    def build_pipeline(self):
        """Method to be implemented that returns a `GromacsPipeline`
        object containing all commands required to set up and perform a
        simulation

        Returns
        -------
        pipeline: GromacsPipeline
            An object capable of calling a Gromacs simulation from the
            command line
        """
        raise NotImplementedError(
            'Subclass does not contain an implementation of '
            '`build_pipeline` method'
        )

    def get_results_path(self):
        """Obtain the results trajectory file path for further
        post-processing

        Returns
        -------
        results_path: str
            The absolute file path for the production run Gromacs
            simulation trajectory (i.e - the coordinate data to be
            analysed)
        """
        raise NotImplementedError(
            'Subclass does not contain an implementation of '
            '`get_results_path` method'
        )
