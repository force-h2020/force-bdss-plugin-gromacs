from traits.api import (
    HasTraits, Unicode, Int, Bool, Instance, Dict
)

from force_gromacs.pipeline.gromacs_pipeline import (
    GromacsPipeline
)


class GromacsSimulationBuilder(HasTraits):
    """Class that creates a GromacsPipeline object for a specific
    simulation"""

    # --------------------
    #  Required Attributes
    # --------------------

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

    # --------------------
    #  Regular Attributes
    # --------------------

    #: GromacsPipeline object to be constructed
    pipeline = Instance(GromacsPipeline)

    #: Current data to be included in human readable topology file
    topology_data = Dict()

    #: Base folder for simulation data
    _folder = Unicode()

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

    # --------------------
    #      Defaults
    # --------------------

    def _pipeline_default(self):
        return GromacsPipeline(dry_run=self.dry_run)

    def _topology_data_default(self):
        return {'topologies': [],
                'fragment_dict': {}}

    def __folder_default(self):
        return '/'.join([self.directory, self.name])

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

    # --------------------
    #    Private Methods
    # --------------------

    def _update_topology_data(self, topology=None, symbol=None, n_mol=0):
        """Updates attribute _topology_data, which stores data to write
        to a human readable Gromacs topology file"""

        if topology is not None:
            if topology not in self.topology_data['topologies']:
                self.topology_data['topologies'].append(topology)

        if symbol is not None:
            if symbol not in self.topology_data['fragment_dict']:
                self.topology_data['fragment_dict'][symbol] = 0

            self.topology_data['fragment_dict'][symbol] += n_mol

    # --------------------
    #    Public Methods
    # --------------------

    def build_pipeline(self):
        """Method to be implemented that returns a `GromacsPipeline`
        object containing all commands required to set up and perform a
        simulation"""
        raise NotImplementedError(
            'Subclass does not contain an implementation of '
            '`build_pipeline` method'
        )
