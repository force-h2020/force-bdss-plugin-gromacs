from unittest import TestCase

from traits.api import TraitError

from force_gromacs.commands.gromacs_commands import (
    Gromacs_genbox, Gromacs_genion
)
from force_gromacs.commands.gromacs_file_tree_builder import (
    GromacsFileTreeBuilder
)
from force_gromacs.io.gromacs_topology_writer import (
    GromacsTopologyWriter
)
from force_gromacs.tests.dummy_classes import (
    DummyCommand, DummyCommand_2, DummyCommand_3
)
from force_gromacs.tests.probe_classes import (
    ProbeGromacsPipeline
)


class TestGromacsPipeline(TestCase):

    def setUp(self):

        self.pipeline = ProbeGromacsPipeline()

    def test_pipeline_getitem(self):

        self.assertEqual(type(self.pipeline[0]), GromacsFileTreeBuilder)
        self.assertEqual(type(self.pipeline[1]), Gromacs_genbox)
        self.assertEqual(type(self.pipeline[2]), Gromacs_genion)
        self.assertEqual(type(self.pipeline[3]), GromacsTopologyWriter)

        self.assertEqual(4, len(self.pipeline))

        keys = [name for name, _ in self.pipeline.steps]

        self.assertListEqual(
            ['file_tree', 'genbox', 'genion', 'top_file'], keys
        )

        for name, command in self.pipeline.steps:
            self.assertEqual(self.pipeline.dry_run, command.dry_run)

    def test_named_steps(self):

        self.assertIsInstance(self.pipeline.named_steps, dict)
        self.assertEqual(
            ['file_tree', 'genbox', 'genion', 'top_file'],
            list(self.pipeline.named_steps.keys())
        )

        new_command = Gromacs_genbox(dry_run=True)
        self.pipeline.append(('new_command', new_command))
        self.assertEqual(
            ['file_tree', 'genbox', 'genion', 'top_file',
             'new_command'],
            list(self.pipeline.named_steps.keys())
        )

    def test___getitem__(self):

        # Allow indexing by name
        self.assertEqual(
            self.pipeline[0], self.pipeline['file_tree']
        )

        # Do not allow slicing
        with self.assertRaisesRegex(
                ValueError,
                'Pipeline does not support slicing'):
            self.pipeline[slice(0, 1, 1)]

    def test_update_dry_run(self):

        self.pipeline.dry_run = False
        for command in self.pipeline:
            self.assertFalse(command.dry_run)

        new_command = Gromacs_genbox(dry_run=True)
        self.pipeline.append(('new_command', new_command))
        self.assertFalse(self.pipeline[-1].dry_run)

    def test_append(self):

        self.pipeline.append(('test_append', Gromacs_genbox()))

        self.assertEqual(5, len(self.pipeline))

        keys = [name for name, _ in self.pipeline.steps]

        self.assertListEqual(
            ['file_tree', 'genbox', 'genion', 'top_file',
             'test_append'],
            keys
        )

    def test__validate_steps(self):

        dummy_command = DummyCommand()

        with self.assertRaises(TraitError):
            self.pipeline.append(
                ('not_a_command', dummy_command)
            )
        self.assertEqual(4, len(self.pipeline))

        dummy_command.run = True
        dummy_command.bash_script = True
        dummy_command.dry_run = True

        with self.assertRaises(TraitError):
            self.pipeline.append(
                ('not_a_command', dummy_command)
            )
        self.assertEqual(4, len(self.pipeline))

        dummy_command = DummyCommand_2()

        with self.assertRaises(TraitError):
            self.pipeline.append(
                ('not_a_command', dummy_command)
            )
        self.assertEqual(4, len(self.pipeline))

        dummy_command = DummyCommand_3()

        with self.assertRaises(TraitError):
            self.pipeline.append(
                ('not_a_command', dummy_command)
            )
        self.assertEqual(4, len(self.pipeline))

    def test_pipeline_build_command(self):

        commands = self.pipeline.bash_script().split('\n')

        self.assertEqual(
            'mkdir ./test_experiment', commands[0]
        )
        self.assertEqual(
            'mkdir ./test_experiment/1_build', commands[1]
        )
        self.assertEqual(
            'mkdir ./test_experiment/2_minimize', commands[2]
        )
        self.assertEqual(
            'mkdir ./test_experiment/3_production', commands[3]
        )

        self.assertIn('genbox', commands[4])
        self.assertIn(' -cp test_coord.gro', commands[4])
        self.assertIn(' -o test_output.gro', commands[4])
        self.assertIn(' -try', commands[4])
        self.assertIn(' -nmol 30', commands[4])

        self.assertIn('genion', commands[5])
        self.assertIn(' -s test_top.trp', commands[5])
        self.assertIn(' -p test_top.top', commands[5])
        self.assertIn(' -o test_output.gro', commands[5])
        self.assertIn(' -np 64', commands[5])
        self.assertIn(' -pname test_coord_2.gro', commands[5])
        self.assertIn(' -pq 1', commands[5])

        self.assertIn('cat <<EOM > ./test_experiment/test_topology.top',
                      commands[6])
        self.assertIn('#include "test_top.itp', commands[7])
        self.assertIn('[ system ]', commands[9])
        self.assertIn('test_experiment', commands[10])
        self.assertIn('[ molecules ]', commands[12])
        self.assertIn('S 30', commands[13])
        self.assertIn('EOM', commands[14])

    def test_pipeline_run(self):

        self.pipeline.run()

        output = self.pipeline.run_output

        self.assertEqual(0, output['file_tree']['returncode'])
        self.assertEqual(0, output['genbox']['returncode'])
        self.assertEqual(0, output['genion']['returncode'])
        self.assertEqual(0, output['top_file']['returncode'])

        self.assertEqual('', output['file_tree']['stdout'])
        self.assertEqual('', output['genbox']['stdout'])
        self.assertEqual('', output['genion']['stdout'])
        self.assertEqual('', output['top_file']['stdout'])

        self.assertEqual('', output['file_tree']['stderr'])
        self.assertEqual('', output['genbox']['stderr'])
        self.assertEqual('', output['genion']['stderr'])
        self.assertEqual('', output['top_file']['stderr'])
