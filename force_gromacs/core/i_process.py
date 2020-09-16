#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from traits.api import Interface, Bool


class IProcess(Interface):
    """Interface for objects that can generate and call
    command line executables, typically via the subprocess library.
    Attributes and methods to be implemented provide standard
    functionalities for using subprocess.

    Any class that provides this interface is able to be chained
    together in a BasePipeline
    """

    #: Whether or not to perform a 'dry run' i.e. build the
    #: command but do not call subprocess to run it
    dry_run = Bool()

    def recall_stderr(self):
        """Returns latest stderr message as Unicode"""

    def recall_stdout(self):
        """Returns latest stdout message as Unicode"""

    def bash_script(self):
        """Method to be implemented that returns a string containing
        the equivalent bash command to invoke the `run` method directly
        from the command line."""

    def run(self):
        """Method to be implemented that will either call a command line
        executable using the subprocess library or perform the equivalent
        operation during runtime."""
