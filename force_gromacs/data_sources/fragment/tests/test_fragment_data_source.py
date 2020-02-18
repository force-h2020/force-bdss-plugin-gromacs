from unittest import TestCase

from force_gromacs.gromacs_plugin import GromacsPlugin
from force_gromacs.data_sources.fragment.fragment_data_source import (
    MissingFragmentException
)
from force_gromacs.tests.fixtures import (
    gromacs_molecule_file
)


class TestFragmentDataSource(TestCase):

    def setUp(self):
        self.plugin = GromacsPlugin()
        self.factory = self.plugin.data_source_factories[0]
        self.data_source = self.factory.create_data_source()
        self.model = self.factory.create_model()

    def test_basic_function(self):

        self.model.name = "Solvent"
        self.model.symbol = "So"
        self.model.topology = gromacs_molecule_file
        self.model.coordinate = "test_coord.gro"

        res = self.data_source.run(self.model, [])
        self.assertEqual("FRAGMENT", res[0].type)

        fragment = res[0].value
        self.assertEqual("Solvent", fragment.name)
        self.assertEqual("So", fragment.symbol)
        self.assertEqual(["O", "H1", "H2"], fragment.atoms, )
        self.assertEqual(18.0, fragment.mass, )
        self.assertEqual(0, fragment.charge)
        self.assertEqual(gromacs_molecule_file, fragment.topology)
        self.assertEqual("test_coord.gro", fragment.coordinate)

    def test_missing_fragment_error(self):

        self.model.symbol = "NotThere"
        self.model.topology = gromacs_molecule_file

        with self.assertRaises(MissingFragmentException):
            self.data_source.run(self.model, [])

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
