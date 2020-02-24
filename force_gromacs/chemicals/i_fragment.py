from traits.api import List, Int

from .i_particle_group import IParticleGroup


class IFragment(IParticleGroup):
    """Contains all input values for each molecular fragment. A
    fragment is defined as a part of a molecule that may become
    dissociated (i.e - an ion) and therefore requires its own set
    of chemical / structural information.

    The only difference between an IFragment and IParticleGroup
    is the notion that a fragment cannot be an isolated species;
    if must exist within a molecule. Therefore we need to know
    the stoichiometric number of each fragment in the molecule
    """

    #: Stoichiometric number of molecular fragment
    number = Int(1)
