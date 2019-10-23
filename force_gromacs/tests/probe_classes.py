from unittest import mock

from force_gromacs.commands.gromacs_commands import (
    Gromacs_genbox, Gromacs_genion
)
from force_gromacs.io.gromacs_file_tree_builder import (
    GromacsFileTreeBuilder
)
from force_gromacs.data_sources.fragment import Fragment
from force_gromacs.io.gromacs_topology_writer import (
    GromacsTopologyWriter
)
from force_gromacs.pipeline.gromacs_pipeline import (
    GromacsPipeline
)
from force_gromacs.pipeline.gromacs_simulation_builder import (
    GromacsSimulationBuilder
)


data = {
    'W': {
        'atoms': ['W'],
        'charges': [0],
        'masses': [18]
    },
    'PI': {
        'atoms': ['PI'],
        'charges': [1],
        'masses': [23]
    },
    'NI': {
        'atoms': ['NI'],
        'charges': [-1],
        'masses': [35]
    }
}

mock_method = (
    "force_gromacs.io.gromacs_topology_reader"
    ".GromacsTopologyReader.read"
)


class ProbeFragment(Fragment):
    def __init__(self, name="Water", symbol='W'):

        with mock.patch(mock_method) as mockreadtop:
            mockreadtop.return_value = data
            super(ProbeFragment, self).__init__(
                name=name,
                symbol=symbol,
                topology="test_top.itp",
                coordinate="test_coord.gro"
            )


class ProbeMolecule(Fragment):

    def __init__(self, name):
        with mock.patch(mock_method) as mockreadtop:
            mockreadtop.return_value = data
            if name == 'Water':
                fragments = [
                    ProbeFragment(name='Water',
                                  symbol='W')
                ]
            elif name == 'Salt':
                fragments = [
                    ProbeFragment(name='Positive Ion',
                                  symbol='PI'),
                    ProbeFragment(name='Negative Ion',
                                  symbol='NI')
                ]

        super(ProbeMolecule, self).__init__(
            name=name,
            fragments=fragments
        )


class ProbeGromacsPipeline(GromacsPipeline):

    def __init__(self):
        steps = [
            (
                'file_tree',
                GromacsFileTreeBuilder(
                    directory='./test_experiment',
                    folders=[
                        '1_build', '2_minimize', '3_production'
                    ],
                    dry_run=False
                )
            ),
            (
                'genbox',
                Gromacs_genbox(
                    command_options={
                        '-cp': 'test_coord.gro',
                        '-nmol': 30,
                        '-o': 'test_output.gro',
                        '-not_a_flag': 60,
                        '-try': True
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

        super(ProbeGromacsPipeline, self).__init__(steps=steps)


class ProbeSimulationBuilder(GromacsSimulationBuilder):

    def build_pipeline(self):
        return ProbeGromacsPipeline()
