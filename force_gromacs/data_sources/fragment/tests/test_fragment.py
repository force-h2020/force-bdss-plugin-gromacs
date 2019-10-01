from unittest import mock, TestCase

from force_gromacs.gromacs_plugin import GromacsPlugin
from force_gromacs.tests.probe_classes import ProbeFragment


class TestFragmentDataSource(TestCase):

    def setUp(self):
        self.plugin = GromacsPlugin()
        self.factory = self.plugin.data_source_factories[0]
        self.data_source = self.factory.create_data_source()

    def test_basic_function(self):

        model = self.factory.create_model()
        model.name = "Water"
        model.symbol = "W"
        model.topology = "test_top.itp"
        model.coordinate = "test_coord.gro"

        data_values = []
        top_lines = ['; Water \n', '[moleculetype]\n', ';\n',
                     ' W 1\n', '\n' '[ atoms]\n', ';\n',
                     '1 P 1 W W 1 0 18.0 \n', '\n']
        mock_method = (
            "force_gromacs.io.gromacs_topology_reader"
            ".GromacsTopologyReader._read_file")

        with mock.patch(mock_method) as mockreadtop:
            mockreadtop.return_value = top_lines

            res = self.data_source.run(model, data_values)
            self.assertEqual("FRAGMENT", res[0].type)

            fragment = res[0].value
            self.assertEqual("Water", fragment.name)
            self.assertEqual("W", fragment.symbol)
            self.assertEqual(["W"], fragment.atoms, )
            self.assertEqual(18.0, fragment.mass, )
            self.assertEqual(0, fragment.charge)
            self.assertEqual("test_top.itp", fragment.topology)
            self.assertEqual("test_coord.gro", fragment.coordinate)


class TestFragment(TestCase):

    def setUp(self):

        top_lines = ['; Water \n', '[moleculetype]\n', ';\n',
                     ' W 1\n', '\n' '[ atoms]\n', ';\n',
                     '1 P 1 W W 1 0 18.0 \n', '\n']
        mock_method = (
            "force_gromacs.io.gromacs_topology_reader"
            ".GromacsTopologyReader._read_file")

        with mock.patch(mock_method) as mockreadtop:
            mockreadtop.return_value = top_lines
            self.fragment = ProbeFragment()

    def test___init__(self):

        self.assertEqual("Water", self.fragment.name)
        self.assertEqual("W", self.fragment.symbol)
        self.assertEqual(["W"], self.fragment.atoms)
        self.assertEqual(18.0, self.fragment.mass)
        self.assertEqual(0, self.fragment.charge)
        self.assertEqual("test_top.itp", self.fragment.topology)
        self.assertEqual("test_coord.gro", self.fragment.coordinate)

    def test_get_masses(self):

        masses = self.fragment.get_masses()
        self.assertListEqual([18], masses)

    def test_get_data_values(self):

        data = self.fragment.get_data_values()

        self.assertEqual("Water", data[0].value)
        self.assertEqual("NAME", data[0].type)
        self.assertEqual("W", data[1].value)
        self.assertEqual("SYMBOL", data[1].type)
        self.assertEqual(["W"], data[2].value)
        self.assertEqual("ATOMS", data[2].type)
        self.assertEqual(18.0, data[3].value)
        self.assertEqual("MASS", data[3].type)
        self.assertEqual(0, data[4].value)
        self.assertEqual("CHARGE", data[4].type)
        self.assertEqual("test_top.itp", data[5].value)
        self.assertEqual("TOPOLOGY", data[5].type)
        self.assertEqual("test_coord.gro", data[6].value)
        self.assertEqual("COORDINATE", data[6].type)