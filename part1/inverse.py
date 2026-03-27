from __future__ import annotations
from __init__ import Matrix


from gaussian import gaussian_eliminate_2
from determinant import determinant

EPSILON = 1e-12


def Inverse(A):
    """Tính ma trận nghịch đảo bằng Gauss-Jordan trên [A | I]."""
    if not isinstance(A, Matrix):
        raise TypeError("A phải là một đối tượng Matrix.")
    if A.rows != A.cols:
        raise ValueError("Chỉ có thể tìm nghịch đảo của ma trận vuông.")
    if abs(determinant(A)) < EPSILON:
        raise ValueError("Ma trận suy biến nên không có nghịch đảo.")

    left = Matrix([row[:] for row in A.data], name=f"copy({A.name})")
    n = A.rows
    identity = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    right = Matrix(identity, name=f"I_{n}")

    gaussian_eliminate_2(left, right)
    return right
