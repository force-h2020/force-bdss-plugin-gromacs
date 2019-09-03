from unittest import TestCase

from traits.testing.unittest_tools import UnittestTools

from force_bdss.api import DataValue

from force_gromacs.gromacs_plugin import GromacsPlugin
from force_gromacs.notification_listeners.driver_events import (
    SimulationProgressEvent
)


class TestHPCWriterNotificationListener(TestCase, UnittestTools):

    def setUp(self):
        self.plugin = GromacsPlugin()
        self.factory = self.plugin.notification_listener_factories[0]
        self.notification_listener = self.factory.create_listener()

        self.script = ('# experiment_5.0\n'
                       'mdrun -s test_topol.tpr\n')
        self.hpc_script = ('#!/bin/sh\n# Example HPC header\n\n'
                           '# experiment_5.0\n'
                           'mdrun -s test_topol.tpr\n')

        self.model = self.factory.create_model()
        self.model.header = '# Example HPC header'

        self.notification_listener.initialize(self.model)

    def test_initialization(self):

        self.assertEqual(
            self.model, self.notification_listener.model
        )

    def test_create_hpc_script(self):

        res = self.notification_listener.create_hpc_script(
            self.script
        )
        self.assertEqual(self.hpc_script, res)

    def test_write_hpc_script(self):

        file_path = self.notification_listener.write_hpc_script(
            self.hpc_script, 'test_experiment'
        )
        self.assertEqual(
            'hpc_sub_script_test_experiment.sh', file_path
        )

    def test_progress_event_handling(self):

        event = SimulationProgressEvent(
            bash_script=DataValue(
                type='SCRIPT', value=self.script
            )
        )

        self.assertEqual(
            self.hpc_script,
            self.notification_listener.deliver(event)
        )
