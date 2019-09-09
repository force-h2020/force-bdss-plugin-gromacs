from unittest import TestCase, mock

from force_bdss.api import DataValue

from force_gromacs.data_sources.molecule import Molecule
from force_gromacs.gromacs_plugin import GromacsPlugin
from force_gromacs.tests.probe_classes import (
    ProbeFragment, data, mock_method
)


class TestMolecule(TestCase):

    def setUp(self):
        self.water = ProbeFragment()
        self.positive_ion = ProbeFragment(
            name='Positive Ion', symbol='PI')
        self.negative_ion = ProbeFragment(
            name='Negative Ion', symbol='NI')

        self.molecule = Molecule(
            fragments=[self.water]
        )

    def test___init__(self):
        self.assertEqual('Water', self.molecule.name)
        self.assertEqual(1, len(self.molecule.fragments))
        self.assertEqual(18, self.molecule.mass)
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


class TestMoleculeDataSource(TestCase):

    def setUp(self):

        self.positive_ion = ProbeFragment(
            name='Positive Ion', symbol='PI')
        self.negative_ion = ProbeFragment(
            name='Negative Ion', symbol='NI')

        self.input_values = [self.positive_ion,
                             self.negative_ion]

        self.plugin = GromacsPlugin()
        self.factory = self.plugin.data_source_factories[1]
        self.data_source = self.factory.create_data_source()

    def test_basic_function(self):
        model = self.factory.create_model()
        model.n_fragments = 2
        model.fragment_numbers = [1, 1]

        in_slots = self.data_source.slots(model)[0]
        self.assertEqual(2, len(in_slots))

        data_values = [
            DataValue(type=slot.type, value=value)
            for slot, value in zip(in_slots, self.input_values)
        ]

        with mock.patch(mock_method) as mockreadtop:
            mockreadtop.return_value = data
            res = self.data_source.run(model, data_values)

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
        model = self.factory.create_model()
        model.n_fragments = 2
        model.fragment_numbers = [2, 3]

        parameters = [
            DataValue(type='FRAGMENT', value=value)
            for value in self.input_values
        ]
        parameters += [DataValue(type='NOTHING', value=0)]

        self.data_source._assign_stoichiometry(model, parameters)

        self.assertEqual(2, self.positive_ion.number)
        self.assertEqual(3, self.negative_ion.number)

    def test_update_fragment_numbers(self):

        model = self.factory.create_model()

        model.fragment_numbers[0] = 3
        model.n_fragments = 5
        in_slots = self.data_source.slots(model)[0]
        self.assertEqual(5, len(in_slots))
        self.assertEqual(5, len(model.fragment_numbers))
        self.assertEqual(3, model.fragment_numbers[0])

        model.fragment_numbers[1] = 5
        model.n_fragments = 2
        in_slots = self.data_source.slots(model)[0]
        self.assertEqual(2, len(in_slots))
        self.assertEqual(2, len(model.fragment_numbers))
        self.assertEqual(5, model.fragment_numbers[1])
