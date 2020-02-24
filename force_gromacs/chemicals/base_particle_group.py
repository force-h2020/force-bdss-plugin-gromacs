from traits.api import (
    HasStrictTraits,
    List,
    Int,
    Tuple,
    Property,
    Float,
    provides
)

from force_bdss.api import DataValue

from .i_particle import IParticle
from .i_particle_group import IParticleGroup


@provides(IParticleGroup)
class BaseParticleGroup(HasStrictTraits):
    """Contains all input values for each particle group. Here, a
    group can be defined as a single atom or collection of
    covalently bonded atoms who therefore behave as a fixed body.
    Therefore we also explicitly include a list of indices referring
    to bonds between pairs of particles"""

    # --------------------
    #  Regular Attributes
    # --------------------

    #: Dictionary containing each particle species reference
    #: index
    particles = List(IParticle)

    #: List of bonded particles, referring to indices in
    #: `particles` attribute
    bonds = List(Tuple(Int, Int))

    # --------------------
    #     Properties
    # --------------------

    #: Total mass of group
    mass = Property(Float, depends_on='particles.mass')

    #: Total charge of group
    charge = Property(Float, depends_on='particles.charge')

    def _get_mass(self):
        return sum([
            particle.mass
            for particle in self.particles])

    def _get_charge(self):
        return sum([
            particle.charge
            for particle in self.particles])

    def get_data_values(self):
        """Return a list containing all DataValues stored in class"""

        return [
            DataValue(type="MASS", value=self.mass),
            DataValue(type="CHARGE", value=self.charge)
        ]
