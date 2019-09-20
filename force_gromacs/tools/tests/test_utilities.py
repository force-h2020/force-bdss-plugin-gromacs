from unittest import TestCase

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

    def test_batch_process(self):

        dot_matrix = batch_process(
            self.matrix, self.matrix, np.dot, size=2
        )

        self.assertEqual((4, 4), dot_matrix.shape)
        self.assertTrue(
            np.allclose(
                np.dot(self.matrix, self.matrix),
                dot_matrix
            )
        )

        dot_matrix = batch_process(
            self.matrix, self.matrix, np.dot, size=3
        )

        self.assertEqual((4, 4), dot_matrix.shape)
        self.assertTrue(
            np.allclose(
                np.dot(self.matrix, self.matrix),
                dot_matrix
            )
        )

        dot_matrix = batch_process(
            self.matrix, self.matrix, np.dot, n_batch=2
        )

        self.assertEqual((4, 4), dot_matrix.shape)
        self.assertTrue(
            np.allclose(
                np.dot(self.matrix, self.matrix),
                dot_matrix
            )
        )

        with self.assertRaises(AssertionError):
            batch_process(
                self.matrix, self.matrix, 2, size=2
            )

        with self.assertRaises(AssertionError):
            batch_process(
                self.matrix, self.matrix, np.dot
            )

        with self.assertRaises(AssertionError):
            batch_process(
                self.matrix[0], self.matrix[1], np.dot,
                size=2
            )
