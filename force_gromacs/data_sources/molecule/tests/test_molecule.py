from unittest import mock, TestCase

from force_gromacs.gromacs_plugin import GromacsPlugin
from force_gromacs.data_sources.molecule import Molecule


class TestMoleculeDataSource(TestCase):

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
            self.assertEqual(res[0].type, "MOLECULE")

            molecule = res[0].value
            self.assertEqual(molecule.name, "Water")
            self.assertEqual(molecule.symbol, "W")
            self.assertEqual(molecule.mass, 18.0)
            self.assertEqual(molecule.charge, 0)
            self.assertEqual(molecule.topology, "test_top.itp")
            self.assertEqual(molecule.coordinate, "test_coord.gro")


class TestMolecule(TestCase):

    def setUp(self):

        name = "Water"
        symbol = "W"
        mass = 18.0
        charge = 0
        topology = "test_top.itp"
        coordinate = "test_coord.gro"

        self.molecule = Molecule(
            name=name,
            symbol=symbol,
            mass=mass,
            charge=charge,
            topology=topology,
            coordinate=coordinate
        )

    def test___init__(self):

        self.assertEqual("Water", self.molecule.name)
        self.assertEqual("W", self.molecule.symbol)
        self.assertEqual(18.0, self.molecule.mass)
        self.assertEqual(0, self.molecule.charge)
        self.assertEqual("test_top.itp", self.molecule.topology)
        self.assertEqual("test_coord.gro", self.molecule.coordinate)

    def test_get_data_values(self):

        data = self.molecule.get_data_values()

        self.assertEqual("Water", data[0].value)
        self.assertEqual("NAME", data[0].type)
        self.assertEqual(18.0, data[1].value)
        self.assertEqual("MASS", data[1].type)
        self.assertEqual(0, data[2].value)
        self.assertEqual("CHARGE", data[2].type)
        self.assertEqual("W", data[3].value)
        self.assertEqual("SYMBOL", data[3].type)
        self.assertEqual("test_top.itp", data[4].value)
        self.assertEqual("TOPOLOGY", data[4].type)
        self.assertEqual("test_coord.gro", data[5].value)
        self.assertEqual("COORDINATE", data[5].type)
