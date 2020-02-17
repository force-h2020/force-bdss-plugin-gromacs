from traits.api import Interface, Array, Any


class IParticleState(Interface):
    """Interface class carrying data that is can be used to determine
    the state of an particle during a Molecular simulation"""

    #: Reference id of particle
    id = Any()

    # Position of particle in each dimension
    position = Array()

    # Velocity of particle in each dimension
    velocity = Array()

    # Total force applied to particle in each dimension
    force = Array()
