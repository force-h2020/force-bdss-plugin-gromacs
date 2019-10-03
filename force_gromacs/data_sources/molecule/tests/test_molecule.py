from unittest import TestCase

from force_gromacs.data_sources.molecule import Molecule
from force_gromacs.tests.probe_classes import (
    ProbeFragment
)


class TestMolecule(TestCase):

    def setUp(self):
        self.water = ProbeFragment()
        self.positive_ion = ProbeFragment(
            name='Positive Ion', symbol='PI')
        self.negative_ion = ProbeFragment(
            name='Negative Ion', symbol='NI')

        self.molecule = Molecule(
            fragments=[self.water],
            n_mol=10
        )

    def test___init__(self):
        self.assertEqual('Water', self.molecule.name)
        self.assertEqual(1, len(self.molecule.fragments))
        self.assertEqual(18, self.molecule.mass)
        self.assertEqual(10, self.molecule.n_mol)
        self.assertEqual(0, self.molecule.charge)
        self.assertTrue(self.molecule.neutral)

    def test_charge(self):

        self.molecule.fragments.append(self.positive_ion)
        self.assertEqual(1, self.molecule.charge)
        self.assertFalse(self.molecule.neutral)

        self.molecule.fragments.append(self.negative_ion)
        self.assertEqual(0, self.molecule.charge)
        self.assertTrue(self.molecule.neutral)

        self.molecule.fragments[1].number = 2
        self.assertEqual(1, self.molecule.charge)
        self.assertFalse(self.molecule.neutral)

        self.molecule.fragments[2].number = 2
        self.assertEqual(0, self.molecule.charge)
        self.assertTrue(self.molecule.neutral)

    def test_name(self):

        self.molecule.fragments.append(self.positive_ion)
        self.assertEqual('Positive Ion Water',
                         self.molecule.name)

        self.molecule.fragments.append(self.negative_ion)
        self.molecule.name = self.molecule._name_default()
        self.assertEqual('Positive Ion Water Negative Ion',
                         self.molecule.name)

    def test_mass(self):
        self.molecule.fragments.append(self.positive_ion)
        self.assertEqual(41, self.molecule.mass)

        self.molecule.fragments.append(self.negative_ion)
        self.assertEqual(76, self.molecule.mass)

        self.molecule.fragments[1].number = 2
        self.assertEqual(99, self.molecule.mass)

        self.molecule.fragments[2].number = 2
        self.assertEqual(134, self.molecule.mass)

    def test_get_data_values(self):

        data_values = self.molecule.get_data_values()

        self.assertEqual("Water", data_values[0].value)
        self.assertEqual("NAME", data_values[0].type)
        self.assertEqual(18.0, data_values[1].value)
        self.assertEqual("MASS", data_values[1].type)
