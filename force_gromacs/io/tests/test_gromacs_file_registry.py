from unittest import TestCase

from force_gromacs.io.gromacs_file_registry import GromacsFileRegistry


class TestFileRegistry(TestCase):

    def setUp(self):

        self.file_registry = GromacsFileRegistry(
            prefix='some-file-name'
        )

    def test_file_names(self):

        self.assertEqual(
            'some-file-name_coord.gro',
            self.file_registry.coord_file
        )
        self.assertEqual(
            'some-file-name_topol.tpr',
            self.file_registry.binary_file
        )
        self.assertEqual(
            'some-file-name_topol.top',
            self.file_registry.top_file
        )
        self.assertEqual(
            'some-file-name_ener.edr',
            self.file_registry.energy_file
        )
        self.assertEqual(
            'some-file-name_traj.trr',
            self.file_registry.traj_file
        )
        self.assertEqual(
            'some-file-name_traj.xtc',
            self.file_registry.comp_traj_file
        )
        self.assertEqual(
            'some-file-name_md.log',
            self.file_registry.log_file
        )
        self.assertEqual(
            'some-file-name_state.cpt',
            self.file_registry.state_file
        )
