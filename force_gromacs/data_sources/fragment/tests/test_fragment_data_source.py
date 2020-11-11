#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase
from tempfile import NamedTemporaryFile

from force_gromacs.data_sources.fragment.fragment_factory import (
    FragmentFactory)
from force_gromacs.data_sources.fragment.fragment_data_source import (
    MissingFragmentException
)
from force_gromacs.tests.fixtures import (
    gromacs_molecule_file, gromacs_coordinate_file
)


class TestFragmentDataSource(TestCase):

    def setUp(self):
        self.factory = FragmentFactory(
            plugin={'id': '0', 'name': 'test'})
        self.data_source = self.factory.create_data_source()
        self.model = self.factory.create_model()

    def test_basic_function(self):

        self.model.name = "Solvent"
        self.model.symbol = "So"
        self.model.topology = gromacs_molecule_file
        self.model.coordinate = gromacs_coordinate_file

        res = self.data_source.run(self.model, [])
        self.assertEqual("FRAGMENT", res[0].type)

        fragment = res[0].value
        self.assertEqual("Solvent", fragment.name)
        self.assertEqual("So", fragment.symbol)
        self.assertEqual(["O", "H1", "H2"], fragment.atoms, )
        self.assertEqual(18.0, fragment.mass, )
        self.assertEqual(0, fragment.charge)
        self.assertEqual(gromacs_molecule_file, fragment.topology)
        self.assertEqual(gromacs_coordinate_file, fragment.coordinate)

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
            "The number of output slots (1 values) returned by"
            " 'Gromacs Molecular Fragment' does not match the "
            "number of user-defined names specified (0 values). "
            "This is either a plugin error or a file error.",
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

        with NamedTemporaryFile() as tmp_file:
            self.model.topology = gromacs_molecule_file
            self.model.coordinate = tmp_file.name
            errors = self.model.verify()
            messages = [error.local_error for error in errors]
            self.assertEqual(2, len(messages))
            self.assertNotIn(
                'Gromacs file name is white space.',
                messages
            )

        self.model.coordinate = gromacs_coordinate_file
        errors = self.model.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(1, len(messages))
        self.assertNotIn(
            'File extension does not match required.',
            messages
        )
