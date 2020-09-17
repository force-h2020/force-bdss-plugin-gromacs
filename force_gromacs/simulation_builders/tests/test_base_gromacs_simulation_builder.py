#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

import os
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
        self.assertEqual(os.path.curdir, self.sim_builder.directory)
        self.assertEqual(
            os.path.join(os.path.curdir, 'test_experiment'),
            self.sim_builder.folder)
        self.assertEqual(
            'test_martini.itp', self.sim_builder.martini_parameters
        )
        self.assertFalse(self.sim_builder.mpi_run)
        self.assertEqual(1, self.sim_builder.n_proc)
        self.assertTrue(self.sim_builder.dry_run)

        self.assertEqual(
            'test_experiment_coord.gro',
            self.sim_builder.file_registry.coord_file
        )
        self.assertEqual(
            'test_experiment_topol.tpr',
            self.sim_builder.file_registry.binary_file
        )
        self.assertEqual(
            'test_experiment_topol.top',
            self.sim_builder.file_registry.top_file
        )
        self.assertEqual(
            'test_experiment_ener.edr',
            self.sim_builder.file_registry.energy_file
        )
        self.assertEqual(
            'test_experiment_traj.trr',
            self.sim_builder.file_registry.traj_file
        )
        self.assertEqual(
            'test_experiment_md.log',
            self.sim_builder.file_registry.log_file
        )
        self.assertEqual(
            'test_experiment_state.cpt',
            self.sim_builder.file_registry.state_file
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
