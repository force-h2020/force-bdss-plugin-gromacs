from unittest import mock, TestCase

from force_gromacs.gromacs_plugin import GromacsPlugin
from force_gromacs.data_sources.fragment import Fragment


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
            self.assertEqual(res[0].type, "FRAGMENT")

            molecule = res[0].value
            self.assertEqual(molecule.name, "Water")
            self.assertEqual(molecule.symbol, "W")
            self.assertEqual(molecule.topology, "test_top.itp")
            self.assertEqual(molecule.coordinate, "test_coord.gro")


class TestFragment(TestCase):

    def setUp(self):

        name = "Water"
        symbol = "W"
        topology = "test_top.itp"
        coordinate = "test_coord.gro"

        self.molecule = Fragment(
            name=name,
            symbol=symbol,
            topology=topology,
            coordinate=coordinate
        )

    def test___init__(self):

        self.assertEqual("Water", self.molecule.name)
        self.assertEqual("W", self.molecule.symbol)
        self.assertEqual("test_top.itp", self.molecule.topology)
        self.assertEqual("test_coord.gro", self.molecule.coordinate)

    def test_get_data_values(self):

        data = self.molecule.get_data_values()

        self.assertEqual("Water", data[0].value)
        self.assertEqual("NAME", data[0].type)
        self.assertEqual("W", data[1].value)
        self.assertEqual("SYMBOL", data[1].type)
        self.assertEqual("test_top.itp", data[2].value)
        self.assertEqual("TOPOLOGY", data[2].type)
        self.assertEqual("test_coord.gro", data[3].value)
        self.assertEqual("COORDINATE", data[3].type)
