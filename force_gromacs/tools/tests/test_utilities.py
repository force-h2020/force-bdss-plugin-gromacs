#  (C) Copyright 2010-2020 Enthought, Inc., Austin, TX
#  All rights reserved.

from unittest import TestCase

import numpy as np

from force_gromacs.tools.utilities import (
    batch_pairwise
)


def probe_function(a, b):

    matrix = np.zeros((a.shape[0],
                       b.shape[0]))

    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            matrix[i][j] = sum(ai + bj)

    return matrix


class UtilitiesTestCase(TestCase):

    def setUp(self):
        self.array = np.array([0, 0, 4, 4, 5, 6, 1, 1])

        self.matrix = np.array([[0, 0, 4, 0],
                                [4, 0, 6, 1],
                                [1, 1, 0, 0],
                                [0, 0, 0, 0]])

        self.test_matrix = np.array([[8, 15, 6, 4],
                                     [15, 22, 13, 11],
                                     [6, 13, 4, 2],
                                     [4, 11, 2, 0]])

    def test_batch_pairwise(self):

        test_matrix = batch_pairwise(
            self.matrix, self.matrix, probe_function
        )
        self.assertEqual((4, 4), test_matrix.shape)
        self.assertTrue(
            np.allclose(
                self.test_matrix,
                test_matrix
            )
        )

        test_matrix = batch_pairwise(
            self.matrix, self.matrix, probe_function,
            batch_size=3
        )
        self.assertEqual((4, 4), test_matrix.shape)
        self.assertTrue(
            np.allclose(
                self.test_matrix,
                test_matrix
            )
        )

        test_matrix = batch_pairwise(
            self.matrix, self.matrix, probe_function,
            batch_size=2, shape=(4, 4)
        )
        self.assertEqual((4, 4), test_matrix.shape)
        self.assertTrue(
            np.allclose(
                self.test_matrix,
                test_matrix
            )
        )

        with self.assertRaises(AssertionError):
            batch_pairwise(
                self.matrix, self.matrix, 2
            )

        with self.assertRaises(AssertionError):
            batch_pairwise(
                self.matrix[0], self.matrix[1],
                probe_function, batch_size=2
            )
