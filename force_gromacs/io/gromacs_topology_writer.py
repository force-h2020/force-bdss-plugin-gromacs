import os

from traits.api import (
    HasTraits, List, Str, Dict, Int, provides
)

from force_gromacs.core.i_process import IProcess


@provides(IProcess)
class GromacsTopologyWriter(HasTraits):
    """Class writes Gromacs topology file"""

    # --------------------
    #  Required Attributes
    # --------------------

    #: List of Gromacs topology files to be included
    topologies = List(Str)

    #: Dictionary containing keys referring to molecular symbols
    #: referenced from the files in `topologies`, with values determining
    #: the number of each molecule to be included in the simulation
    fragment_dict = Dict(Str, Int)

    # ------------------------------
    #  Required / Regular Attributes
    # ------------------------------

    #: Location to create topology file in. If not provided,
    #: a default value including sim_name attribute will be used.
    directory = Str()

    #: Name of the Gromacs topology file to be created. If not provided,
    #: a default value including sim_name attribute will be used.
    top_name = Str()

    #: Reference name for the Gromacs simulation. Can be used to define
    #: default values of directory and top_name attributes
    sim_name = Str()

    # ------------------
    #      Defaults
    # ------------------

    def _directory_default(self):
        """If directory is not defined, use current directory
        with sim_name as default directory"""
        return f"{os.path.curdir}/{self.sim_name}"

    def _top_name_default(self):
        """If topology file name is not defined, use sim_name with
        .top extension as default file name"""
        return f"{self.sim_name}_topol.top"

    # ------------------
    #  Private Methods
    # ------------------

    def _create_simulation_top(self):
        """Builds human readable topology file for Gromacs simulation"""

        top_file = ""
        included_topologies = []
        for topology in self.topologies:
            if topology not in included_topologies:
                top_file += '#include "{}"\n'.format(topology)
                included_topologies.append(topology)

        top_file += '\n[ system ]\n'
        top_file += self.sim_name + '\n'

        top_file += '\n[ molecules ]\n'
        for symbol, n_mol in self.fragment_dict.items():
            top_file += '{} {}\n'.format(symbol, n_mol)

        return top_file

    # ------------------
    #   Public Methods
    # ------------------

    def recall_stderr(self):
        """Returns dummy stderr message"""
        return ''

    def recall_stdout(self):
        """Returns dummy stdout message"""
        return ''

    def bash_script(self):
        """Output terminal command as a bash script"""

        top_file = self._create_simulation_top()

        bash_script = (
            f"cat <<EOM > {self.directory}/{self.top_name}"
            f"\n{top_file}EOM"
        )

        return bash_script

    def run(self):
        """Writes a human readable topology file for
        Gromacs simulation"""

        top_file = self._create_simulation_top()

        if not self.dry_run:
            with open(f'{self.directory}/{self.top_name}',
                      'w') as outfile:
                outfile.write(top_file)

        # Provide successful return code
        return 0
