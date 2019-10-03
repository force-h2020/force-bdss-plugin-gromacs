from unittest import TestCase, mock

import testfixtures

from force_gromacs.io.gromacs_topology_reader import (
    GromacsTopologyReader
)

FILE_READER_OPEN_PATH = (
    "force_gromacs.io.base_file_reader.open"
)

top_file = """;Solvent
             [moleculetype]
             ;
             So 1
             [atoms]
             ;
             1 T 1 So So 1 0 18.0
             ; Ion
             [ moleculetype ]
             ;
             I 1
             [ atoms ]
             ;
             1 F 1 I I 1 1.0 24"""


class TestGromacsTopologyReader(TestCase):

    def setUp(self):

        self.reader = GromacsTopologyReader()

    def test_basic_function(self):
        mock_open = mock.mock_open(read_data=top_file)

        with mock.patch(FILE_READER_OPEN_PATH, mock_open,
                        create=True):

            data = self.reader.read('test_top.itp')

            self.assertEqual(2, len(data))
            self.assertIn('So', data.keys())
            self.assertIn('I', data.keys())

            self.assertEqual(['So'], data['So']['atoms'])
            self.assertEqual(['I'], data['I']['atoms'])

            self.assertEqual([18.0], data['So']['masses'])
            self.assertEqual([24], data['I']['masses'])

            self.assertEqual([0], data['So']['charges'])
            self.assertEqual([1], data['I']['charges'])

    def test__remove_comments(self):
        top_lines = top_file.split('\n')

        cleaned_lines = self.reader._remove_comments(top_lines)

        self.assertEqual(8, len(cleaned_lines))
        self.assertEqual('[moleculetype]', cleaned_lines[0])
        self.assertEqual('So 1', cleaned_lines[1])
        self.assertEqual('[atoms]', cleaned_lines[2])
        self.assertEqual('1 T 1 So So 1 0 18.0', cleaned_lines[3])
        self.assertEqual('[ moleculetype ]', cleaned_lines[4])
        self.assertEqual('I 1', cleaned_lines[5])
        self.assertEqual('[ atoms ]', cleaned_lines[6])
        self.assertEqual('1 F 1 I I 1 1.0 24', cleaned_lines[7])

    def test__get_molecule_sections(self):
        cleaned_lines = [
            '[moleculetype]', 'So 1', '[atoms]',
            '1 T 1 So So 1 0 18.0',
            '[ moleculetype ]', 'I 1', '[ atoms ]',
            '1 F 1 I I 1 1.0 24'
        ]

        mol_sections = self.reader._get_molecule_sections(cleaned_lines)

        self.assertEqual(2, len(mol_sections))
        self.assertListEqual(
            ['[moleculetype]', 'So 1', '[atoms]',
             '1 T 1 So So 1 0 18.0'], mol_sections[0])
        self.assertListEqual(
            ['[ moleculetype ]', 'I 1', '[ atoms ]',
             '1 F 1 I I 1 1.0 24'], mol_sections[1])

        with self.assertRaisesRegex(
                RuntimeError,
                'Gromacs topology file does not include any'
                ' molecule types'):
            self.reader._get_molecule_sections([])

    def test__get_data(self):
        cleaned_lines = [
            '[moleculetype]', 'So 1', '[atoms]',
            '1 T 1 So So 1 0 18.0',
            '[ moleculetype ]', 'I 1', '[ atoms ]',
            '1 F 1 I I 1 1.0 24'
        ]

        (symbols, atoms,
         charges, masses) = self.reader._get_data(cleaned_lines)

        self.assertEqual(2, len(symbols))
        self.assertEqual(2, len(atoms))
        self.assertEqual(2, len(charges))
        self.assertEqual(2, len(masses))

        self.assertListEqual(['So', 'I'], symbols)
        self.assertListEqual([['So'], ['I']], atoms)
        self.assertListEqual([[0], [1]], charges)
        self.assertListEqual([[18.0], [24]], masses)

    def test_check_file_types(self):

        topology = 'some_file.isp'
        coordinate = 'some_file.xc'

        with self.assertRaises(IOError):
            self.reader._check_file_types(topology)

        with self.assertRaises(IOError):
            self.reader._check_file_types(coordinate)

    def test_file_opening_exception_handling(self):

        with testfixtures.LogCapture() as capture:
            with self.assertRaises(IOError):
                self.reader.read(
                    'this_file_should_not_exist.itp'
                )
            capture.check(
                ('force_gromacs.io.gromacs_topology_reader',
                 'ERROR',
                 'unable to open "this_file_should_not_exist.itp"')
            )

        mock_open = mock.mock_open(read_data=" ")
        with mock.patch(
                    FILE_READER_OPEN_PATH, mock_open,
                    create=True),\
                testfixtures.LogCapture() as capture:
            with self.assertRaises(RuntimeError):
                self.reader.read(
                    'this_file_is_empty.itp'
                )
            capture.check(
                ('force_gromacs.io.gromacs_topology_reader',
                 'ERROR',
                 'unable to load data from "this_file_is_empty.itp"')
            )
