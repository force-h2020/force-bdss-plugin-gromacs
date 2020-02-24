from traits.api import Str, File, Int, List, Property, provides

from force_bdss.api import DataValue

from .base_particle_group import BaseParticleGroup
from .i_fragment import IFragment


@provides(IFragment)
class GromacsFragment(BaseParticleGroup):
    """Contains all input values for a molecular fragment, as defined
    by Gromacs input scripts. Also contains useful routines for
    postprocessing Gromacs files, such as returning a list of atom
    references and masses.
    """

    # --------------------
    #  Required Attributes
    # --------------------

    #: Symbol referring to fragment in Gromacs input files
    symbol = Str()

    #: Gromacs topology '.itp' file
    topology = File()

    #: Gromacs coordinate '.gro' file
    coordinate = File()

    # --------------------
    #  Regular Attributes
    # --------------------

    #: Human readable name for reference
    name = Str()

    #: Stoichiometric number of fragments in molecule
    stoichiometry = Int(1)

    # --------------------
    #     Properties
    # --------------------

    #: List of atoms in Gromacs topology '.itp' file
    atoms = Property(List(Str), depends_on='particles.id')

    def _get_atoms(self):
        return [particle.id for particle in self.particles]

    # --------------------
    #   Public Methods
    # --------------------

    def get_masses(self):
        """Return list of atomic masses"""
        return [particle.mass for particle in self.particles]

    def get_data_values(self):
        """Return a list containing all DataValues stored in class"""

        return [
            DataValue(type="NAME", value=self.name),
            DataValue(type="SYMBOL", value=self.symbol),
            DataValue(type="ATOMS", value=self.atoms),
            DataValue(type="MASS", value=self.mass),
            DataValue(type="CHARGE", value=self.charge),
            DataValue(type="TOPOLOGY", value=self.topology),
            DataValue(type="COORDINATE", value=self.coordinate)
        ]
