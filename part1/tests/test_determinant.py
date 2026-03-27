import os
import sys
import unittest

PART1_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PART1_DIR not in sys.path:
    sys.path.insert(0, PART1_DIR)

from __init__ import Matrix
from determinant import determinant


class DeterminantTests(unittest.TestCase):
    def test_determinant_of_square_matrix(self):
        A = Matrix([[1, 2, 3], [0, 4, 5], [1, 0, 6]], "A")

        self.assertAlmostEqual(determinant(A), 22.0)

    def test_determinant_of_singular_matrix(self):
        A = Matrix([[1, 2], [2, 4]], "A")

        self.assertEqual(determinant(A), 0.0)

    def test_non_square_matrix_raises_error(self):
        A = Matrix([[1, 2, 3], [4, 5, 6]], "A")

        with self.assertRaises(ValueError):
            determinant(A)


if __name__ == "__main__":
    unittest.main()
