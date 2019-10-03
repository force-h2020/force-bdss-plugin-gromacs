from unittest import TestCase

import numpy as np

from force_gromacs.tools.positions import (
    molecular_positions
)


class PositionsTestCase(TestCase):

    def setUp(self):

        self.simple_coord = np.array([[0, 0, 0],
                                      [1, 1, 1],
                                      [4, 4, 4],
                                      [5, 5, 5],
                                      [2, 0, 2]])
        self.simple_masses = np.array([1, 2, 1, 2])

        self.large_coord = np.array(
            [[2.741, 7.518, 3.306], [3.075, 7.604, 3.104],
             [3.410, 7.690, 2.901], [3.744, 7.775, 2.699],
             [2.516, 0.583, 1.985], [2.551, 0.953, 2.135],
             [2.586, 1.322, 2.285], [2.621, 1.691, 2.435],
             [6.715, 2.014, 3.789], [6.999, 1.741, 3.721],
             [7.283, 1.467, 3.654], [7.567, 1.194, 3.587]])
        self.large_masses = np.array(
            [10, 5, 5, 5, 10, 5, 5, 5, 10, 5, 5, 5]
        )

    def test_simple_molecular_positions(self):

        coord = self.simple_coord[:-1]

        molecules = molecular_positions(
            coord, 2, self.simple_masses)

        self.assertEqual((2, 3), molecules.shape)
        self.assertTrue(
            np.allclose(np.array([[0.666667, 0.666667, 0.666667],
                                  [4.666667, 4.666667, 4.666667]]),
                        molecules)
        )

        molecules = molecular_positions(
            coord, 2, self.simple_masses, mode='sites',
            com_sites=0)

        self.assertEqual((2, 3), molecules.shape)
        self.assertTrue(
            np.allclose(np.array([[0, 0, 0],
                                  [4, 4, 4]]),
                        molecules)
        )

    def test_invalid_mode(self):

        with self.assertRaisesRegex(
                AssertionError,
                "Argument mode==invalid must be either"
                " 'molecule' or 'sites'"):
            molecular_positions(
                self.simple_coord, 2, self.simple_masses,
                mode='invalid')

    def test_invalid_com_sites(self):

        with self.assertRaisesRegex(
                AssertionError,
                "Argument com_sites must have a length "
                r"\(3\) less than n_sites \(2\)"):
            molecular_positions(
                self.simple_coord, 2, self.simple_masses,
                mode='sites', com_sites=[0, 1, 2])
