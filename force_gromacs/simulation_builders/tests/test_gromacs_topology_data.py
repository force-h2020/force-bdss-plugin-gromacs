from unittest import TestCase, mock

from force_gromacs.simulation_builders.gromacs_topology_data import (
    GromacsTopologyData
)
from force_gromacs.io.tests.test_gromacs_topology_reader import (
    FILE_READER_OPEN_PATH, top_file
)


class TestGromacsTopologyData(TestCase):

    def setUp(self):

        self.topology_data = GromacsTopologyData()

    def test__init__(self):

        self.assertListEqual([], self.topology_data.molecule_files)
        self.assertDictEqual({}, self.topology_data.fragment_ledger)

    def test_add_fragment(self):

        self.topology_data.add_fragment('PI')
        self.assertDictEqual({'PI': 0}, self.topology_data.fragment_ledger)

        # Don't add duplicate items
        self.topology_data.add_fragment('PI')
        self.assertDictEqual({'PI': 0}, self.topology_data.fragment_ledger)

        self.topology_data.add_fragment('NI', 10)
        self.assertDictEqual(
            {'PI': 0, 'NI': 10},
            self.topology_data.fragment_ledger)

    def test_remove_fragment(self):

        self.topology_data.fragment_ledger = {'PI': 10}

        self.topology_data.remove_fragment('PI')
        self.assertDictEqual({}, self.topology_data.fragment_ledger)

        # Don't fail if fragment is not present
        self.topology_data.remove_fragment('PI')
        self.assertDictEqual({}, self.topology_data.fragment_ledger)

    def test_edit_fragment(self):

        self.topology_data.fragment_ledger = {'PI': 10}

        self.topology_data.edit_fragment_number('PI', 5)
        self.assertDictEqual({'PI': 15}, self.topology_data.fragment_ledger)

        self.topology_data.edit_fragment_number('PI', -15)
        self.assertDictEqual({}, self.topology_data.fragment_ledger)

    def test_add_topology_file(self):

        self.topology_data.add_molecule_file('some_top.itp')
        self.assertListEqual(['some_top.itp'], self.topology_data.molecule_files)

        # Don't add duplicate items
        self.topology_data.add_molecule_file('some_top.itp')
        self.assertListEqual(['some_top.itp'], self.topology_data.molecule_files)

    def test_remove_topology_files(self):

        self.topology_data.molecule_files = ['some_top.itp']

        self.topology_data.remove_molecule_file('some_top.itp')
        self.assertListEqual([], self.topology_data.molecule_files)

        # Don't fail if topology is not present
        self.topology_data.remove_molecule_file('some_top.itp')
        self.assertListEqual([], self.topology_data.molecule_files)

    def test_verify(self):

        self.topology_data.fragment_ledger = {'I': 10}
        self.assertFalse(self.topology_data.verify())

        self.topology_data.molecule_files = ['some_top.itp']
        self.assertFalse(self.topology_data.verify())

        mock_open = mock.mock_open(read_data=" ")
        with mock.patch(FILE_READER_OPEN_PATH, mock_open,
                        create=True):
            self.assertFalse(self.topology_data.verify())

        mock_open = mock.mock_open(read_data=top_file)
        with mock.patch(FILE_READER_OPEN_PATH, mock_open,
                        create=True):
            self.assertTrue(self.topology_data.verify())
