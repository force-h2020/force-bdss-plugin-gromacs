#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase

import numpy as np

from force_gromacs.tools.distances import (
    minimum_image, pairwise_difference_matrix, distance_matrix,
    batch_distance_matrix, squared_euclidean_distance,
    euclidean_distance
)


class DistancesTestCase(TestCase):

    def setUp(self):

        self.mol_ref = ['1PS', '1PS', '2PS', '2PS', '1NA']
        self.coord = np.array([[0., 0., 0.],
                               [1., 1., 1.],
                               [4., 4., 4.],
                               [5., 5., 5.],
                               [2., 0., 2.]])

        self.cell_dim = np.array([6., 6., 6.])

        self.d_matrix = np.asarray([[[0., 0., 0.],
                                   [-1., -1., -1.],
                                   [2., 2., 2.],
                                   [1., 1., 1.],
                                   [-2., 0., -2]],

                                  [[1, 1, 1],
                                   [0., 0., 0.],
                                   [-3, -3, -3],
                                   [2, 2, 2],
                                   [-1, 1, -1]],

                                  [[-2, -2, -2],
                                   [3, 3, 3],
                                   [0., 0., 0.],
                                   [-1, -1, -1.],
                                   [2, -2, 2]],

                                  [[-1, -1, -1],
                                   [-2, -2, -2],
                                   [1, 1, 1],
                                   [0, 0, 0.],
                                   [3, -1, 3]],

                                  [[2, 0, 2],
                                   [1, -1, 1],
                                   [-2, 2, -2.],
                                   [-3, 1, -3.],
                                   [0., 0., 0.]]])

        self.r2_matrix = np.array([[0, 3, 12, 3, 8],
                                   [3, 0, 27, 12, 3],
                                   [12, 27, 0, 3, 12],
                                   [3, 12, 3, 0, 19],
                                   [8, 3, 12, 19, 0]])

        self.r_matrix = np.sqrt(self.r2_matrix)

    def test_minimum_image(self):

        d_coord = np.array([[[0, 0, 0],
                             [1, 5, 1]],
                            [[-1, -5, -1],
                             [0, 0, 0]]], dtype=float)

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

        d_coord = pairwise_difference_matrix(
            self.coord, self.coord, self.cell_dim)
        self.assertTrue(
            np.allclose(d_coord, self.d_matrix)
        )

    def test_squared_euclidean_distance(self):
        r2_coord = squared_euclidean_distance(
            self.coord, self.coord, pbc_box=self.cell_dim)
        self.assertEqual((5, 5), r2_coord.shape)
        self.assertTrue(
            np.allclose(r2_coord, self.r2_matrix)
        )

        r2_coord = squared_euclidean_distance(
            self.coord, self.coord[:-1], self.cell_dim
        )

        self.assertEqual((5, 4), r2_coord.shape)
        self.assertTrue(
            np.allclose(self.r2_matrix[:, :-1], r2_coord)
        )

    def test_euclidean_distance(self):
        r_coord = euclidean_distance(self.coord, self.coord,
                                     pbc_box=self.cell_dim)

        self.assertTrue(
            np.allclose(r_coord, self.r_matrix)
        )

    def test_distance_matrix(self):

        r_coord = distance_matrix(
            self.coord, self.cell_dim
        )
        self.assertEqual((5, 5), r_coord.shape)
        self.assertTrue(
            np.allclose(self.r_matrix, r_coord)
        )

        r2_coord = distance_matrix(
            self.coord, self.cell_dim, metric='sqeuclidean')
        self.assertEqual((5, 5), r2_coord.shape)
        self.assertTrue(
            np.allclose(self.r2_matrix, r2_coord)
        )

        d_coord = distance_matrix(
            self.coord, self.cell_dim, metric='vector')
        self.assertEqual((5, 5, 3), d_coord.shape)
        self.assertTrue(
            np.allclose(self.d_matrix, d_coord)
        )

        with self.assertRaises(AssertionError):
            distance_matrix(
                self.coord, self.cell_dim, metric='hamming')

    def test_batch_distance_matrix(self):
        r_coord = batch_distance_matrix(
            self.coord, self.cell_dim
        )
        self.assertEqual((5, 5), r_coord.shape)
        self.assertTrue(
            np.allclose(self.r_matrix, r_coord)
        )

        r2_coord = batch_distance_matrix(
            self.coord, self.cell_dim, metric='sqeuclidean',
            batch_size=2)
        self.assertEqual((5, 5), r2_coord.shape)
        self.assertTrue(
            np.allclose(self.r2_matrix, r2_coord)
        )

        d_coord = batch_distance_matrix(
            self.coord, self.cell_dim, metric='vector',
            batch_size=2)
        self.assertEqual((5, 5, 3), d_coord.shape)
        self.assertTrue(
            np.allclose(self.d_matrix, d_coord)
        )

        with self.assertRaises(AssertionError):
            batch_distance_matrix(
                self.coord, self.cell_dim, metric='hamming')
