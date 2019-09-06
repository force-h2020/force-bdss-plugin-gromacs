from traits.api import Unicode, File

from force_bdss.api import BaseDataSourceModel
from force_bdss.core.verifier import VerifierError


class FragmentDataSourceModel(BaseDataSourceModel):
    """Class containing all input parameters for a single molecular
    fragment in a Gromacs simulation"""

    # --------------------
    #  Required Attributes
    # --------------------

    #: Name of the fragment
    name = Unicode(
        desc='Name of fragment')

    #: Reference symbol of fragment in Gromacs files
    symbol = Unicode(
        desc='Reference symbol in input Gromacs topology file')

    #: Location of Gromacs topology file containing molecular data
    topology = File(
        desc='File path for Gromacs topology file',
        verify=True
    )

    #: Location of Gromacs coordinate file containing molecular data
    coordinate = File(
        desc='File path for Gromacs coordinate file',
        verify=True
    )

    # --------------------
    #    Private Methods
    # --------------------

    def _file_check(self, file_path, ext=None):
        """Performs a series of checks on selected Gromacs file located
        at file_path

        Parameters
        ----------
        file_path: str
            File path for Gromacs input file
        ext: str, optional
            Expected extension of Gromacs input file
        """
        errors = []
        if file_path.isspace():
            errors.append(
                VerifierError(
                    subject=self,
                    local_error="Gromacs file name is white space.",
                    global_error=(
                        "Gromacs file not specified."
                    ),
                )
            )

        if ext is not None:
            if not file_path.endswith('.{}'.format(ext)):
                errors.append(
                    VerifierError(
                        subject=self,
                        local_error="File extension does not match required.",
                        global_error=(
                            "File is not a valid Gromacs file type."
                        ),
                    )
                )

        try:
            with open(file_path, 'r'):
                pass
        except IOError:
            errors.append(
                VerifierError(
                    subject=self,
                    local_error="Opening file returns IOError.",
                    global_error=(
                        "Unable to open Gromacs file."
                    ),
                )
            )

        return errors

    # --------------------
    #    Public Methods
    # --------------------

    def verify(self):
        """Overloads BaseDataSourceModel verify method to check file names
        status upon activation of verify_workflow_event."""

        errors = super(FragmentDataSourceModel, self).verify()
        errors += self._file_check(self.topology, 'itp')
        errors += self._file_check(self.coordinate, 'gro')

        return errors
