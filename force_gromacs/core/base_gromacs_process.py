from traits.api import HasTraits, Bool, Int, Bytes


class BaseGromacsProcess(HasTraits):
    """Base class for objects that can generate and call Gromacs
    commands, typically via the subprocess library. Attributes
    and methods to be implemented provide standard functionalities
    for using subprocess."""

    #: Whether or not to perform a 'dry run' i.e. build the Gromacs
    #: command but do not call subprocess to run it
    dry_run = Bool(True)

    #: Return code from subprocess command
    _returncode = Int(0)

    #: Stderr from subprocess command
    _stderr = Bytes()

    #: Stdout from subprocess command
    _stdout = Bytes()

    def recall_stderr(self):
        """Returns latest stderr message as Unicode"""
        return self._stderr.decode('unicode_escape')

    def recall_stdout(self):
        """Returns latest stdout message as Unicode"""
        return self._stdout.decode('unicode_escape')

    def bash_script(self):
        raise NotImplementedError(
            'Subclass does not contain an implementation of'
            '`bash_script` method'
        )

    def run(self):
        raise NotImplementedError(
            'Subclass does not contain an implementation of'
            '`run` method'
        )
