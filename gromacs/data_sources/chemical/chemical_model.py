from traits.api import Unicode, File

from force_bdss.core.verifier import VerifierError
from force_bdss.api import BaseDataSourceModel


class ChemicalDataSourceModel(BaseDataSourceModel):
    """Class containing all parameters for a single chemical
    ingredient (molecular species) in a Gromacs
    simulation"""

    name = Unicode(
        desc='Name of molecular chemical')

    symbol = Unicode(
        desc='Reference symbol in input Gromacs topology file')

    topology = File(
        desc='File path for Gromacs topology file',
        verify=True
    )

    coordinate = File(
        desc='File path for Gromacs coordinate file',
        verify=True
    )

    def _file_check(self, file_path, ext):
        """Performs a series of checks on selected Gromacs
        file

        Parameters
        ----------
        file_path: str
            File path for Gromacs input file
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

        elif not file_path.endswith('.{}'.format(ext)):
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

    # Overloads BaseDataSourceModel verify method to check file names
    # and counter-ion status upon activation of verify_workflow_event.
    def verify(self):

        errors = super(ChemicalDataSourceModel, self).verify()
        errors += self._file_check(self.topology, 'itp')
        errors += self._file_check(self.coordinate, 'gro')

        return errors
