#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase, mock

from traits.testing.unittest_tools import UnittestTools

from force_gromacs.gromacs_plugin import GromacsPlugin
from force_gromacs.notification_listeners.driver_events import (
    SimulationProgressEvent
)

HPC_WRITER_OPEN_PATH = (
    "force_gromacs.notification_listeners.hpc_writer.hpc_writer.open"
)


class TestHPCWriter(TestCase, UnittestTools):

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

    def test__extract_simulation_name(self):

        name = self.notification_listener._extract_simulation_name(
            self.script
        )
        self.assertEqual('experiment_5.0', name)

        name = self.notification_listener._extract_simulation_name(
            'mdrun -s test_topol.tpr\n'
        )
        self.assertIn('gromacs-sim-', name)

        name = self.notification_listener._extract_simulation_name(
            '\n\nmdrun -s test_topol.tpr\n'
        )
        self.assertIn('gromacs-sim-', name)

    def test_create_file_path(self):

        file_path = self.notification_listener.create_file_path(
            'experiment_5.0'
        )
        self.assertEqual('hpc_sub_script_experiment_5.0.sh', file_path)

    def test_create_hpc_script(self):

        res = self.notification_listener.create_hpc_script(
            self.script
        )
        self.assertEqual(self.hpc_script, res)

    def test__write_hpc_script(self):
        mock_open = mock.mock_open()

        with mock.patch(HPC_WRITER_OPEN_PATH, mock_open, create=True):
            self.notification_listener._write_hpc_script(
                'some_path', self.hpc_script
            )
            mock_open.assert_not_called()

        self.model.dry_run = False
        with mock.patch(HPC_WRITER_OPEN_PATH, mock_open, create=True):
            self.notification_listener._write_hpc_script(
                'some_path', self.hpc_script
            )
            mock_open.assert_called_once()

    def test_progress_event_handling(self):

        event = SimulationProgressEvent(
            bash_script=self.script
        )

        self.assertEqual(
            self.hpc_script,
            self.notification_listener.deliver(event)
        )
        self.assertEqual(
            {
                'id': 'force_gromacs.notification_listeners'
                      '.driver_events.SimulationProgressEvent',
                'model_data': {
                    'bash_script':
                        '# experiment_5.0\nmdrun -s test_topol.tpr\n'
                }
            },
            event.__getstate__()
        )
