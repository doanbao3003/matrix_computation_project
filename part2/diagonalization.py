"""
File: diagonalization.py
Người làm: Khánh Trần

Nhiệm vụ:
- Tính eigenvalues và eigenvectors
- Phục vụ cho SVD (trên A^T A)
"""

import os
import sys
import math

# ---------------------------------------------------------------------------
# Import Matrix từ Part 1 để tái sử dụng transpose (get_Tran) và matmul (__mul__)
# ---------------------------------------------------------------------------
_current_dir = os.path.dirname(os.path.abspath(__file__))
_part1_dir = os.path.join(os.path.dirname(_current_dir), "part1")
if _part1_dir not in sys.path:
    sys.path.insert(0, _part1_dir)

from matrix import Matrix


def transpose(A):
    """
    Chuyển vị ma trận.
    Tái sử dụng Matrix.get_Tran() từ Part 1 (matrix.py).

    Input: A (list 2D)
    Output: A^T (list 2D)
    """
    mat = Matrix([row[:] for row in A], "tmp")
    return mat.get_Tran().data


def matmul(A, B):
    """
    Nhân 2 ma trận.
    Tái sử dụng Matrix.__mul__() từ Part 1 (matrix.py).

    Input: A, B (list 2D)
    Output: A × B (list 2D)
    """
    mat_a = Matrix(A, "A")
    mat_b = Matrix(B, "B")
    return (mat_a * mat_b).data


def compute_ata(A):
    """
    Input: A (list 2D)
    Output: A^T A (list 2D)
    """
    AT = transpose(A)
    return matmul(AT, A)


def eigen_decomposition(A):
    """
    Tính eigenvalues và eigenvectors cho ma trận đối xứng (A^T A).
    Sử dụng thuật toán Jacobi (pure Python, không phụ thuộc numpy).

    Thuật toán Jacobi:
        Lặp lại phép xoay Givens trên từng cặp (p, q) ngoài đường chéo
        để triệt tiêu phần tử S[p][q] cho đến khi S gần đường chéo.

        Mỗi phép xoay:  S' = J^T · S · J
        với J là ma trận xoay cos/sin tại vị trí (p, q).

    Input: A (matrix vuông đối xứng, thường là A^T A)
    Output:
        eigenvalues: list[float]  (sắp xếp giảm dần)
        eigenvectors: list[list[float]] (các vector cột, tương ứng eigenvalues)
    """
    n = len(A)

    # Copy ma trận để không ảnh hưởng dữ liệu gốc
    S = [row[:] for row in A]

    # Ma trận eigenvectors — khởi tạo = ma trận đơn vị I
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    max_sweeps = 100
    tol = 1e-12

    for _ in range(max_sweeps):
        # Tính tổng bình phương các phần tử ngoài đường chéo (trên tam giác trên)
        off_norm = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                off_norm += S[i][j] ** 2

        # Nếu đủ nhỏ → ma trận đã gần đường chéo → hội tụ
        if off_norm < tol:
            break

        # Duyệt qua tất cả cặp (p, q) — cyclic sweep
        for p in range(n):
            for q in range(p + 1, n):
                # Bỏ qua nếu phần tử đã đủ nhỏ
                if abs(S[p][q]) < tol / n:
                    continue

                # Tính góc xoay theta
                if abs(S[p][p] - S[q][q]) < 1e-15:
                    theta = math.pi / 4.0
                else:
                    theta = 0.5 * math.atan2(2.0 * S[p][q], S[p][p] - S[q][q])

                c = math.cos(theta)
                s = math.sin(theta)

                # Lưu giá trị cũ trên đường chéo và vị trí (p,q)
                spp = S[p][p]
                sqq = S[q][q]
                spq = S[p][q]

                # Áp dụng phép xoay Jacobi: S' = J^T · S · J
                # Cập nhật hàng/cột i (i ≠ p, q)
                for i in range(n):
                    if i != p and i != q:
                        sip = S[i][p]
                        siq = S[i][q]
                        S[i][p] = c * sip + s * siq
                        S[p][i] = S[i][p]   # đối xứng
                        S[i][q] = -s * sip + c * siq
                        S[q][i] = S[i][q]   # đối xứng

                # Cập nhật phần tử đường chéo
                S[p][p] = c * c * spp + 2 * s * c * spq + s * s * sqq
                S[q][q] = s * s * spp - 2 * s * c * spq + c * c * sqq

                # Triệt tiêu phần tử ngoài đường chéo (mục đích chính)
                S[p][q] = 0.0
                S[q][p] = 0.0

                # Cập nhật eigenvectors: V' = V · J
                for i in range(n):
                    vip = V[i][p]
                    viq = V[i][q]
                    V[i][p] = c * vip + s * viq
                    V[i][q] = -s * vip + c * viq

    # Eigenvalues = đường chéo của S sau khi hội tụ
    eigenvalues = [S[i][i] for i in range(n)]

    # Sắp xếp giảm dần theo eigenvalue
    indices = sorted(range(n), key=lambda i: eigenvalues[i], reverse=True)
    sorted_eigenvalues = [eigenvalues[i] for i in indices]

    # Sắp xếp lại eigenvectors theo thứ tự mới
    sorted_V = [[V[row][indices[col]] for col in range(n)] for row in range(n)]

    return sorted_eigenvalues, sorted_V


def sort_eigenpairs(eigenvalues, eigenvectors):
    """
    Sort eigenvalues giảm dần và reorder eigenvectors
    """
    # Tạo list (eigenvalue, eigenvector)
    pairs = list(zip(eigenvalues, zip(*eigenvectors)))
    # zip(*eigenvectors) để lấy vector theo cột

    # Sort giảm dần theo eigenvalue
    pairs.sort(key=lambda x: x[0], reverse=True)

    # Tách lại
    sorted_values = [pair[0] for pair in pairs]
    sorted_vectors = list(zip(*[pair[1] for pair in pairs]))

    # Convert tuple → list
    sorted_vectors = [list(row) for row in sorted_vectors]

    return sorted_values, sorted_vectors


def build_diagonal(eigenvalues):
    """
    Input: eigenvalues
    Output: ma trận đường chéo D
    """
    n = len(eigenvalues)

    D = [[0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        D[i][i] = eigenvalues[i]

    return D