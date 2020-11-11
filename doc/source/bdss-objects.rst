BDSS Plugin Objects
===================

The FORCE Gromacs plugin also contributes serveral BDSS objects that can be used either
out of the box or provide a base class for further customization.

Data Sources
------------

FragmentDataSource
~~~~~~~~~~~~~~~~~~

The ``FragmentDataSource`` class provides an interface for a BDSS user to create a ``GromacsFragment`` that
can be propagated through a Workflow as a ``DataValue``. The data source takes no input parameters, and produces
a single output parameter, which is the ``GromacsFragment`` instance being constructed. Therefore it can be considered
as a factory of ``GromacsFragment`` objects.

The following information must be provided in the model interface:

- **Name**: A human readable name of the fragment.
- **Symbol**: The symbol that is used to idenfity the fragment in GROMACS input files
- **Coordinate**: A path to the GROMACS coordinate ``.gro`` file that described the fragment's geometry
- **Topology**: A path to the GROMACS topology ``.itp`` file that described the fragment's force field parameters

MoleculeDataSource
~~~~~~~~~~~~~~~~~~

The ``MoleculeDataSource`` class provides an interface for a BDSS user to create a ``GromacsMolecule`` that
can be propagated through a Workflow as a ``DataValue``. The data source takes one or more ``GromacsFragment``
input parameters, and produces a single output parameter, which is the ``GromacsMolecule`` instance being constructed.
Therefore it can be considered as a factory of ``GromacsMolecule`` objects.

The following information must be provided in the model interface:

- **No. Fragment Types**: The number of different fragment types in the molecule
- **Fragment Numbers**: The stoichiometric number of each fragment type in the molecule

SimulationDataSource
~~~~~~~~~~~~~~~~~~~~

The ``SimulationDataSource`` base class provides an interface for a BDSS user to create and run a
``BaseGromacsSimulationBuilder`` instance that can construct and perform a ``GromacsPipeline`` object.
The data source takes one or more ``GromacsMolecule`` input parameters, and produces a single output parameter,
which is the file path to the GROMACS trajectory file that is expected to be post-processed by further data sources.

The data source requires developers to implement the ``create_simulation_builder`` method, which produces
a ``BaseGromacsSimulationBuilder`` instance.

.. code-block:: python

    def create_simulation_builder(self, model, parameters):
        """Method that returns a `GromacsSimulationBuilder` object capable
        of generating a `GromacsPipeline`

        Parameters
        ----------
        model: SimulationDataSourceModel
            The BaseDataSourceModel associated with this class
        parameters: List(DataValue)
            a list of DataValue objects containing the information needed
            for the execution of the DataSource.

        Returns
        -------
        simulation_builder: BaseGromacsSimulationBuilder
            An object capable of generating a GromacsPipeline that calls
            a Gromacs simulation
        """

It also emits a ``SimulationProgressEvent`` object containing
the bash script for each GROMACS command that is called during the simulation.

The following information must be provided in the model interface:

- **Name**: A human readable name of the simulation.
- **Output Directory**: The local directory path that will be used to contain simulation output and input files
- **No. Molecule Types**: The number of different molecule types in the simulation cell
- **Size**: The total number of fragments in the simulation
- **No. Steps**: The length of the simulation in time steps
- **MARTINI Parameter**: A path to the GROMACS topology ``.itp`` file that contains the MARTINI forcefield
- **Minimization Parameter File**: File path to the GROMACS parameter ``.top`` file that contains the instructions for an
  energy minimization run
- **Production Parameter File**: File path to the GROMACS parameter ``.top`` file that contains the instructions for a
  production run
- **Overwrite Simulation Data?**: Whether or not to overwrite any existing simulation data files.
- **Dry Run?**: Whether or not to perform a dry run of the simulation.
- **MPI Run?**: Whether or not to perform an MPI run of the simulation using parallel processing
- **No. Processes**: Number of processes to use in an MPI run
- **Overwrite Data?**: Whether or not to overwrite any existing simulation data files.


Notification Listeners
----------------------

HPCWriter
~~~~~~~~~

The ``HPCWriter`` class reacts to a ``SimulationProgressEvent`` in order to output bash file that can
be used as a submission script to a HPC. The file contains the series of GROMACS commands that is communicated
by the ``SimulationProgressEvent`` as well as a customizable header and prefix. The output file name is determined
by the name of the simulation contained in the event's bash script.

The following information must be provided in the model interface:

- **Header**: The header of the output bash file containing HPC submission script details
- **Prefix**: An extended multi-line section of the output bash file containing any additioanl submission script
  details
- **Dry Run?**: Whether or not to perform a dry run of writing the file.