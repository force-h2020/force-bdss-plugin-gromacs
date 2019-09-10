from force_bdss.api import (
    BaseDataSource, DataValue, Slot
)

from force_gromacs.notification_listeners.driver_events import (
    SimulationProgressEvent
)


class SimulationDataSource(BaseDataSource):
    """Class that generates and calls a bash script for a single
    Gromacs simulation. Contains the option to perform the simulation
    locally, or export the bash script in order to run on a remote
    cluster."""

    def notify_bash_script(self, model, bash_script):
        """Notify the construction of a bash script for a Gromacs
        simulation. Assigns an `ExperimentProgressEvent` to the
        `progress_event` attribute on associated
        `SimulationDataSourceModel`. By doing so it can be picked
        up by the `UnileverMCO` and passed onto any
        `NotificationListeners` present.

        Parameters
        ----------
        model: SimulationDataSourceModel
            The BaseDataSourceModel associated with this class
        bash_script: str
            A string containing the constructed
            bash script to run a Gromacs simulation.
        """

        model.driver_event = SimulationProgressEvent(
            bash_script=DataValue(
                type="SCRIPT", value=bash_script
            )
        )

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
        of generating a `GromacsPipeline`"""
        raise NotImplementedError(
            "Class needs to implement create_simulation_builder`"
            "method that returns a GromacsSimulationBuilder instance"
        )

    def run(self, model, parameters):
        """Takes in all parameters and molecules required to
        perform a Gromacs simulation"""

        # Generate a `GromacsSimulationBuilder` object that will pre-process
        # all user input and produce a `GromacsPipeline` object in order
        # to run a simulation locally or export a bash script for submission
        # to a cluster
        simulation_builder = self.create_simulation_builder(
            model, parameters
        )

        # Create a `GromacsPipeline` with all commands needed to run the
        # simulation simulation
        pipeline = simulation_builder.build_pipeline()

        # Create bash script of Gromacs commands for remote submission
        bash_script = self.create_bash_script(
            pipeline, name=simulation_builder.name
        )

        # Export the bash script to any HPCWriterNotificationListener
        self.notify_bash_script(model, bash_script)

        # Run simulation locally
        pipeline.run()

        return []

    def slots(self, model):

        input_slots = tuple(
                Slot(description=f"Molecule {index + 1} data",
                     type="MOLECULE")
                for index in range(model.n_molecule_types)
            )

        return (
            input_slots,
            (
            ),
        )
