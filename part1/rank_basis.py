from __future__ import annotations
from __init__ import Matrix


from gaussian import gaussian_eliminate_2

EPSILON = 1e-12


def rank_and_basic(A):
    """Trả về cơ sở không gian dòng, cơ sở không gian cột và hạng của ma trận."""
    if not isinstance(A, Matrix):
        raise TypeError("A phải là một đối tượng Matrix.")

    original = Matrix([row[:] for row in A.data], name=A.name)
    rref_A = Matrix([row[:] for row in A.data], name=f"rref({A.name})")
    zero_side = Matrix([[0.0] for _ in range(A.rows)], name='0')
    gaussian_eliminate_2(rref_A, zero_side)

    pivot_cols = []
    for i in range(rref_A.rows):
        pivot_col = None
        for j in range(rref_A.cols):
            if abs(rref_A.data[i][j]) > EPSILON:
                pivot_col = j
                break
        if pivot_col is not None:
            pivot_cols.append(pivot_col)

    row_basis = [row[:] for row in rref_A.data if any(abs(x) > EPSILON for x in row)]
    col_basis = [[original.data[r][c]] for r in range(original.rows) for c in []]
    col_basis = [[original.data[r][c] for r in range(original.rows)] for c in pivot_cols]

    return {
        'rank': len(pivot_cols),
        'row_basis': row_basis,
        'column_basis': col_basis,
        'pivot_columns': pivot_cols,
        'rref': rref_A,
    }


# Alias tên đúng theo mô tả đề bài nếu cần dùng.
rank_and_basis = rank_and_basic
