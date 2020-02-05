from unittest import TestCase

from force_gromacs.simulation_builders.base_gromacs_simulation_builder import (
    BaseGromacsSimulationBuilder
)
from force_gromacs.simulation_builders.gromacs_topology_data import (
    GromacsTopologyData
)
from force_gromacs.pipelines.gromacs_pipeline import GromacsPipeline


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
            'test_experiment_coord.gro', self.sim_builder.coord_file
        )
        self.assertEqual(
            'test_experiment_topol.tpr', self.sim_builder.binary_file
        )
        self.assertEqual(
            'test_experiment_topol.top', self.sim_builder.top_file
        )
        self.assertEqual(
            'test_experiment_ener.edr', self.sim_builder.energy_file
        )
        self.assertEqual(
            'test_experiment_traj', self.sim_builder.traj_file
        )
        self.assertEqual(
            'test_experiment_md.log', self.sim_builder.log_file
        )
        self.assertEqual(
            'test_experiment_state.cpt', self.sim_builder.state_file
        )

        self.assertIsInstance(
            self.sim_builder._pipeline, GromacsPipeline
        )
        self.assertEqual(
            self.sim_builder.dry_run, self.sim_builder._pipeline.dry_run
        )
        self.assertIsInstance(
            self.sim_builder.topology_data, GromacsTopologyData
        )

    def test_not_implemented_methods(self):

        with self.assertRaises(NotImplementedError):
            self.sim_builder.build_pipeline()

        with self.assertRaises(NotImplementedError):
            self.sim_builder.get_results_path()
