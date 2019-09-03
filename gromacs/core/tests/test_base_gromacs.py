from unittest import TestCase

from gromacs.core.base_gromacs_process import (
    BaseGromacsProcess
)


class TestBaseGromacsCommand(TestCase):

    def setUp(self):
        #: Create Gromacs command objects
        self.gromacs = BaseGromacsProcess(dry_run=True)

    def test___init__(self):
        self.assertTrue(self.gromacs.dry_run)
        self.assertEqual(0, self.gromacs._returncode)

    def test__not_implemented(self):

        with self.assertRaises(NotImplementedError):
            self.gromacs.bash_script()

        with self.assertRaises(NotImplementedError):
            self.gromacs.run()

    def test_recall(self):

        self.gromacs._stdout = b'output'
        self.gromacs._stderr = b'error'

        self.assertEqual(
            'output', self.gromacs.recall_stdout()
        )
        self.assertEqual(
            'error', self.gromacs.recall_stderr()
        )
