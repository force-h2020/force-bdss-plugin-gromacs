from traits.api import (
    HasStrictTraits, List, Unicode, Float, Property,
    Bool, cached_property, Int
)

from force_bdss.api import DataValue

from force_gromacs.chemicals.i_fragment import IFragment

from .base_particle_group import BaseParticleGroup


class Molecule(BaseParticleGroup):
    """Class representing a neutral molecular species consisting of
    one or more molecular fragments"""

    # --------------------
    #  Required Attributes
    # --------------------

    #: List of molecular fragments that make up this molecule.
    fragments = List(IFragment)

    # --------------------
    #  Regular Attributes
    # --------------------

    #: Molecule name
    name = Unicode()

    #: Number of molecules to be added to simulation
    n_mol = Int()

    # --------------------
    #     Properties
    # --------------------

    #: Molecular mass of all molecular fragments
    mass = Property(Float, depends_on='fragments.[mass,number]')

    #: Molecular mass of all molecular fragments
    charge = Property(Float, depends_on='fragments.[charge,number]')

    #: Check to ensure the molecule is electronically neutral
    neutral = Property(Bool, depends_on='charge')

    # --------------------
    #      Defaults
    # --------------------

    def _name_default(self):
        """Naive naming procedure, based on name and charge of constituent
        fragments. Follows general chemical nomenclature of naming an
        ionic compound first by its positive ion, followed by its negative
        ion."""
        name = ''
        for fragment in self.fragments:
            if fragment.charge < 0:
                name = ' '.join([name, fragment.name]).strip()
            else:
                name = ' '.join([fragment.name, name]).strip()
        return name

    # --------------------
    #     Listeners
    # --------------------

    @cached_property
    def _get_mass(self):
        return sum([fragment.mass * fragment.number
                    for fragment in self.fragments])

    @cached_property
    def _get_charge(self):
        return sum([fragment.charge * fragment.number
                    for fragment in self.fragments])

    def _get_neutral(self):
        """Check whether molecule is neutral"""
        return self.charge == 0

    # --------------------
    #    Public Methods
    # --------------------

    def get_data_values(self):
        """Return a list containing all regular DataValues stored
        in class"""
        data_values = [DataValue(type="NAME", value=self.name),
                       DataValue(type="MASS", value=self.mass)]

        return data_values
