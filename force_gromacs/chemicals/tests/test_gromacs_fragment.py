from unittest import TestCase

from force_gromacs.tests.probe_classes.chemicals import ProbeGromacsFragment


class TestGromacsFragment(TestCase):

    def setUp(self):

        self.fragment = ProbeGromacsFragment()

    def test___init__(self):

        self.assertEqual("Water", self.fragment.name)
        self.assertEqual("W", self.fragment.symbol)
        self.assertEqual(["O", "H1", "H2"], self.fragment.atoms)
        self.assertEqual(18.0, self.fragment.mass)
        self.assertEqual(0, self.fragment.charge)
        self.assertEqual("test_top.itp", self.fragment.topology)
        self.assertEqual("test_coord.gro", self.fragment.coordinate)

    def test_get_masses(self):

        masses = self.fragment.get_masses()
        self.assertListEqual([16, 1, 1], masses)

    def test_get_data_values(self):

        data = self.fragment.get_data_values()

        self.assertEqual("Water", data[0].value)
        self.assertEqual("NAME", data[0].type)
        self.assertEqual("W", data[1].value)
        self.assertEqual("SYMBOL", data[1].type)
        self.assertEqual(["O", "H1", "H2"], data[2].value)
        self.assertEqual("ATOMS", data[2].type)
        self.assertEqual(18.0, data[3].value)
        self.assertEqual("MASS", data[3].type)
        self.assertEqual(0, data[4].value)
        self.assertEqual("CHARGE", data[4].type)
        self.assertEqual("test_top.itp", data[5].value)
        self.assertEqual("TOPOLOGY", data[5].type)
        self.assertEqual("test_coord.gro", data[6].value)
        self.assertEqual("COORDINATE", data[6].type)
