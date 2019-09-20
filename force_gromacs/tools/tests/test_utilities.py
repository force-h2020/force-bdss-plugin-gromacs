from unittest import TestCase

from scipy.spatial.distance import cdist
import numpy as np

from force_gromacs.tools.utilities import (
    batch_process
)


class UtilitiesTestCase(TestCase):

    def setUp(self):
        self.array = np.array([0, 0, 4, 4, 5, 6, 1, 1])

        self.matrix = np.array([[0, 0, 4, 0],
                                [4, 0, 6, 1],
                                [1, 1, 0, 0],
                                [0, 0, 0, 0]])

        self.r2_matrix = np.array([[0., 21., 18., 16.],
                                   [21.,  0., 47., 53.],
                                   [18., 47.,  0.,  2.],
                                   [16., 53.,  2.,  0.]])

        self.r_matrix = np.sqrt(self.r2_matrix)

    def test_batch_process(self):

        r_matrix = batch_process(
            self.matrix, self.matrix, cdist
        )

        self.assertEqual((4, 4), r_matrix.shape)
        self.assertTrue(
            np.allclose(
                self.r_matrix,
                r_matrix
            )
        )

        r_matrix = batch_process(
            self.matrix, self.matrix, cdist, batch_size=3
        )

        self.assertEqual((4, 4), r_matrix.shape)
        self.assertTrue(
            np.allclose(
                self.r_matrix,
                r_matrix
            )
        )

        r_matrix = batch_process(
            self.matrix, self.matrix, cdist, batch_size=2,
            shape=(4, 4)
        )

        self.assertEqual((4, 4), r_matrix.shape)
        self.assertTrue(
            np.allclose(
                self.r_matrix,
                r_matrix
            )
        )

        with self.assertRaises(AssertionError):
            batch_process(
                self.matrix, self.matrix, 2
            )

        with self.assertRaises(AssertionError):
            batch_process(
                self.matrix[0], self.matrix[1], cdist,
                batch_size=2
            )
