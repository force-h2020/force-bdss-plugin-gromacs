from traits.api import HasTraits, ReadOnly


class BaseFileReader(HasTraits):
    """Class parses Gromacs input files and returns data
    required for each molecular type listed.
    """

    # --------------------
    # Protected Attributes
    # --------------------

    #: Extension of accepted file types
    _ext = ReadOnly()

    # ------------------
    #     Defaults
    # ------------------

    def __ext_default(self):
        """Default extension for this reader subclass"""
        raise NotImplementedError

    # ------------------
    #  Private Methods
    # ------------------

    def _check_file_types(self, file_path):
        """Raise exception if specified Gromacs file does not have
        expected format"""

        space_check = file_path.isspace()
        ext_check = not file_path.endswith(f'.{self._ext}')

        if space_check or ext_check:
            raise IOError(
                '{} not a valid Gromacs file type'.format(
                    file_path))

    def _read_file(self, file_path):
        """Simple file loader"""

        self._check_file_types(file_path)

        with open(file_path, 'r') as infile:
            file_lines = infile.readlines()

        return file_lines

    def _get_data(self, file_lines):
        """Process data from a parsed Gromacs file"""
        raise NotImplementedError

    # ------------------
    #   Public Methods
    # ------------------

    def read(self, file_path):
        """Read file and return processed data"""
        raise NotImplementedError
