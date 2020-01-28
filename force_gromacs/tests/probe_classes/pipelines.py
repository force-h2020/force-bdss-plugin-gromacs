from traits.api import HasStrictTraits, Bool, provides

from force_gromacs.commands.gromacs_commands import (
    Gromacs_solvate, Gromacs_genion
)
from force_gromacs.io.file_tree_builder import (
    FileTreeBuilder
)
from force_gromacs.pipelines.base_pipeline import BasePipeline
from force_gromacs.core.i_process import IProcess
from force_gromacs.io.gromacs_topology_writer import (
    GromacsTopologyWriter
)
from force_gromacs.pipelines.gromacs_pipeline import (
    GromacsPipeline
)


@provides(IProcess)
class ProbeProcess(HasStrictTraits):

    dry_run = Bool()

    def recall_stderr(self):
        return ''

    def recall_stdout(self):
        return ''

    def bash_script(self):
        return ''

    def run(self):
        pass


class ProbePipeline(BasePipeline):
    def __init__(self):
        steps = [
            ('first', ProbeProcess()),
            ('second', ProbeProcess()),
            ('third', ProbeProcess()),
            ('fourth', ProbeProcess())
        ]
        super(ProbePipeline, self).__init__(steps=steps)


class ProbeGromacsPipeline(GromacsPipeline):

    def __init__(self):
        steps = [
            (
                'file_tree',
                FileTreeBuilder(
                    directory='./test_experiment',
                    folders=[
                        '1_build', '2_minimize', '3_production'
                    ],
                    dry_run=True
                )
            ),
            (
                'solvate',
                Gromacs_solvate(
                    command_options={
                        '-cp': 'test_coord.gro',
                        '-radius': 30,
                        '-o': 'test_output.gro',
                        '-not_a_flag': 60
                    }
                )
            ),
            (
                'genion',
                Gromacs_genion(
                    command_options={
                        '-s': 'test_top.trp',
                        '-p': 'test_top.top',
                        '-pname': 'test_coord_2.gro',
                        '-np': 64,
                        '-pq': 1,
                        '-o': 'test_output.gro',
                        '-cp': 'problem'
                    }
                )
            ),
            (
                'top_file',
                GromacsTopologyWriter(
                    top_name='test_topology.top',
                    sim_name='test_experiment',
                    topologies=['test_top.itp'],
                    fragment_dict={'S': 30}
                )
            )
        ]

        super(ProbeGromacsPipeline, self).__init__(
            steps=steps, dry_run=True)
