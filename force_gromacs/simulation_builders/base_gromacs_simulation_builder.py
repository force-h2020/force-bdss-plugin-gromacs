#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.
import os

from traits.api import (
    HasTraits, Str, Int, Bool, Instance, Directory,
    provides
)

from force_gromacs.io.gromacs_file_registry import GromacsFileRegistry
from force_gromacs.pipelines.gromacs_pipeline import GromacsPipeline
from force_gromacs.simulation_builders.gromacs_topology_data import (
    GromacsTopologyData
)
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

    #: Length of simulation in time steps
    n_steps = Int()

    #: Location to create simulation file tree in. (By default,
    #: the current working directory)
    directory = Directory('.')

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

    #: Folder to create for beginning of simulation file tree
    folder = Directory()

    #: Current data to be included in human readable topology file
    topology_data = Instance(GromacsTopologyData)

    #: GromacsFileRegistry containing instructions how to format each file
    #: type
    file_registry = Instance(GromacsFileRegistry)

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

    def _folder_default(self):
        return os.path.join(self.directory, self.name)

    def _topology_data_default(self):
        return GromacsTopologyData()

    def _file_registry_default(self):
        return GromacsFileRegistry(prefix=self.name)

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
