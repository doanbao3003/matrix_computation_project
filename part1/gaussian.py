from __future__ import annotations
from __init__ import Matrix


EPSILON = 1e-12


def _matrix_copy(M):
    return Matrix([row[:] for row in M.data], getattr(M, 'name', 'Unknown'))


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


def gaussian_eliminate(A, b):
    """Đưa A về dạng bậc thang (REF) bằng khử Gauss có partial pivoting.

    Hàm cập nhật trực tiếp cả A và b theo đúng các phép biến đổi sơ cấp hàng.
    """
    if not isinstance(A, Matrix):
        raise TypeError("A phải là một đối tượng Matrix.")
    b = _ensure_column_vector(b, A.rows)

    pivot_row = 0
    for pivot_col in range(A.cols):
        if pivot_row >= A.rows:
            break

        max_row = max(range(pivot_row, A.rows), key=lambda r: abs(A.data[r][pivot_col]))
        if abs(A.data[max_row][pivot_col]) < EPSILON:
            continue

        if max_row != pivot_row:
            A.swap_rows(max_row, pivot_row)
            b.swap_rows(max_row, pivot_row)

        for r in range(pivot_row + 1, A.rows):
            if abs(A.data[r][pivot_col]) < EPSILON:
                continue
            factor = A.data[r][pivot_col] / A.data[pivot_row][pivot_col]
            A.add_multiple_of_row(r, pivot_row, -factor)
            b.add_multiple_of_row(r, pivot_row, -factor)
            if abs(A.data[r][pivot_col]) < EPSILON:
                A.data[r][pivot_col] = 0.0

        pivot_row += 1

    return A, b


def back_substitution(A, b):
    """Giải hệ tam giác trên Ax=b sau khi đã khử Gauss."""
    if not isinstance(A, Matrix):
        raise TypeError("A phải là một đối tượng Matrix.")
    if A.rows != A.cols:
        raise ValueError("A phải là ma trận vuông để giải bằng thế lùi.")

    b = _ensure_column_vector(b, A.rows)
    n = A.rows
    x = [[0.0] for _ in range(n)]

    for i in range(n - 1, -1, -1):
        pivot = A.data[i][i]
        rhs = b.data[i][0] - sum(A.data[i][j] * x[j][0] for j in range(i + 1, n))

        if abs(pivot) < EPSILON:
            if abs(rhs) < EPSILON:
                raise ValueError("Hệ có vô số nghiệm; không thể dùng thế lùi để tìm nghiệm duy nhất.")
            raise ValueError("Hệ vô nghiệm hoặc ma trận suy biến.")

        x[i][0] = rhs / pivot

    return Matrix(x, name='x')



def gaussian_eliminate_2(A, b):
    """Đưa A về dạng chuẩn tắc hàng (RREF) bằng Gauss-Jordan có partial pivoting."""
    if not isinstance(A, Matrix):
        raise TypeError("A phải là một đối tượng Matrix.")
    if not isinstance(b, Matrix):
        raise TypeError("b phải là một đối tượng Matrix.")
    if b.rows != A.rows:
        raise ValueError("Số hàng của b phải bằng số hàng của A.")

    pivot_row = 0
    for pivot_col in range(A.cols):
        if pivot_row >= A.rows:
            break

        max_row = max(range(pivot_row, A.rows), key=lambda r: abs(A.data[r][pivot_col]))
        if abs(A.data[max_row][pivot_col]) < EPSILON:
            continue

        if max_row != pivot_row:
            A.swap_rows(max_row, pivot_row)
            b.swap_rows(max_row, pivot_row)

        pivot = A.data[pivot_row][pivot_col]
        A.multiply_row_with_real_number(pivot_row, 1.0 / pivot)
        b.multiply_row_with_real_number(pivot_row, 1.0 / pivot)

        for r in range(A.rows):
            if r == pivot_row or abs(A.data[r][pivot_col]) < EPSILON:
                continue
            factor = A.data[r][pivot_col]
            A.add_multiple_of_row(r, pivot_row, -factor)
            b.add_multiple_of_row(r, pivot_row, -factor)
            A.data[r][pivot_col] = 0.0

        A.data[pivot_row][pivot_col] = 1.0
        pivot_row += 1

    return A, b
