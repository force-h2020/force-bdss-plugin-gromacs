#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import subprocess
import os

from traits.api import (
    Unicode,
    Enum,
    Set,
    Dict,
    List,
    Property,
    on_trait_change
)

from force_gromacs.core.base_process import BaseProcess


class BaseGromacsCommand(BaseProcess):
    """Base class for Gromacs commands. Requires the command `name` to be
    defined on initiation, and takes in a list of accepted command line
    `flags`.

    For each call, a dictionary containing command line flags
    and their corresponding objects as key : item pairs needs to be
    previously assigned as the `command_option` attribute. If arguments
    need to be piped in during the run, the `user_input` attribute can
    be assigned as a string containing the information required.

    Upon calling the `run` method, the full command is generated and
    called locally using the `subprocess` library. A bash script to perform
    the equivalent operation can be returned using the `bash_script`
    method."""

    # --------------------
    #  Required Attributes
    # --------------------

    #: Name of Gromacs executable
    executable = Enum('gmx', '')

    #: Name of Gromacs task
    name = Unicode(allow_none=False)

    #: List of accepted flags for command line options
    flags = List()

    # --------------------
    #  Regular Attributes
    # --------------------

    #: A dictionary with the form (key=flag, item=argument) for
    #: determining each command line option that will be generated
    command_options = Dict()

    #: Optional additional input to be piped into the Gromacs
    #: command
    user_input = Unicode()

    # ------------------
    #     Properties
    # ------------------

    #: Set of accepted flags for command line options
    _flags = Property(Set, depends_on='flags')

    # ------------------
    #     Listeners
    # ------------------

    def _get__flags(self):
        """Private attribute `_flags` contains unique set of command
        line options that is readonly."""
        return set(self.flags + ['-h'])

    @on_trait_change('command_options')
    def check_command_options(self):
        """Check that new Gromacs command contains allowed flags"""
        checked_command_options = {}
        for key, value in self.command_options.items():
            if key in self._flags:
                checked_command_options[key] = value

        self.command_options = checked_command_options

    # ------------------
    #  Private Methods
    # ------------------

    def _build_process(self, command):
        """Creates process to run Gromacs command on. Also sets up piping
        in of any arguments in `user_input` if required."""

        if self.user_input != '':

            input_proc = subprocess.Popen(
                ['echo'] + self.user_input.split(),
                stdout=subprocess.PIPE
            )

            process = subprocess.Popen(
                command.split(),
                env=os.environ,
                stdin=input_proc.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            input_proc.stdout.close()
            input_proc.poll()

        else:
            process = subprocess.Popen(
                command.split(),
                env=os.environ,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

        return process

    def _build_command(self):
        """Generate terminal command from input data"""

        command = ' '.join([self.executable, self.name]).strip()

        for flag, arg in self.command_options.items():
            if arg is None:
                pass
            elif type(arg) == bool:
                command += ' {}'.format(flag)
            else:
                command += ' {} {}'.format(flag, arg)

        return command

    # ------------------
    #   Public Methods
    # ------------------

    def bash_script(self):
        """Output terminal command as a bash script"""

        command = self._build_command()

        if self.user_input != '':
            script = f"echo '{self.user_input}' | {command}"
        else:
            script = command

        return script

    def run(self):
        """Run command on terminal using subprocess

        Raises
        ------
        RuntimeError
            if Gromacs did not run correctly

        Returns
        -------
        returncode: int
            Return code from subprocess running Gromacs command
        """

        command = self._build_command()

        if self.dry_run:
            self._stdout, self._stderr, self._returncode = (
                b'', b'', 0
            )

        else:
            try:
                proc = self._build_process(command)
            except FileNotFoundError:
                raise RuntimeError(
                    f"Gromacs executable '{self.name}' was "
                    "not found. Check Gromacs installation")

            self._stdout, self._stderr = proc.communicate()
            self._returncode = proc.returncode

            if self._returncode != 0:

                msg = (
                    f"Gromacs command '{command}' did not run correctly. "
                    f"Error code: {self._returncode}")

                if self._stderr:
                    msg += (
                        f", '{self._stderr.decode('unicode_escape').strip()}'")

                raise RuntimeError(msg)

        return self._returncode
