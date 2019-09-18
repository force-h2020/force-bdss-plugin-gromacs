from unittest import TestCase

import numpy as np


from force_gromacs.utilities import (
    minimum_image, pairwise_difference_matrix, distance_matrix,
    create_molecule_coord
)


class UtilitiesTestCase(TestCase):

    def setUp(self):

        self.mol_ref = ['1PS', '1PS', '2PS', '2PS', '1NA']
        self.coord = np.array([[0, 0, 0],
                               [1, 1, 1],
                               [4, 4, 4],
                               [5, 5, 5],
                               [2, 0, 2]])

        self.cell_dim = np.array([6, 6, 6])

        self.d_matrix = np.asarray([[[0., 0., 0.],
                                   [-1., -1., -1.],
                                   [2., 2., 2.],
                                   [1., 1., 1.],
                                   [-2., 0., -2]],

                                  [[1, 1, 1],
                                   [0., 0., 0.],
                                   [3, 3, 3],
                                   [2, 2, 2],
                                   [-1, 1, -1]],

                                  [[-2, -2, -2],
                                   [-3, -3, -3],
                                   [0., 0., 0.],
                                   [-1, -1, -1.],
                                   [2, -2, 2]],

                                  [[-1, -1, -1],
                                   [-2, -2, -2],
                                   [1, 1, 1],
                                   [0, 0, 0.],
                                   [-3, -1, -3]],

                                  [[2, 0, 2],
                                   [1, -1, 1],
                                   [-2, 2, -2.],
                                   [3, 1, 3.],
                                   [0., 0., 0.]]])

        self.r2_matrix = np.array([[0, 3, 12, 3, 8],
                                   [3, 0, 27, 12, 3],
                                   [12, 27, 0, 3, 12],
                                   [3, 12, 3, 0, 19],
                                   [8, 3, 12, 19, 0]])

    def test_minimum_image(self):

        d_coord = np.array([[[0, 0, 0],
                             [1, 5, 1]],
                            [[-1, -5, -1],
                             [0, 0, 0]]])

        minimum_image(d_coord, self.cell_dim)

        self.assertTrue(np.allclose(
            np.array([[[0, 0, 0],
                       [1, -1, 1]],
                      [[-1, 1, -1],
                       [0, 0, 0]]]), d_coord)
        )

        with self.assertRaises(AssertionError):
            minimum_image(d_coord, self.cell_dim[:2])

    def test_pairwise_difference_matrix(self):

        d_coord = pairwise_difference_matrix(
            self.coord[:3, :1], self.coord[:3, :1])

        self.assertEqual((3, 3, 1), d_coord.shape)
        self.assertTrue(
            np.allclose(d_coord,
                        np.array([[[0], [-1], [-4]],
                                  [[1], [0], [-3]],
                                  [[4], [3], [0]]]))
        )

        d_coord = pairwise_difference_matrix(
            self.coord[:3, :2], self.coord[:3, :2])

        self.assertEqual((3, 3, 2), d_coord.shape)
        self.assertTrue(
            np.allclose(d_coord,
                        np.array([[[0, 0], [-1, -1], [-4, -4]],
                                  [[1, 1], [0, 0], [-3, -3]],
                                  [[4, 4], [3, 3], [0, 0]]]))
        )

        d_coord = pairwise_difference_matrix(
            self.coord[:4, :1], self.coord[:3, :1])

        self.assertEqual((4, 3, 1), d_coord.shape)
        self.assertTrue(
            np.allclose(d_coord,
                        np.array([[[0], [-1], [-4]],
                                  [[1], [0], [-3]],
                                  [[4], [3], [0]],
                                  [[5], [4], [1]]]))
        )

    def test_distance_matrix(self):

        r2_coord, d_coord = distance_matrix(self.coord, self.coord,
                                            self.cell_dim)

        self.assertEqual((5, 5, 3), d_coord.shape)
        self.assertEqual((5, 5), r2_coord.shape)

        self.assertTrue(
            np.allclose(self.d_matrix, d_coord)
        )
        self.assertTrue(
            np.allclose(self.r2_matrix, r2_coord)
        )

        r2_coord = distance_matrix(self.coord, self.coord,
                                   self.cell_dim, distances=False)
        self.assertEqual((5, 5), r2_coord.shape)
        self.assertTrue(
            np.allclose(self.r2_matrix, r2_coord)
        )

        r2_coord = distance_matrix(self.coord, self.coord[:-1],
                                   self.cell_dim, distances=False)

        self.assertEqual((5, 4), r2_coord.shape)
        self.assertTrue(
            np.allclose(self.r2_matrix[:,:-1], r2_coord)
        )

    def test_create_molecule_coord(self):

        coord = self.coord[:-1]
        mol_M = np.array([1, 2, 1, 2])

        molecules = create_molecule_coord(
            coord, 2, mol_M)

        self.assertEqual((2, 3), molecules.shape)
        self.assertTrue(
            np.allclose(np.array([[0.666667, 0.666667, 0.666667],
                                  [4.666667, 4.666667, 4.666667]]),
                        molecules)
        )

        molecules = create_molecule_coord(
            coord, 2, mol_M, mode='sites', com_sites=0)

        self.assertEqual((2, 3), molecules.shape)
        self.assertTrue(
            np.allclose(np.array([[0, 0, 0],
                                  [4, 4, 4]]),
                        molecules)
        )