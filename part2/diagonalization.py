"""
File: diagonalization.py
Người làm: Khánh Trần

Nhiệm vụ:
- Tính eigenvalues và eigenvectors
- Phục vụ cho SVD (trên A^T A)
"""

import numpy as np


def transpose(A):
    """
    Input: A (matrix)
    Output: A^T
    """
    rows = len(A)
    cols = len(A[0])

    AT = [[0 for _ in range(rows)] for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            AT[j][i] = A[i][j]

    return AT


def matmul(A, B):
    """
    Input: A, B (matrix)
    Output: A * B
    """
    n = len(A)
    m = len(A[0])
    p = len(B[0])

    # Khởi tạo ma trận kết quả
    C = [[0 for _ in range(p)] for _ in range(n)]

    for i in range(n):
        for j in range(p):
            for k in range(m):
                C[i][j] += A[i][k] * B[k][j]

    return C


def compute_ata(A):
    """
    Input: A
    Output: A^T A
    """
    AT = transpose(A)
    return matmul(AT, A)


def eigen_decomposition(A):
    """
    Input: A (matrix vuông, thường là A^T A)
    Output:
        eigenvalues: list[float]
        eigenvectors: matrix (các vector cột)
    """
    A_np = np.array(A, dtype=float)

    eigenvalues, eigenvectors = np.linalg.eig(A_np)

    # Convert về list
    eigenvalues = eigenvalues.tolist()
    eigenvectors = eigenvectors.tolist()

    return eigenvalues, eigenvectors


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