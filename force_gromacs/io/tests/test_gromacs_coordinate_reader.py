from unittest import TestCase

import numpy as np

from force_gromacs.io.gromacs_coordinate_reader import (
    GromacsCoordinateReader
)
from force_gromacs.tests.fixtures import gromacs_coordinate_file


class TestGromacsCoordinateReader(TestCase):

    def setUp(self):

        self.coord = np.array([
            [0.546, 0.326, 0.070],
            [0.285, 0.135, 0.310],
            [0.212, 0.178, 0.770],
            [0.166, 0.422, 1.173],
            [1.638, 0.315, 1.042],
            [1.680, 0.707, 1.028]])
        self.coord = np.stack((self.coord, self.coord))

        self.dim = np.array([[4.36258, 4.36258, 4.36258],
                             [4.36258, 4.36258, 4.36258]])

        self.reader = GromacsCoordinateReader()

    def test_basic_function(self):

        data = self.reader.read(gromacs_coordinate_file)

        self.assertEqual(4, len(data))
        self.assertIn('mol_ref', data.keys())
        self.assertIn('atom_ref', data.keys())
        self.assertIn('coord', data.keys())
        self.assertIn('dim', data.keys())

        self.assertIsInstance(data['mol_ref'], list)
        self.assertIsInstance(data['atom_ref'], list)
        self.assertIsInstance(data['coord'], np.ndarray)
        self.assertIsInstance(data['dim'], np.ndarray)

        self.assertEqual(6, len(data['mol_ref']))
        self.assertEqual(6, len(data['atom_ref']))
        self.assertEqual((2, 6, 3), data['coord'].shape)
        self.assertEqual((2, 3,), data['dim'].shape)

        data = self.reader.read(gromacs_coordinate_file, 1)

        self.assertEqual(6, len(data['mol_ref']))
        self.assertEqual(6, len(data['atom_ref']))
        self.assertEqual((1, 6, 3), data['coord'].shape)
        self.assertEqual((1, 3,), data['dim'].shape)
        self.assertTrue(np.allclose(self.coord[:1], data['coord']))
        self.assertTrue(np.allclose(self.dim[:1], data['dim']))

        data = self.reader.read(gromacs_coordinate_file, symbols=['PS1', 'SS'])

        self.assertEqual(4, len(data['mol_ref']))
        self.assertEqual(4, len(data['atom_ref']))
        self.assertEqual((2, 4, 3), data['coord'].shape)
        self.assertEqual((2, 3,), data['dim'].shape)

    def test__get_data(self):
        file_lines = self.reader._read_file(gromacs_coordinate_file)

        mol_ref, atom_ref, coord, dim = self.reader._get_data(file_lines)

        self.assertEqual(6, len(mol_ref))
        self.assertEqual(6, len(atom_ref))
        self.assertEqual((2, 6, 3), coord.shape)
        self.assertEqual((2, 3,), dim.shape)

        self.assertListEqual(
            ['1PS1', '1PS1', '2SS', '2SS', '3PI', '4NI'],
            mol_ref
        )
        self.assertListEqual(
            ['PS11', 'PS12', 'SS1', 'SS2', 'PI', 'NI'],
            atom_ref
        )

        self.assertTrue(np.allclose(self.coord, coord))
        self.assertTrue(np.allclose(self.dim, dim))

        mol_ref, atom_ref, coord, dim = self.reader._get_data(file_lines, 1)

        self.assertEqual(6, len(mol_ref))
        self.assertEqual(6, len(atom_ref))
        self.assertEqual((1, 6, 3), coord.shape)
        self.assertEqual((1, 3,), dim.shape)

    def test__remove_index(self):
        string = '424ght6aos57'
        self.assertEqual('ght6aos57',
                         self.reader._remove_index(string))

    def test_extract_molecules(self):

        data = {'mol_ref': ['1PS1', '1PS1', '2SS', '2SS', '3PI', '4NI']}

        indices = self.reader.extract_molecules(data, 'PS1')
        self.assertListEqual([0, 1], indices)

        indices = self.reader.extract_molecules(data, ['PS1'])
        self.assertListEqual([0, 1], indices)

        indices = self.reader.extract_molecules(data, ['PS1', 'SS'])
        self.assertListEqual([0, 1, 2, 3], indices)

        indices = self.reader.extract_molecules(data, ['S'])
        self.assertListEqual([], indices)

    def test_check_file_types(self):

        coordinate = 'some_file.go'

        with self.assertRaises(IOError):
            self.reader._check_file_types(coordinate)

    def test_file_opening_exception_handling(self):

        with self.assertRaises(IOError):
            self.reader.read('this_file_should_not_exist.gro')
