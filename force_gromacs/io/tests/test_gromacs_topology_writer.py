from unittest import TestCase, mock
import testfixtures

from force_gromacs.io.gromacs_topology_writer import (
    GromacsTopologyWriter
)
from force_gromacs.simulation_builders.gromacs_topology_data import (
    GromacsTopologyData
)

GROMACS_WRITER_OPEN_PATH = (
    "force_gromacs.io.gromacs_topology_writer.open"
)


class TestGromacsTopologyWriter(TestCase):

    def setUp(self):

        topology_data = GromacsTopologyData(
            molecule_files=['test_surf_1.itp', 'test_surf_2.itp',
                            'test_salt.itp', 'test_solv.itp'],
            fragment_ledger={
                'PS': 1200,
                'SS': 480,
                'S': 200,
                'So': 2120
            }
        )
        self.writer = GromacsTopologyWriter(
            topology_data=topology_data,
            sim_name='test_experiment',
            top_name='test_top.itp',
            dry_run=True
        )

    def test__create_simulation_top(self):
        top_file = self.writer._create_simulation_top()

        res = top_file.split('\n')
        self.assertEqual(14, len(res))
        self.assertEqual('#include "test_surf_1.itp"', res[0])
        self.assertEqual('#include "test_surf_2.itp"', res[1])
        self.assertEqual('#include "test_salt.itp"', res[2])
        self.assertEqual('#include "test_solv.itp"', res[3])
        self.assertEqual('[ system ]', res[5])
        self.assertEqual('test_experiment', res[6])
        self.assertEqual('[ molecules ]', res[8])
        self.assertEqual('PS 1200', res[9])
        self.assertEqual('SS 480', res[10])
        self.assertEqual('S 200', res[11])
        self.assertEqual('So 2120', res[12])

    def test_bash_script(self):

        bash_script = self.writer.bash_script()

        res = bash_script.split('\n')
        self.assertEqual(15, len(res))
        self.assertEqual('cat <<EOM > ./test_experiment/test_top.itp',
                         res[0])
        self.assertEqual('#include "test_surf_1.itp"', res[1])
        self.assertEqual('#include "test_surf_2.itp"', res[2])
        self.assertEqual('#include "test_salt.itp"', res[3])
        self.assertEqual('#include "test_solv.itp"', res[4])
        self.assertEqual('[ system ]', res[6])
        self.assertEqual('test_experiment', res[7])
        self.assertEqual('[ molecules ]', res[9])
        self.assertEqual('PS 1200', res[10])
        self.assertEqual('SS 480', res[11])
        self.assertEqual('S 200', res[12])
        self.assertEqual('So 2120', res[13])
        self.assertEqual('EOM', res[14])

    def test_run_exceptions(self):
        mock_open = mock.mock_open()

        with testfixtures.LogCapture():
            with mock.patch(
                    GROMACS_WRITER_OPEN_PATH,
                    mock_open, create=True):
                self.writer.run()
                mock_open.assert_not_called()

            self.writer.dry_run = False
            with mock.patch(
                    GROMACS_WRITER_OPEN_PATH,
                    mock_open, create=True):
                self.writer.run()
                mock_open.assert_called_once()
