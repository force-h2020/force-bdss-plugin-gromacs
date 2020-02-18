from unittest import TestCase, mock

import testfixtures

from force_gromacs.io.gromacs_molecule_reader import (
    GromacsMoleculeReader
)
from force_gromacs.tests.fixtures import gromacs_molecule_file

FILE_READER_OPEN_PATH = (
    "force_gromacs.io.base_file_reader.open"
)

top_file = """;Solvent
             [moleculetype]
             ;
             So 1
             [atoms]
             ;
             1 T 1 So So 1 0 18.0 ; extra info
             ; Ion
             [ moleculetype ]
             ;
             I 1
             [ atoms ]
             ;
             1 F 1 I I 1 1.0 24"""


class TestGromacsMoelculeReader(TestCase):

    def setUp(self):

        self.reader = GromacsMoleculeReader()
        self.cleaned_lines = [
            '[moleculetype]', 'So 1', '[atoms]',
            '1 T 1 So So 1 0 18.0',
            '[ moleculetype ]', 'I 1', '[ atoms ]',
            '1 F 1 I I 1 1.0 24'
        ]

    def test_read(self):

        fragments = self.reader.read(gromacs_molecule_file)

        self.assertEqual(2, len(fragments))
        self.assertListEqual(
            ['So', 'I'],
            [fragment.symbol for fragment in fragments]
        )

        self.assertEqual(['O', 'H1', 'H2'], fragments[0].atoms)
        self.assertEqual(['I'], fragments[1].atoms)

        self.assertEqual(20, fragments[0].mass)
        self.assertEqual(24, fragments[1].mass)

        self.assertEqual(0, fragments[0].charge)
        self.assertEqual(1, fragments[1].charge)

        self.assertEqual(gromacs_molecule_file, fragments[0].topology)
        self.assertEqual(gromacs_molecule_file, fragments[1].topology)

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

        mol_sections = self.reader._get_molecule_sections(
            self.cleaned_lines)

        self.assertEqual(2, len(mol_sections))
        self.assertListEqual(
            ['[moleculetype]', 'So 1', '[atoms]',
             '1 T 1 So So 1 0 18.0'], mol_sections[0])
        self.assertListEqual(
            ['[ moleculetype ]', 'I 1', '[ atoms ]',
             '1 F 1 I I 1 1.0 24'], mol_sections[1])

        with self.assertRaisesRegex(
                IOError,
                'Gromacs topology file does not include any'
                ' molecule types'):
            self.reader._get_molecule_sections([])

    def test__get_data(self):

        fragments = self.reader._get_data(
            self.cleaned_lines)

        self.assertEqual(2, len(fragments))

        self.assertEqual(
            ['So'],
            [particle.id for particle in fragments[0].particles]
        )
        self.assertEqual(
            ['I'],
            [particle.id for particle in fragments[1].particles]
        )

        self.assertEqual(
            [0],
            [particle.charge for particle in fragments[0].particles]
        )
        self.assertEqual(
            [1],
            [particle.charge for particle in fragments[1].particles]
        )

        self.assertEqual(
            [18],
            [particle.mass for particle in fragments[0].particles]
        )
        self.assertEqual(
            [24],
            [particle.mass for particle in fragments[1].particles]
        )

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
                ('force_gromacs.io.gromacs_molecule_reader',
                 'ERROR',
                 'unable to open "this_file_should_not_exist.itp"')
            )

        mock_open = mock.mock_open(read_data=" ")
        with mock.patch(
                    FILE_READER_OPEN_PATH, mock_open,
                    create=True),\
                testfixtures.LogCapture() as capture:
            with self.assertRaises(IOError):
                self.reader.read(
                    'this_file_is_empty.itp'
                )
            capture.check(
                ('force_gromacs.io.gromacs_molecule_reader',
                 'ERROR',
                 'unable to load data from "this_file_is_empty.itp"')
            )
