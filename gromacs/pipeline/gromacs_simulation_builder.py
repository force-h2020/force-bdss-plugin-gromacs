from traits.api import HasTraits, Unicode, Int, Bool, Instance

from gromacs.pipeline.gromacs_pipeline import (
    GromacsPipeline
)


class GromacsSimulationBuilder(HasTraits):
    """Class that creates a GromacsPipeline object for a specific
    simulation"""

    #: Reference name of simulation
    name = Unicode()

    #: Particle size of simulation
    size = Int()

    #: Location to create simulation file tree in. (By default,
    #: the current working directory)
    directory = Unicode('.')

    #: Location of MARTINI bead parameter file
    martini_parameters = Unicode()

    #: Whether or not to perform an MPI parallel run
    mpi_run = Bool(False)

    #: Number of processors required for MPI run
    n_proc = Int(1)

    #: Whether or not to perform a dry run
    dry_run = Bool(True)

    pipeline = Instance(GromacsPipeline)

    #: Output coordinate file name
    _coord_file = Unicode()

    #: Output binary file name
    _binary_file = Unicode()

    #: Output topology file name
    _top_file = Unicode()

    #: Output energy file name
    _energy_file = Unicode()

    #: Output trajectory file name
    _traj_file = Unicode()

    #: Output log file name
    _log_file = Unicode()

    #: Output state file name
    _state_file = Unicode()

    def _pipeline_default(self):
        return GromacsPipeline(dry_run=self.dry_run)

    def __coord_file_default(self):
        return self.name + '_coord.gro'

    def __binary_file_default(self):
        return self.name + '_topol.tpr'

    def __top_file_default(self):
        return self.name + '_topol.top'

    def __energy_file_default(self):
        return self.name + '_ener.edr'

    def __traj_file_default(self):
        return self.name + '_traj'

    def __log_file_default(self):
        return self.name + '_md.log'

    def __state_file_default(self):
        return self.name + '_state.cpt'

    def build_pipeline(self):
        raise NotImplementedError
