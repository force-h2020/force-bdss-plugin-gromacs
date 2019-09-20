""" This submodule implements the following :class:`BaseGromacsCommand`
subclasses:

* :class:`Gromacs_genconf` provides a wrapper around Gromacs genconf command.
* :class:`Gromacs_genbox` provides a wrapper around Gromacs genbox command.
* :class:`Gromacs_grompp` provides a wrapper around Gromacs genmpp command.
* :class:`Gromacs_genion` provides a wrapper around Gromacs genion command.
* :class:`Gromacs_mdrun` provides a wrapper around Gromacs mdrun command.

The `name` and `flags` attributes of these subclasses have been overridden as
ReadOnly traits, and so cannot be mutated during runtime. Developers wishing to
create further wrappers around additional Gromacs commands are encouraged to do
so in a similar way.

Note - all objects are tested on Gromacs version 4.6.7
"""

from traits.api import ReadOnly

from force_gromacs.core.base_gromacs_command import BaseGromacsCommand


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
    http://manual.gromacs.org/documentation/2018/onlinehelp/gmx-mdrun.html

    Extra boolean attribute `mpi_run` signals whether to perform a
    simulation using MPI parallel processing (default is `False`). The number
    of cores can also be set using the `n_proc` attribute (default is `1`).

    Example
    ------
    Calling simulation run in series:
        md_run = Gromacs_mdrun()
    Calling a MPI run on 2 cores:
        mpi_mdrun = Gromacs_mdrun(mpi_run=True, n_proc=2)
    """

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


class Gromacs_select(BaseGromacsCommand):
    """Wrapper around Gromacs select (or g_select) command
    http://manual.gromacs.org/archive/4.6.5/online/g_select.html"""

    #: Name of Gromacs genbox command
    name = ReadOnly('g_select')

    #: List of accepted flags for Gromacs genbox command
    flags = ReadOnly(['-f', '-s', '-n', '-os', '-oc', '-oi',
                      '-on', '-om', '-of', '-ofpdb', '-olt', '-b',
                      '-e', '-dt', 'tu', '-fgroup', '-xvg',
                      '-rmpbc', '-normpbc', '-pbc', '-nppbc', '-sf',
                      '-selrpos', '-seltype', '-select', '-norm',
                      '-nonorm', '-resnr', 'pdbatoms', '-cumlt',
                      '-nocumlt'])

    def __init__(self, name=None, flags=None,
                 *args, **kwargs):
        super(Gromacs_select, self).__init__(*args, **kwargs)


class Gromacs_trjconv(BaseGromacsCommand):
    """Wrapper around Gromacs trjconv command
    http://manual.gromacs.org/documentation/2018/onlinehelp/gmx-trjconv.html"""

    #: Name of Gromacs trjconv command
    name = ReadOnly('trjconv')

    #: List of accepted flags for Gromacs genion command
    flags = ReadOnly(['-f', '-s', '-n', '-fr', '-sub', '-drop',
                      '-o', '-b', '-e', '-tu', '-w', '-now', '-xvg',
                      '-skip', '-dt', 'round', '-noround', '-dump',
                      '-timestep', '-pbc', '-ur', '-centre', '-nocentre',
                      '-boxcenter', '-box', '-trans', '-shift', '-fit',
                      '-ndec', 'vel', '-novel', '-force', '-noforce',
                      '-trunc', '-exec', '-split', '-sep', '-nosep',
                      '-nzero', '-dropunder', '-dropover', '-conect',
                      '-noconect'])

    def __init__(self, name=None, flags=None,
                 *args, **kwargs):
        super(Gromacs_trjconv, self).__init__(*args, **kwargs)
