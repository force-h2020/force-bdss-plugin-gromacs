from traits.api import List

from .i_particle import IParticle


class IParticleGroup(IParticle):
    """Contains all input values for a collection of particles.
    At this stage we simply restrict this to a list of IParticle
    instances that are contained within the group. Later
    implementations may require an explicit description of the
    bonds or connections between particles
    """

    #: List of particles in group
    particles = List(IParticle)
