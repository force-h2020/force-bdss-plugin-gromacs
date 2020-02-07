import os

from force_bdss.api import (
    BaseDataSource, DataValue, Slot, Instance
)

from force_gromacs.simulation_builders.i_simulation_builder import (
    ISimulationBuilder)


class SimulationDataSource(BaseDataSource):
    """Class that generates and calls a bash script for a single
    Gromacs simulation. Contains the option to perform the simulation
    locally, or export the bash script in order to run on a remote
    cluster."""

    simulation_builder = Instance(ISimulationBuilder)

    def _check_perform_simulation(self, model, results_path):
        """Check to see whether a simulation should be performed.
        If a results file already exists, then only perform a new
        simulation if required by the model"""

        if os.path.exists(results_path):
            return model.ow_data
        return True

    def create_bash_script(self, pipeline, name=None):
        """Creates a string that can be exported as a bash script
        to run a Gromacs simulation simulation

        Parameters
        ----------
        pipeline: GromacsPipeline
            A `GromacsPipeline` instance that can generate a bash
            script to run a series of `BaseGromacsCommands`
        name: str, optional
            A simulation-specific name to include in the header
            of each bash script for reference purposes

        Returns
        -------
        bash_script: str
            String that can be exported as a bash file to call a
            series of command line functions
        """

        bash_script = ""

        if name is not None:
            # Add the simulation name to the top of the script
            bash_script = f"# {name}\n"

        # Generate reference bash script
        bash_script += pipeline.bash_script()

        return bash_script

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
        raise NotImplementedError(
            "Class needs to implement create_simulation_builder`"
            "method that returns a BaseGromacsSimulationBuilder instance"
        )

    def run(self, model, parameters):
        """Takes in all parameters and molecules required to
        perform a Gromacs simulation"""

        # Generate a `BaseGromacsSimulationBuilder` object that will
        # pre-process all user input and produce a `GromacsPipeline`
        # object in order to run a simulation locally or export a bash
        # script for submission to a cluster
        self.simulation_builder = self.create_simulation_builder(
            model, parameters
        )

        # Output the path containing the results trajectory file
        results_path = self.simulation_builder.get_results_path()

        if self._check_perform_simulation(model, results_path):

            # Create a `GromacsPipeline` with all commands needed to run the
            # simulation simulation
            pipeline = self.simulation_builder.build_pipeline()

            # Create bash script of Gromacs commands for remote submission
            bash_script = self.create_bash_script(
                pipeline, name=self.simulation_builder.name
            )

            # Export the bash script to any HPCWriterNotificationListener
            model.notify_bash_script(bash_script)

            # Run simulation locally
            pipeline.run()

        return [
            DataValue(type="TRAJECTORY", value=results_path)
        ]

    def slots(self, model):

        input_slots = tuple(
                Slot(description=f"Molecule {index + 1} data",
                     type="MOLECULE")
                for index in range(model.n_molecule_types)
            )

        output_slots = (
            Slot(description="Gromacs trajectory path",
                 type="TRAJECTORY"),
        )

        return (
            input_slots,
            output_slots
        )
