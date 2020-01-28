from traits.api import Interface, List, Str, Float


class IFragment(Interface):
    """Contains all input values for each molecular fragment. A
    fragment is defined as a part of a fragment that may become
    dissociated (i.e - an ion) and therefore requires its own set
    of chemical / structural information"""

    #: List of atoms in molecular fragment
    atoms = List(Str)

    #: Molecular mass of fragment in g / mol
    mass = Float

    #: Molecular charge of fragment
    charge = Float

    def get_data_values(self):
        """Return a list containing all DataValues stored in class"""
