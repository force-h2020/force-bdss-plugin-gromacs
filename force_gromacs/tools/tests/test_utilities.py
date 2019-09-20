from unittest import TestCase

import numpy as np
from scipy.spatial.distance import cdist

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

    def test_batch_process(self):
        r_matrix = batch_process(
            self.matrix, self.matrix, cdist, size=2
        )

        self.assertEqual((4, 4), r_matrix.shape)
        self.assertTrue(
            np.allclose(
                cdist(self.matrix, self.matrix),
                r_matrix
            )
        )

        r_matrix = batch_process(
            self.matrix, self.matrix, cdist, size=3
        )

        self.assertEqual((4, 4), r_matrix.shape)
        self.assertTrue(
            np.allclose(
                cdist(self.matrix, self.matrix),
                r_matrix
            )
        )

        r_matrix = batch_process(
            self.matrix, self.matrix, cdist, n_batch=2
        )

        self.assertEqual((4, 4), r_matrix.shape)
        self.assertTrue(
            np.allclose(
                cdist(self.matrix, self.matrix),
                r_matrix
            )
        )

        with self.assertRaises(AssertionError):
            batch_process(
                self.matrix, self.matrix, cdist
            )
