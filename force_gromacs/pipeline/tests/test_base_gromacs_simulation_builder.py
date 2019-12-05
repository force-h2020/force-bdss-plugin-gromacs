from unittest import TestCase

from force_gromacs.pipeline.base_gromacs_simulation_builder import (
    BaseGromacsSimulationBuilder
)
from force_gromacs.pipeline.gromacs_pipeline import GromacsPipeline


class TestGromacsSimulationBuilder(TestCase):

    def setUp(self):

        name = 'test_experiment'
        size = 100
        martini_parameters = 'test_martini.itp'

        self.sim_builder = BaseGromacsSimulationBuilder(
            name=name,
            size=size,
            martini_parameters=martini_parameters
        )

    def test__init__(self):

        self.assertEqual('test_experiment', self.sim_builder.name)
        self.assertEqual(100, self.sim_builder.size)
        self.assertEqual('.', self.sim_builder.directory)
        self.assertEqual(
            'test_martini.itp', self.sim_builder.martini_parameters
        )
        self.assertFalse(self.sim_builder.mpi_run)
        self.assertEqual(1, self.sim_builder.n_proc)
        self.assertTrue(self.sim_builder.dry_run)

        self.assertEqual(
            'test_experiment_coord.gro', self.sim_builder._coord_file
        )
        self.assertEqual(
            'test_experiment_topol.tpr', self.sim_builder._binary_file
        )
        self.assertEqual(
            'test_experiment_topol.top', self.sim_builder._top_file
        )
        self.assertEqual(
            'test_experiment_ener.edr', self.sim_builder._energy_file
        )
        self.assertEqual(
            'test_experiment_traj', self.sim_builder._traj_file
        )
        self.assertEqual(
            'test_experiment_md.log', self.sim_builder._log_file
        )
        self.assertEqual(
            'test_experiment_state.cpt', self.sim_builder._state_file
        )

        self.assertIsInstance(
            self.sim_builder.pipeline, GromacsPipeline
        )
        self.assertEqual(
            self.sim_builder.dry_run, self.sim_builder.pipeline.dry_run
        )

        self.assertEqual(
            {'topologies': [],
             'fragment_dict': {}},
            self.sim_builder.topology_data
        )

    def test__update_topology_data(self):

        self.sim_builder._update_topology_data('some_top.itp', 'Mol', 10)
        self.assertEqual(
            ['some_top.itp'], self.sim_builder.topology_data['topologies']
        )
        self.assertEqual(
            {'Mol': 10}, self.sim_builder.topology_data['fragment_dict']
        )

        self.sim_builder._update_topology_data('some_other_top.itp', 'At', 10)
        self.assertEqual(
            ['some_top.itp',
             'some_other_top.itp'],
            self.sim_builder.topology_data['topologies']
        )
        self.assertEqual(
            {'Mol': 10,
             'At': 10}, self.sim_builder.topology_data['fragment_dict']
        )

        self.sim_builder._update_topology_data('and_another_top.itp')
        self.assertEqual(
            ['some_top.itp',
             'some_other_top.itp',
             'and_another_top.itp'],
            self.sim_builder.topology_data['topologies']
        )
        self.assertEqual(
            {'Mol': 10,
             'At': 10}, self.sim_builder.topology_data['fragment_dict']
        )

        self.sim_builder._update_topology_data(symbol='Mol', n_mol=100)
        self.assertEqual(
            ['some_top.itp',
             'some_other_top.itp',
             'and_another_top.itp'],
            self.sim_builder.topology_data['topologies']
        )
        self.assertEqual(
            {'Mol': 110,
             'At': 10}, self.sim_builder.topology_data['fragment_dict']
        )

    def test_not_implemented_methods(self):

        with self.assertRaises(NotImplementedError):
            self.sim_builder.build_pipeline()

        with self.assertRaises(NotImplementedError):
            self.sim_builder.get_results_path()
