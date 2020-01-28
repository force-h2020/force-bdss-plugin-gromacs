from unittest import TestCase

from force_gromacs.core.base_process import (
    BaseProcess
)


class TestBaseProcess(TestCase):

    def setUp(self):
        #: Create Gromacs command objects
        self.process = BaseProcess()

    def test___init__(self):
        self.assertTrue(self.process.dry_run)
        self.assertEqual(0, self.process._returncode)

    def test__not_implemented(self):

        with self.assertRaises(NotImplementedError):
            self.process.bash_script()

        with self.assertRaises(NotImplementedError):
            self.process.run()

    def test_recall(self):

        self.process._stdout = b'output'
        self.process._stderr = b'error'

        self.assertEqual(
            'output', self.process.recall_stdout()
        )
        self.assertEqual(
            'error', self.process.recall_stderr()
        )
