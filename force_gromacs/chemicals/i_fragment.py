from traits.api import List, Int

from .i_particle import IParticle


class IFragment(IParticle):
    """Contains all input values for each molecular fragment. A
    fragment is defined as a part of a fragment that may become
    dissociated (i.e - an ion) and therefore requires its own set
    of chemical / structural information"""

    #: List of particles in molecular fragment
    particles = List(IParticle)

    #: Stoichiometric number of molecular fragment
    number = Int(1)
