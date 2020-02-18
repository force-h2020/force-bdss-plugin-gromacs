from traits.api import HasStrictTraits, Str, Float, provides

from force_gromacs.chemicals.i_particle import IParticle
from force_gromacs.chemicals.molecule import Molecule
from force_gromacs.chemicals.gromacs_particle import GromacsParticle
from force_gromacs.chemicals.gromacs_fragment import GromacsFragment


data = {
    'W': {
        'elements': ['O', 'H', 'H'],
        'ids': ['O', 'H1', 'H2'],
        'indices': [1, 2, 3],
        'charges': [-2, 1, 1],
        'masses': [16, 1, 1],
        'bonds': [(1, 2), (2, 3)]
    },
    'PI': {
        'elements': ['PI'],
        'ids': ['PI'],
        'indices': [1],
        'charges': [1],
        'masses': [23],
        'bonds': []
    },
    'NI': {
        'elements': ['NI'],
        'ids': ['NI'],
        'indices': [1],
        'charges': [-1],
        'masses': [35],
        'bonds': []
    }
}


def particle_generator(key):
    """Simple generator to provide input details for each
    GromacsParticle instance in a ProbeGromacsFragment"""
    inner_keys = [
        'elements', 'ids', 'indices',
        'charges', 'masses'
    ]

    generator = tuple(
        data[key][inner_key] for inner_key in inner_keys
    )

    for element, id, index, charge, mass in zip(*generator):
        yield element, id, index, charge, mass


@provides(IParticle)
class ProbeParticle(HasStrictTraits):

    symbol = Str()

    mass = Float()

    charge = Float()


class ProbeGromacsFragment(GromacsFragment):
    def __init__(self, name="Water", symbol='W'):
        generator = particle_generator(symbol)
        particles = [
            GromacsParticle(
                element=element, index=index, id=id,
                charge=charge, mass=mass
            )
            for element, id, index, charge, mass in generator
        ]
        bonds = data[symbol]['bonds']
        super(ProbeGromacsFragment, self).__init__(
            name=name,
            symbol=symbol,
            particles=particles,
            bonds=bonds,
            topology="test_top.itp",
            coordinate="test_coord.gro"
        )


class ProbeMolecule(Molecule):

    def __init__(self, name):
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
