#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import HasStrictTraits, Bool, Int, Bytes, provides

from .i_process import IProcess


@provides(IProcess)
class BaseProcess(HasStrictTraits):
    """Base class for objects that can generate and call
    command line executables via the subprocess library.
    Attributes and methods to be implemented provide standard
    functionalities for using subprocess."""

    #: Whether or not to perform a 'dry run' i.e. build the bash
    #: command but do not call subprocess to run it
    dry_run = Bool(True)

    #: Return code from subprocess command
    _returncode = Int(0)

    #: Stderr from subprocess command
    _stderr = Bytes()

    #: Stdout from subprocess command
    _stdout = Bytes()

    def recall_stderr(self):
        """Returns latest stderr message as unicode"""
        return self._stderr.decode('unicode_escape')

    def recall_stdout(self):
        """Returns latest stdout message as unicode"""
        return self._stdout.decode('unicode_escape')

    def bash_script(self):
        """Method to be implemented that returns a string containing
        the equivalent bash command to invoke the `run` method directly
        from the command line."""
        raise NotImplementedError(
            'Subclass does not contain an implementation of '
            '`bash_script` method'
        )

    def run(self):
        """Method to be implemented that will either call a
        command using the subprocess library or perform the equivalent
        operation during runtime."""
        raise NotImplementedError(
            'Subclass does not contain an implementation of '
            '`run` method'
        )
