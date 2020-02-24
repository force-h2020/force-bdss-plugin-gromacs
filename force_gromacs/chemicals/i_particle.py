from traits.api import Interface, Float


class IParticle(Interface):
    """Contains all input values for a particle species, defined in
    terms of classical mechanics by a mass and charge. An example
    particle may include an atom, molecule or ion"""

    #: Particle mass of fragment in g / mol
    mass = Float()

    #: Particle charge of fragment
    charge = Float()
