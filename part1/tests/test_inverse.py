
import os
import sys
import unittest

PART1_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PART1_DIR not in sys.path:
    sys.path.insert(0, PART1_DIR)

from __init__ import Matrix
from inverse import Inverse


class InverseTests(unittest.TestCase):
    def test_inverse_of_invertible_matrix(self):
        A = Matrix([[1.0, 2.0], [3.0, 4.0]], "A")

        inverse_matrix = Inverse(A)

        expected = [[-2.0, 1.0], [1.5, -0.5]]
        for i in range(2):
            for j in range(2):
                self.assertAlmostEqual(inverse_matrix.data[i][j], expected[i][j])

    def test_inverse_of_singular_matrix_raises_error(self):
        A = Matrix([[1.0, 2.0], [2.0, 4.0]], "A")

        with self.assertRaises(ValueError):
            Inverse(A)

    def test_inverse_of_non_square_matrix_raises_error(self):
        A = Matrix([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], "A")

        with self.assertRaises(ValueError):
            Inverse(A)


if __name__ == "__main__":
    unittest.main()
