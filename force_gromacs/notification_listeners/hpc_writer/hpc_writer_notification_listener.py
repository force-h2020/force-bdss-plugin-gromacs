from traits.api import Instance

from force_bdss.api import (
    BaseNotificationListener,
)

from force_gromacs.notification_listeners.driver_events import (
    SimulationProgressEvent
)

from .hpc_writer_model import HPCWriterModel


class HPCWriterNotificationListener(BaseNotificationListener):
    """Class that outputs a bash script that can be submitted to a
    HPC queue in order to run Gromacs simulation on a remote cluster"""

    model = Instance(HPCWriterModel)

    def _insert_string(self, string, unit, index):

        return string[:index] + unit + string[index:]

    def create_hpc_script(self, bash_script):
        """Combines UI header for HPC cluster with Gromacs
        script"""

        return '#!/bin/sh\n' + self.model.header + '\n\n' + bash_script

    def write_hpc_script(self, hpc_script, experiment_name):
        """Outputs HPC script as file 'path'"""

        file_path = '_'.join([self.model.path, experiment_name]) + '.sh'

        if not self.model.dry_run:
            with open(file_path, 'w') as outfile:
                outfile.write(hpc_script)

        return file_path

    def initialize(self, model):

        self.model = model

    def deliver(self, event):

        if isinstance(event, SimulationProgressEvent):

            bash_script = event.bash_script.value

            experiment_name = bash_script.split('\n')[0]
            experiment_name = experiment_name.strip('# ')

            hpc_script = self.create_hpc_script(bash_script)

            self.write_hpc_script(
                hpc_script, experiment_name
            )

            return hpc_script
