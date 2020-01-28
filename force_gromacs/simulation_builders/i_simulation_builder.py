from traits.api import Interface, Str, Int, Bool


class ISimulationBuilder(Interface):
    """Class that creates a pipeline for a specific simulation"""

    # --------------------
    #  Required Attributes
    # --------------------

    #: Reference name of simulation
    name = Str()

    #: Particle size of simulation
    size = Int()

    #: Location to create simulation file tree in.
    directory = Str()

    #: Whether or not to perform an MPI parallel run
    mpi_run = Bool()

    #: Number of processors required for MPI run
    n_proc = Int()

    #: Whether or not to perform a dry run
    dry_run = Bool()

    def build_pipeline(self):
        """Method to be implemented that returns a `GromacsPipeline`
        object containing all commands required to set up and perform a
        simulation"""

    def get_results_path(self):
        """Obtain the results trajectory file path for further
        post-processing"""
