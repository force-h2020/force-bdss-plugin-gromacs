#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import os
from unittest import TestCase

from force_gromacs.tests.probe_classes.pipelines import (
    ProbeGromacsPipeline
)


class TestGromacsPipeline(TestCase):

    def setUp(self):

        self.pipeline = ProbeGromacsPipeline()

    def test_pipeline_bash_script(self):

        commands = self.pipeline.bash_script().split('\n')

        self.assertEqual(
            'mkdir test_experiment', commands[0]
        )
        self.assertEqual(
            'mkdir ' + os.path.join('test_experiment', '1_build'),
            commands[1]
        )
        self.assertEqual(
            'mkdir ' + os.path.join('test_experiment', '2_minimize'),
            commands[2]
        )
        self.assertEqual(
            'mkdir ' + os.path.join('test_experiment', '3_production'),
            commands[3]
        )

        self.assertIn('solvate', commands[4])
        self.assertIn(' -cp test_coord.gro', commands[4])
        self.assertIn(' -o test_output.gro', commands[4])
        self.assertIn(' -radius 30', commands[4])

        self.assertIn('genion', commands[5])
        self.assertIn(' -s test_top.trp', commands[5])
        self.assertIn(' -p test_top.top', commands[5])
        self.assertIn(' -o test_output.gro', commands[5])
        self.assertIn(' -np 64', commands[5])
        self.assertIn(' -pname test_coord_2.gro', commands[5])
        self.assertIn(' -pq 1', commands[5])

        self.assertIn(
            'cat <<EOM > ' + os.path.join(
                os.path.curdir, 'test_experiment', 'test_topology.top'),
            commands[6])
        self.assertIn('#include "test_top.itp', commands[7])
        self.assertIn('[ system ]', commands[9])
        self.assertIn('test_experiment', commands[10])
        self.assertIn('[ molecules ]', commands[12])
        self.assertIn('S 30', commands[13])
        self.assertIn('EOM', commands[14])

    def test_pipeline_run(self):

        self.pipeline.run()
        names = ['file_tree', 'solvate', 'genion', 'top_file']
        output = self.pipeline.run_output

        for name in names:
            self.assertEqual(0, output[name]['returncode'])
            self.assertEqual('', output[name]['stdout'])
            self.assertEqual('', output[name]['stderr'])
