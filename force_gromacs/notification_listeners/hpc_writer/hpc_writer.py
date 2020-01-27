from traits.api import Instance

from force_bdss.api import (
    BaseNotificationListener,
)

from force_gromacs.notification_listeners.driver_events import (
    SimulationProgressEvent
)

from .hpc_writer_model import HPCWriterModel


class HPCWriter(BaseNotificationListener):
    """Class that outputs a bash script that can be submitted to a
    HPC queue in order to run Gromacs simulation on a remote cluster"""

    #: A reference to the HPCWriterModel object created during the
    #: force-bdss MCODriver loop. Used to pass messages to the MCO.
    model = Instance(HPCWriterModel)

    # --------------------
    #   Private Methods
    # --------------------

    def _write_hpc_script(self, file_path, hpc_script):
        """Writes HPC script to a bash file located at
        `file_path`"""

        if not self.model.dry_run:
            with open(file_path, 'w') as outfile:
                outfile.write(hpc_script)

    def _extract_simulation_name(self, bash_script):
        """If bash_script contains simulation name, extract and
        return it, otherwise create a unique id"""

        lines = bash_script.split('\n')

        for line in lines:
            if line.isspace():
                continue

            if line.startswith('#'):
                name = line.strip('# ')
                return name
            else:
                break

        name = f"gromacs-sim-{str(id(line))}"

        return name

    # --------------------
    #    Public Methods
    # --------------------

    def create_file_path(self, simulation_name):
        """Create a unique file path to write the a bash script"""

        file_path = '_'.join([self.model.prefix, simulation_name]) + '.sh'

        return file_path

    def create_hpc_script(self, bash_script):
        """Combines UI header for HPC cluster with Gromacs
        script"""

        hpc_script = "#!/bin/sh\n"
        hpc_script += self.model.header
        hpc_script += f"\n\n{bash_script}"

        return hpc_script

    def initialize(self, model):
        self.model = model

    def deliver(self, event):

        if isinstance(event, SimulationProgressEvent):

            bash_script = event.bash_script

            simulation_name = self._extract_simulation_name(bash_script)
            file_path = self.create_file_path(simulation_name)
            hpc_script = self.create_hpc_script(bash_script)

            self._write_hpc_script(file_path, hpc_script)

            return hpc_script
