import os

from traits.api import List, Unicode, Int

from gromacs.core.base_gromacs_process import BaseGromacsProcess


class GromacsTopologyWriter(BaseGromacsProcess):
    """  Class writes Gromacs topology file"""

    # --------------------
    #  Required Attributes
    # --------------------

    #: Reference name for the Gromacs simulation
    sim_name = Unicode()

    #: List of Gromacs topology files to be included
    topologies = List(Unicode)

    #: List of molecular symbols referenced from
    #: from the files in `topologies` to be included in the
    #: simulation
    symbols = List(Unicode)

    #: List of integers referring to the number of each
    #: molecular species in `symbols` to be included in the
    #: simulation
    n_mols = List(Int)

    # --------------------
    #  Regular Attributes
    # --------------------

    #: Location to create topology in. (By default, the
    #: current working directory)
    directory = Unicode()

    #: Name of the Gromacs topology file to be created
    top_name = Unicode()

    # ------------------
    #      Defaults
    # ------------------

    def _directory_default(self):
        return f"{os.path.curdir}/{self.sim_name}"

    def _top_name_default(self):
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
        for symbol, n in zip(self.symbols, self.n_mols):
            top_file += '{} {}\n'.format(symbol, n)

        return top_file

    # ------------------
    #   Public Methods
    # ------------------

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

        return self._returncode
