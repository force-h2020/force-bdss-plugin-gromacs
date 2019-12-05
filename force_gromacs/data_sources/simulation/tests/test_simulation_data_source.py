from unittest import TestCase, mock

from traits.testing.unittest_tools import UnittestTools

from force_bdss.api import DataValue

from force_gromacs.tests.probe_classes import (
    ProbeSimulationBuilder, ProbeMolecule, ProbeGromacsPipeline
)
from force_gromacs.gromacs_plugin import GromacsPlugin


SIMULATION_DATASOURCE_PATH = ('force_gromacs.data_sources.simulation'
                              '.simulation_data_source.SimulationDataSource')
SIMULATION_BUILDER_PATH = (f"{SIMULATION_DATASOURCE_PATH}"
                           '.create_simulation_builder')


class TestSimulationDataSource(TestCase, UnittestTools):

    def setUp(self):
        self.plugin = GromacsPlugin()
        self.factory = self.plugin.data_source_factories[2]
        self.data_source = self.factory.create_data_source()

        #: Example input values
        self.size = 4000
        self.name = 'test_experiment'
        self.martini_parameters = 'test_martini.itp'
        self.md_min_parameters = 'test_min_parm.mdp'
        self.md_prod_parameters = 'test_prod_parm.mdp'

        self.model = self.factory.create_model()
        self.model.n_molecule_types = 2
        self.model.martini_parameters = self.martini_parameters
        self.model.md_prod_parameters = self.md_prod_parameters
        self.model.md_min_parameters = self.md_min_parameters
        self.model.size = self.size
        self.model.name = self.name

        self.water = ProbeMolecule('Water')
        self.salt = ProbeMolecule('Salt')
        self.input_values = [[self.water, self.salt]]

    def test_basic_function(self):

        in_slots = self.data_source.slots(self.model)[0]
        self.assertEqual(2, len(in_slots))

        data_values = [
            DataValue(type=slot.type, value=value)
            for slot, value in zip(in_slots, self.input_values)
        ]

        with mock.patch(SIMULATION_BUILDER_PATH) as mock_sim:
            mock_sim.return_value = ProbeSimulationBuilder()
            with mock.patch('os.path.exists') as mock_exists:
                mock_exists.return_value = True
                with self.assertTraitChanges(
                        self.model, 'driver_event', count=0):
                    self.data_source.run(self.model, data_values)
                self.model.ow_data = True
                with self.assertTraitChanges(
                        self.model, 'driver_event', count=1):
                    res = self.data_source.run(self.model, data_values)

        self.assertEqual(1, len(res))
        self.assertEqual('/path/to/trajectory.gro', res[0].value)

    def test__check_perform_simulation(self):

        with mock.patch('os.path.exists') as mock_exists:
            self.model.ow_data = True
            mock_exists.return_value = True
            self.assertTrue(
                self.data_source._check_perform_simulation(
                    self.model, '/some/path'))

            mock_exists.return_value = False
            self.assertTrue(
                self.data_source._check_perform_simulation(
                    self.model, '/some/path'))

            self.model.ow_data = False
            self.assertTrue(
                self.data_source._check_perform_simulation(
                    self.model, '/some/path'))

            mock_exists.return_value = True
            self.assertFalse(
                self.data_source._check_perform_simulation(
                    self.model, '/some/path'))

    def test_slots(self):

        self.model.n_molecule_types = 4
        in_slots = self.data_source.slots(self.model)[0]
        self.assertEqual(4, len(in_slots))

    def test__n_molecule_types_check(self):

        model = self.factory.create_model()
        model.n_molecule_types = 0
        errors = model.verify()

        messages = [error.local_error for error in errors]
        self.assertIn(
            "Number of molecule types must be at least 1",
            messages
        )

    def test_not_implemented_error(self):

        with self.assertRaises(NotImplementedError):
            self.data_source.create_simulation_builder(None, None)

    def test_create_bash_script(self):

        name = 'test_experiment'
        pipeline = ProbeGromacsPipeline()

        bash_script = self.data_source.create_bash_script(
            pipeline, name
        )

        commands = bash_script.split('\n')

        self.assertEqual(17, len(commands))
        self.assertEqual(
            '# test_experiment', commands[0]
        )

    def test_notify_bash_script(self):

        bash_script = ('# experiment_5.0\n'
                       'mdrun -s test_topol.tpr\n')

        with self.assertTraitChanges(
                self.model, 'driver_event', count=1):
            self.data_source.notify_bash_script(
                self.model, bash_script
            )

    def test_driver_event(self):

        in_slots = self.data_source.slots(self.model)[0]

        data_values = [
            DataValue(type=slot.type, value=value)
            for slot, value in zip(in_slots, self.input_values)
        ]

        with mock.patch('force_gromacs.data_sources.simulation'
                        '.simulation_data_source.SimulationDataSource'
                        '.create_simulation_builder') as mocksim:
            mocksim.return_value = ProbeSimulationBuilder()
            self.data_source.run(self.model, data_values)

        bash_script = self.model.driver_event.bash_script.value

        commands = bash_script.split('\n')
        self.assertEqual(17, len(commands))
