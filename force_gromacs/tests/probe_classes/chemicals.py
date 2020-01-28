from unittest import mock

from force_gromacs.chemicals.molecule import Molecule
from force_gromacs.chemicals.gromacs_fragment import GromacsFragment


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


class ProbeGromacsFragment(GromacsFragment):
    def __init__(self, name="Water", symbol='W'):

        with mock.patch(mock_method) as mockreadtop:
            mockreadtop.return_value = data
            super(ProbeGromacsFragment, self).__init__(
                name=name,
                symbol=symbol,
                topology="test_top.itp",
                coordinate="test_coord.gro"
            )


class ProbeMolecule(Molecule):

    def __init__(self, name):
        with mock.patch(mock_method) as mockreadtop:
            mockreadtop.return_value = data
            if name == 'Water':
                fragments = [
                    ProbeGromacsFragment(name='Water',
                                         symbol='W')
                ]
            elif name == 'Salt':
                fragments = [
                    ProbeGromacsFragment(name='Positive Ion',
                                         symbol='PI'),
                    ProbeGromacsFragment(name='Negative Ion',
                                         symbol='NI')
                ]

        super(ProbeMolecule, self).__init__(
            name=name,
            fragments=fragments
        )
