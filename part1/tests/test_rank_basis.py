
import os
import sys
import unittest

PART1_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PART1_DIR not in sys.path:
    sys.path.insert(0, PART1_DIR)

from __init__ import Matrix
from rank_basis import rank_and_basic


class RankBasisTests(unittest.TestCase):
    def test_rank_and_basis_returns_expected_structure(self):
        A = Matrix([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [1.0, 1.0, 1.0]], "A")

        result = rank_and_basic(A)

        self.assertEqual(result["rank"], 2)
        self.assertEqual(result["row_basis"], [[1.0, 0.0, -1.0], [0.0, 1.0, 2.0]])
        self.assertEqual(result["column_basis"], [[1.0, 2.0, 1.0], [2.0, 4.0, 1.0]])
        self.assertEqual(result["pivot_columns"], [0, 1])
        self.assertEqual(result["rref"].data, [[1.0, 0.0, -1.0], [0.0, 1.0, 2.0], [0.0, 0.0, 0.0]])

    def test_rank_and_basis_for_zero_matrix(self):
        A = Matrix([[0.0, 0.0], [0.0, 0.0]], "Zero")

        result = rank_and_basic(A)

        self.assertEqual(result["rank"], 0)
        self.assertEqual(result["row_basis"], [])
        self.assertEqual(result["column_basis"], [])
        self.assertEqual(result["pivot_columns"], [])


if __name__ == "__main__":
    unittest.main()
