from traits.api import HasStrictTraits, Str, Float, provides, Int

from .i_particle import IParticle


@provides(IParticle)
class GromacsParticle(HasStrictTraits):
    """Contains all input values for a particle species, defined in
    terms of classical mechanics by a mass and charge. An example
    particle may include an atom, molecule or ion"""

    #: Index of particle in molecular .itp file
    index = Int()

    #: Reference id of particle
    id = Str()

    #: Elemental symbol particle
    element = Str()

    #: Particle mass of fragment in g / mol
    mass = Float

    #: Particle charge of fragment
    charge = Float
