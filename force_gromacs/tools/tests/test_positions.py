from unittest import TestCase

import numpy as np

from force_gromacs.tools.positions import (
    molecular_positions
)


class PositionsTestCase(TestCase):

    def setUp(self):

        self.mol_ref = ['1PS', '1PS', '2PS', '2PS', '1NA']
        self.coord = np.array([[0, 0, 0],
                               [1, 1, 1],
                               [4, 4, 4],
                               [5, 5, 5],
                               [2, 0, 2]])

    def test_create_molecule_coord(self):

        coord = self.coord[:-1]
        mol_M = np.array([1, 2, 1, 2])

        molecules = molecular_positions(
            coord, 2, mol_M)

        self.assertEqual((2, 3), molecules.shape)
        self.assertTrue(
            np.allclose(np.array([[0.666667, 0.666667, 0.666667],
                                  [4.666667, 4.666667, 4.666667]]),
                        molecules)
        )

        molecules = molecular_positions(
            coord, 2, mol_M, mode='sites', com_sites=0)

        self.assertEqual((2, 3), molecules.shape)
        self.assertTrue(
            np.allclose(np.array([[0, 0, 0],
                                  [4, 4, 4]]),
                        molecules)
        )
