from __future__ import annotations
from __init__ import Matrix


EPSILON = 1e-12


def determinant(A):
    """Tính định thức bằng khử Gauss có partial pivoting."""
    if not isinstance(A, Matrix):
        raise TypeError("A phải là một đối tượng Matrix.")
    if A.rows != A.cols:
        raise ValueError("Chỉ tính định thức cho ma trận vuông.")

    temp = Matrix([row[:] for row in A.data], name=f"copy({A.name})")
    n = temp.rows
    swap_count = 0
    det = 1.0

    for pivot_col in range(n):
        max_row = max(range(pivot_col, n), key=lambda r: abs(temp.data[r][pivot_col]))
        if abs(temp.data[max_row][pivot_col]) < EPSILON:
            return 0.0

        if max_row != pivot_col:
            temp.swap_rows(max_row, pivot_col)
            swap_count += 1

        pivot = temp.data[pivot_col][pivot_col]
        det *= pivot

        for r in range(pivot_col + 1, n):
            if abs(temp.data[r][pivot_col]) < EPSILON:
                continue
            factor = temp.data[r][pivot_col] / pivot
            temp.add_multiple_of_row(r, pivot_col, -factor)
            temp.data[r][pivot_col] = 0.0

    if swap_count % 2 == 1:
        det = -det
    return det
