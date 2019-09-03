import logging
import os

from traits.api import List, Unicode

from gromacs.core.base_gromacs_process import BaseGromacsProcess

log = logging.getLogger(__name__)


class GromacsFileTreeBuilder(BaseGromacsProcess):
    """  Class builds file trees for a Gromacs experiment"""

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

        if os.path.exists(directory) or self.dry_run:
            pass
        else:
            os.mkdir(directory)

    def _create_directories(self):

        directory_list = [self.directory]

        for folder in self.folders:
            directory_list.append(
                '/'.join([self.directory, folder])
            )

        return directory_list

    # --------------------
    #    Public Methods
    # --------------------

    def bash_script(self):
        """Creates a bash script to build the file tree"""

        directory_list = self._create_directories()

        bash_script = '\n'.join([
            f'mkdir {directory}' for directory in directory_list
        ])

        return bash_script

    def run(self):
        """Builds the file tree locally"""

        directory_list = self._create_directories()

        for directory in directory_list:
            self._make_directory(directory)

        return self._returncode
