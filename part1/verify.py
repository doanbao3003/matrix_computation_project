from __future__ import annotations
from __init__ import Matrix


EPSILON = 1e-9


def _ensure_column_vector(b, expected_rows=None, name='b'):
    if not isinstance(b, Matrix):
        raise TypeError(f"{name} phải là một đối tượng Matrix.")
    if b.cols == 1:
        result = b
    elif b.rows == 1:
        result = b.get_Tran()
    else:
        raise ValueError(f"{name} phải có kích thước n x 1 hoặc 1 x n.")
    if expected_rows is not None and result.rows != expected_rows:
        raise ValueError(f"Số hàng của {name} phải bằng {expected_rows}.")
    return result


def verify_solution(A, x, b, tol=EPSILON):
    """Kiểm chứng nghiệm x của hệ Ax = b."""
    if not isinstance(A, Matrix):
        raise TypeError("A phải là một đối tượng Matrix.")
    x = _ensure_column_vector(x, A.cols, name='x')
    b = _ensure_column_vector(b, A.rows, name='b')

    ax = A * x
    residual_data = []
    max_error = 0.0
    for i in range(A.rows):
        err = ax.data[i][0] - b.data[i][0]
        residual_data.append([err])
        max_error = max(max_error, abs(err))

    return {
        'is_correct': max_error <= tol,
        'Ax': ax,
        'residual': Matrix(residual_data, name='Ax - b'),
        'max_error': max_error,
        'tolerance': tol,
    }
