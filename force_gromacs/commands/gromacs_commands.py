from traits.api import (
    ReadOnly
)

from force_gromacs.api import BaseGromacsCommand


class Gromacs_genconf(BaseGromacsCommand):
    """Wrapper around Gromacs genconf command
    http://manual.gromacs.org/archive/4.6.5/online/genconf.html"""

    #: Name of Gromacs genbox command
    name = ReadOnly('genconf')

    #: List of accepted flags for Gromacs genbox command
    flags = ReadOnly(['-f', '-o', '-trj', '-nbox'])

    def __init__(self, name=None, flags=None,
                 *args, **kwargs):
        super(Gromacs_genconf, self).__init__(*args, **kwargs)


#: NOTE: as of Gromacs 5.0, this tool has been split to gmx solvate
#: and gmx insert-molecules.
class Gromacs_genbox(BaseGromacsCommand):
    """Wrapper around Gromacs genbox command
    http://manual.gromacs.org/archive/4.6.5/online/genbox.html"""

    #: Name of Gromacs genbox command
    name = ReadOnly('genbox')

    #: List of accepted flags for Gromacs genbox command
    flags = ReadOnly(['-cp', '-cs', '-ci', '-maxsol',
                      '-o', '-box', '-try', '-nmol'])

    def __init__(self, name=None, flags=None,
                 *args, **kwargs):
        super(Gromacs_genbox, self).__init__(*args, **kwargs)


class Gromacs_grompp(BaseGromacsCommand):
    """Wrapper around Gromacs grompp command
    http://manual.gromacs.org/documentation/2018/onlinehelp/gmx-grompp.html"""

    #: Name of Gromacs grompp command
    name = ReadOnly('grompp')

    #: List of accepted flags for Gromacs grompp command
    flags = ReadOnly(['-f', '-c', '-r', '-rb', '-n', '-p',
                      '-t', '-e', '-ref', '-po', '-pp',
                      '-o', '-idm', '-time', '-maxwarn'])

    def __init__(self, name=None, flags=None,
                 *args, **kwargs):
        super(Gromacs_grompp, self).__init__(*args, **kwargs)


class Gromacs_genion(BaseGromacsCommand):
    """Wrapper around Gromacs genion command
    http://manual.gromacs.org/documentation/2018/onlinehelp/gmx-genion.html"""

    #: Name of Gromacs genion command
    name = ReadOnly('genion')

    #: List of accepted flags for Gromacs genion command
    flags = ReadOnly(['-s', '-n', '-p', '-o', '-np', '-pname',
                      '-pq', '-nn', '-nname', '-nq', '-rmin',
                      '-seed', '-conc'])

    def __init__(self, name=None, flags=None,
                 *args, **kwargs):
        super(Gromacs_genion, self).__init__(*args, **kwargs)


class Gromacs_mdrun(BaseGromacsCommand):
    """Wrapper around Gromacs mdrun command
    http://manual.gromacs.org/documentation/2018/onlinehelp/gmx-mdrun.html"""

    #: Name of Gromacs genion command
    name = ReadOnly()

    #: List of accepted flags for Gromacs genion command
    flags = ReadOnly(['-s', '-g', '-e', '-o', '-x', '-c',
                      '-cpo'])

    def __init__(self, name=None, flags=None, mpi_run=False,
                 n_proc=1, *args, **kwargs):

        if mpi_run:
            name = f'mpirun -np {n_proc} mdrun_mpi'
        else:
            name = 'mdrun'

        super(Gromacs_mdrun, self).__init__(
            name=name, *args, **kwargs
        )
