import logging
import os

from traits.api import HasTraits, List, Unicode, provides

from force_gromacs.core.i_base_process import IBaseProcess

log = logging.getLogger(__name__)


@provides(IBaseProcess)
class GromacsFileTreeBuilder(HasTraits):
    """Class builds file trees for a Gromacs experiment"""

    # --------------------
    #  Required Attributes
    # --------------------

    #: Location to create file tree in. (By default, the
    #: current working directory)
    directory = Unicode()

    #: Folders to be created in the base directory
    folders = List(Unicode)

    # --------------------
    #   Private Methods
    # --------------------

    def _make_directory(self, directory):
        """Creates new directory if path does not already exists and
        `dry_run` attribute is set to `False`"""
        if os.path.exists(directory) or self.dry_run:
            pass
        else:
            os.mkdir(directory)

    def _create_directory_list(self):
        """Returns a list of strings representing the folder paths
        to be created in the file tree"""
        directory_list = [self.directory]

        for folder in self.folders:
            directory_list.append(
                '/'.join([self.directory, folder])
            )

        return directory_list

    # --------------------
    #    Public Methods
    # --------------------

    def recall_stderr(self):
        """Returns dummy stderr message"""
        return ''

    def recall_stdout(self):
        """Returns dummy stdout message"""
        return ''

    def bash_script(self):
        """Creates a bash script to build the file tree"""

        directory_list = self._create_directory_list()

        bash_script = '\n'.join([
            f'mkdir {directory}' for directory in directory_list
        ])

        return bash_script

    def run(self):
        """Builds the file tree locally"""

        directory_list = self._create_directory_list()

        for directory in directory_list:
            self._make_directory(directory)

        # Provide successful return code
        return 0
