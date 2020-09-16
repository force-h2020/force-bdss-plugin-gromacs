#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase, mock

from force_bdss.api import DataValue

from force_gromacs.gromacs_plugin import GromacsPlugin
from force_gromacs.tests.probe_classes.chemicals import (
    ProbeGromacsFragment, data
)

mock_method = ('force_gromacs.io.gromacs_molecule_reader'
               '.GromacsMoleculeReader.read')


class TestMoleculeDataSource(TestCase):

    def setUp(self):

        self.positive_ion = ProbeGromacsFragment(
            name='Positive Ion', symbol='PI')
        self.negative_ion = ProbeGromacsFragment(
            name='Negative Ion', symbol='NI')

        self.input_values = [self.positive_ion,
                             self.negative_ion]

        self.plugin = GromacsPlugin()
        self.factory = self.plugin.data_source_factories[1]
        self.data_source = self.factory.create_data_source()
        self.model = self.factory.create_model()

    def test_basic_function(self):
        self.model.n_fragments = 2
        self.model.fragment_numbers = [1, 1]

        in_slots = self.data_source.slots(self.model)[0]
        self.assertEqual(2, len(in_slots))

        data_values = [
            DataValue(type=slot.type, value=value)
            for slot, value in zip(in_slots, self.input_values)
        ]

        with mock.patch(mock_method) as mockreadtop:
            mockreadtop.return_value = data
            res = self.data_source.run(self.model, data_values)

        self.assertEqual("MOLECULE", res[0].type)

        molecule = res[0].value
        self.assertEqual("Positive Ion Negative Ion",
                         molecule.name)
        self.assertEqual(58, molecule.mass, )
        self.assertEqual(0, molecule.charge)
        self.assertTrue(molecule.neutral)

    def test___make_local_parameter_copy(self):
        parameters = [
            DataValue(type='FRAGMENT', value=value)
            for value in self.input_values
        ]

        with mock.patch(mock_method) as mockreadtop:
            mockreadtop.return_value = data
            self.data_source._make_local_parameter_copy(
                parameters)

        self.assertNotEqual(
            parameters[0].value, self.input_values[0]
        )
        self.assertNotEqual(
            parameters[1].value, self.input_values[1]
        )

    def test__assign_stoichiometry(self):
        self.model.n_fragments = 2
        self.model.fragment_numbers = [2, 3]

        self.data_source._assign_stoichiometry(
            self.model, self.input_values)

        self.assertEqual(2, self.positive_ion.stoichiometry)
        self.assertEqual(3, self.negative_ion.stoichiometry)

    def test_update_fragment_numbers(self):

        self.model.fragment_numbers[0] = 3
        self.model.n_fragments = 5
        in_slots = self.data_source.slots(self.model)[0]
        self.assertEqual(5, len(in_slots))
        self.assertEqual(5, len(self.model.fragment_numbers))
        self.assertEqual(3, self.model.fragment_numbers[0])

        self.model.fragment_numbers[1] = 5
        self.model.n_fragments = 2
        in_slots = self.data_source.slots(self.model)[0]
        self.assertEqual(2, len(in_slots))
        self.assertEqual(2, len(self.model.fragment_numbers))
        self.assertEqual(5, self.model.fragment_numbers[1])

    def test___n_fragments_check(self):
        errors = self.model._n_fragments_check()
        self.assertEqual(0, len(errors))

        self.model.n_fragments = 0
        errors = self.model._n_fragments_check()
        messages = [error.local_error for error in errors]

        self.assertEqual(1, len(errors))
        self.assertIn(
            'Number of molecular fragments must be at least 1',
            messages
        )

    def test_verify(self):

        self.model.n_fragments = 0
        errors = self.model.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(2, len(messages))
        self.assertIn(
            'Number of molecular fragments must be at least 1',
            messages
        )
        self.assertIn(
            "The number of output slots (1 values) returned by 'Gromacs "
            "Molecule' does not match the number of user-defined names "
            "specified (0 values). This is either a plugin error "
            "or a file error.",
            messages
        )

        self.model.n_fragments = 1
        errors = self.model.verify()
        messages = [error.local_error for error in errors]
        self.assertEqual(2, len(messages))
        self.assertIn(
            "The number of input slots (1 values) returned by 'Gromacs "
            "Molecule' does not match the number of user-defined names "
            "specified (0 values). This is either a plugin error "
            "or a file error.",
            messages
        )
        self.assertIn(
            "The number of output slots (1 values) returned by 'Gromacs "
            "Molecule' does not match the number of user-defined names "
            "specified (0 values). This is either a plugin error "
            "or a file error.",
            messages
        )
