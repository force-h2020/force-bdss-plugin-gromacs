from traits.api import Interface, Unicode, Int, Bool


class ISimulationBuilder(Interface):
    """Class that creates a pipeline for a specific simulation"""

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

    #: Whether or not to perform an MPI parallel run
    mpi_run = Bool(False)

    #: Number of processors required for MPI run
    n_proc = Int(1)

    #: Whether or not to perform a dry run
    dry_run = Bool(True)

    def build_pipeline(self):
        """Method to be implemented that returns a `GromacsPipeline`
        object containing all commands required to set up and perform a
        simulation"""

    def get_results_path(self):
        """Obtain the results trajectory file path for further
        post-processing"""
