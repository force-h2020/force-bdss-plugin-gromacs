from unittest import TestCase

from traits.trait_errors import TraitError

from force_gromacs.core.base_gromacs_command import (
    BaseGromacsCommand
)


class TestBaseGromacsCommand(TestCase):

    def setUp(self):
        # Create Gromacs command objects
        self.gromacs_command = BaseGromacsCommand(
            name='gmx',
            flags=['-c', '-o', '-flag'],
            dry_run=True)

    def test___init__(self):
        self.assertEqual('gmx', self.gromacs_command.name)
        self.assertListEqual(
            ['-c', '-o', '-flag'], self.gromacs_command.flags
        )
        self.assertEqual(
            {'-c', '-o', '-flag'}, self.gromacs_command._flags)

        self.assertTrue(self.gromacs_command.dry_run)
        self.assertEqual('', self.gromacs_command.user_input)
        self.assertEqual({}, self.gromacs_command.command_options)

    def test__flags_readonly(self):

        with self.assertRaises(TraitError):
            self.gromacs_command._flags = []

    def test_check_command_options(self):

        self.gromacs_command.command_options = {
            '-c': 'coordinate',
            '-o': 'output',
            '-flag': True,
            '-a': 'not_allowed'
        }

        self.assertEqual(
            {'-c': 'coordinate',
             '-o': 'output',
             '-flag': True},
            self.gromacs_command.command_options
        )

    def test__build_process(self):

        command = 'echo Hello World'
        proc = self.gromacs_command._build_process(command)

        stdout, stderr = proc.communicate()
        returncode = proc.returncode

        self.assertEqual(0, returncode)
        self.assertEqual(b'Hello World\n', stdout)
        self.assertEqual(b'', stderr)

        self.gromacs_command.user_input = 'Hello World'
        command = 'uniq'

        proc = self.gromacs_command._build_process(command)

        stdout, stderr = proc.communicate()
        returncode = proc.returncode

        self.assertEqual(0, returncode)
        self.assertEqual(b'Hello World\n', stdout)
        self.assertEqual(b'', stderr)

    def test__build_command(self):

        command = self.gromacs_command._build_command()
        self.assertEqual('gmx', command)

        self.gromacs_command.command_options = {
            '-c': 'coordinate',
            '-o': 'output',
            '-flag': True,
        }
        command = self.gromacs_command._build_command()
        self.assertIn('gmx', command)
        self.assertIn(' -c coordinate', command)
        self.assertIn(' -o output', command)
        self.assertIn(' -flag', command)
        self.assertNotIn('True', command)

    def test_bash_script(self):

        bash_script = self.gromacs_command.bash_script()
        self.assertEqual('gmx', bash_script)

        self.gromacs_command.command_options = {
            '-c': 'coordinate',
            '-o': 'output',
            '-flag': True,
        }
        self.gromacs_command.user_input = 'ATOM'

        bash_script = self.gromacs_command.bash_script()
        self.assertIn("echo 'ATOM' |", bash_script)
        self.assertIn(' gmx', bash_script)
        self.assertIn(' -c coordinate', bash_script)
        self.assertIn(' -o output', bash_script)
        self.assertIn(' -flag', bash_script)

    def test_run(self):

        self.assertEqual(0, self.gromacs_command.run())
        self.assertEqual('', self.gromacs_command.recall_stdout())
        self.assertEqual('', self.gromacs_command.recall_stderr())
