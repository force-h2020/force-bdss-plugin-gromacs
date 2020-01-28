from unittest import TestCase

from force_gromacs.tests.probe_classes.pipelines import (
    ProbeProcess, ProbePipeline
)


class TestPipeline(TestCase):

    def setUp(self):

        self.pipeline = ProbePipeline()
        self.step_names = ['first', 'second', 'third', 'fourth']

    def test__len__(self):
        self.assertEqual(4, len(self.pipeline))

        new_command = ProbeProcess(dry_run=True)
        self.pipeline.steps.append(('new_command', new_command))

        self.assertEqual(5, len(self.pipeline))

        self.pipeline.steps.pop(0)

        self.assertEqual(4, len(self.pipeline))

    def test_steps(self):

        self.assertEqual(4, len(self.pipeline.steps))
        for index in range(4):
            self.assertIsInstance(self.pipeline[index], ProbeProcess)

        self.assertListEqual(
            self.step_names,
            [name for name, _ in self.pipeline.steps]
        )

        for name, command in self.pipeline.steps:
            self.assertEqual(self.pipeline.dry_run, command.dry_run)

    def test_named_steps(self):

        self.assertEqual(4, len(self.pipeline.named_steps))
        self.assertIn('first', self.pipeline.named_steps)
        self.assertIn('second', self.pipeline.named_steps)
        self.assertIn('third', self.pipeline.named_steps)
        self.assertIn('fourth', self.pipeline.named_steps)

        self.assertIsInstance(
            self.pipeline.named_steps['first'], ProbeProcess
        )
        self.assertIsInstance(
            self.pipeline.named_steps['second'], ProbeProcess
        )
        self.assertIsInstance(
            self.pipeline.named_steps['third'], ProbeProcess
        )
        self.assertIsInstance(
            self.pipeline.named_steps['fourth'], ProbeProcess
        )

        new_command = ProbeProcess(dry_run=True)
        self.pipeline.append(('new_command', new_command))
        self.assertIn('new_command', self.pipeline.named_steps)

        self.assertIsInstance(
            self.pipeline.named_steps['new_command'], ProbeProcess
        )

    def test___getitem__(self):

        # Allow indexing by name, both should point to same object
        for index, name in enumerate(self.step_names):
            self.assertIs(self.pipeline[index], self.pipeline[name])

        # Do not allow slicing
        with self.assertRaisesRegex(
                ValueError,
                'Pipeline does not support slicing'):
            self.pipeline[slice(0, 1, 1)]

    def test___iter__(self):

        for index, (name, process) in enumerate(self.pipeline):
            self.assertEqual(self.pipeline[index], process)
            self.assertEqual(self.step_names[index], name)

    def test_update_dry_run(self):

        self.pipeline.dry_run = False
        for _, command in self.pipeline:
            self.assertFalse(command.dry_run)

        new_command = ProbeProcess(dry_run=True)
        self.pipeline.append(('new_command', new_command))
        self.assertFalse(self.pipeline[-1].dry_run)

    def test_append(self):

        self.pipeline.append(('test_append', ProbeProcess()))

        self.assertEqual(5, len(self.pipeline))
        self.assertListEqual(
            self.step_names + ['test_append'],
            [name for name, _ in self.pipeline.steps]
        )
