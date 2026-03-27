
import os
import sys
import unittest

PART1_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PART1_DIR not in sys.path:
    sys.path.insert(0, PART1_DIR)

from __init__ import Matrix
from gaussian import back_substitution, gaussian_eliminate, gaussian_eliminate_2


class GaussianTests(unittest.TestCase):
    def test_gaussian_eliminate_and_back_substitution(self):
        A = Matrix([[2.0, 1.0], [4.0, -6.0]], "A")
        b = Matrix([[5.0], [-2.0]], "b")

        gaussian_eliminate(A, b)
        solution = back_substitution(A, b)

        self.assertEqual(solution.data, [[1.75], [1.5]])

    def test_gaussian_eliminate_accepts_row_vector_b(self):
        A = Matrix([[1.0, 1.0], [1.0, -1.0]], "A")
        b = Matrix([[4.0, 0.0]], "b_row")

        _, transformed_b = gaussian_eliminate(A, b)
        solution = back_substitution(A, transformed_b)

        self.assertEqual(transformed_b.rows, 2)
        self.assertEqual(transformed_b.cols, 1)
        self.assertEqual(solution.data, [[2.0], [2.0]])

    def test_gaussian_eliminate_2_returns_rref_and_rhs(self):
        A = Matrix([[1.0, 2.0, 1.0], [2.0, 4.0, 0.0]], "A")
        b = Matrix([[3.0], [6.0]], "b")

        reduced_A, reduced_b = gaussian_eliminate_2(A, b)

        self.assertIs(reduced_A, A)
        self.assertIs(reduced_b, b)
        self.assertEqual(A.data, [[1.0, 2.0, 0.0], [0.0, 0.0, 1.0]])
        self.assertEqual(b.data, [[3.0], [0.0]])


if __name__ == "__main__":
    unittest.main()
