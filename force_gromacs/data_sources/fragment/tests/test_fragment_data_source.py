from unittest import mock, TestCase

from force_gromacs.gromacs_plugin import GromacsPlugin


class TestFragmentDataSource(TestCase):

    def setUp(self):
        self.plugin = GromacsPlugin()
        self.factory = self.plugin.data_source_factories[0]
        self.data_source = self.factory.create_data_source()
        self.model = self.factory.create_model()

    def test_basic_function(self):

        self.model.name = "Water"
        self.model.symbol = "W"
        self.model.topology = "test_top.itp"
        self.model.coordinate = "test_coord.gro"

        data_values = []
        top_lines = ['; Water \n', '[moleculetype]\n', ';\n',
                     ' W 1\n', '\n' '[ atoms]\n', ';\n',
                     '1 P 1 W W 1 0 18.0 \n', '\n']
        mock_method = (
            "force_gromacs.io.gromacs_topology_reader"
            ".GromacsTopologyReader._read_file")

        with mock.patch(mock_method) as mockreadtop:
            mockreadtop.return_value = top_lines

            res = self.data_source.run(self.model, data_values)
            self.assertEqual("FRAGMENT", res[0].type)

            fragment = res[0].value
            self.assertEqual("Water", fragment.name)
            self.assertEqual("W", fragment.symbol)
            self.assertEqual(["W"], fragment.atoms, )
            self.assertEqual(18.0, fragment.mass, )
            self.assertEqual(0, fragment.charge)
            self.assertEqual("test_top.itp", fragment.topology)
            self.assertEqual("test_coord.gro", fragment.coordinate)

    def test___file_check(self):

        errors = self.model._file_check(' ', 'ext')
        messages = [error.local_error for error in errors]
        self.assertEqual(2, len(messages))
        self.assertIn(
            'Gromacs file name is white space.',
            messages
        )
        self.assertIn(
            'File extension does not match required.',
            messages
        )

        errors = self.model._file_check(' ')
        messages = [error.local_error for error in errors]
        self.assertEqual(1, len(messages))
        self.assertIn(
            'Gromacs file name is white space.',
            messages
        )

        errors = self.model._file_check(
            'some_invalid_ext.tps', 'ext'
        )
        messages = [error.local_error for error in errors]
        self.assertEqual(1, len(messages))
        self.assertIn(
            'File extension does not match required.',
            messages
        )

    def test_model_verify(self):

        self.model = self.factory.create_model()
        errors = self.model.verify()

        messages = [error.local_error for error in errors]
        self.assertEqual(5, len(messages))
        self.assertIn(
            'The number of output slots is incorrect.',
            messages
        )
        self.assertIn(
            'Gromacs file name is white space.',
            messages
        )
        self.assertIn(
            'File extension does not match required.',
            messages
        )

        self.model.topology = "test_top.itp"
        self.model.coordinate = "test_coord.go"
        errors = self.model.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(2, len(messages))
        self.assertIn(
            'The number of output slots is incorrect.',
            messages
        )
        self.assertIn(
            'File extension does not match required.',
            messages
        )

        self.model.coordinate = "test_coord.gro"
        errors = self.model.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(1, len(messages))
        self.assertIn(
            'The number of output slots is incorrect.',
            messages
        )
