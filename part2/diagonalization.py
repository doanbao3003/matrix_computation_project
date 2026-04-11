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
    Input: A (matrix dạng list 2D)
    Output: A^T (list 2D)

    Dùng NumPy để tăng tốc cho ma trận lớn.
    """
    return np.asarray(A, dtype=float).T.tolist()


def matmul(A, B):
    """
    Input: A, B (matrix dạng list 2D)
    Output: A * B (list 2D)

    Dùng NumPy @ operator (BLAS) thay vì 3 vòng lặp Python.
    Tốc độ: ~1000x nhanh hơn cho n=500.
    """
    return (np.asarray(A, dtype=float) @ np.asarray(B, dtype=float)).tolist()


def compute_ata(A):
    """
    Input: A (list 2D)
    Output: A^T A (list 2D)

    Dùng NumPy: A_np.T @ A_np — một lệnh duy nhất, chạy ở C level.
    """
    A_np = np.asarray(A, dtype=float)
    return (A_np.T @ A_np).tolist()


def eigen_decomposition(A):
    """
    Input: A (matrix vuông, thường là A^T A — ma trận đối xứng)
    Output:
        eigenvalues: list[float]  (sắp xếp giảm dần)
        eigenvectors: matrix (các vector cột, tương ứng eigenvalues)

    Dùng np.linalg.eigh thay vì eig vì:
        - A^T A luôn đối xứng → eigh là đúng và nhanh hơn
        - eigh luôn trả về eigenvalues thực (real), tránh lỗi complex
        - eig có thể trả complex do sai số floating-point → lỗi so sánh '<'
    """
    A_np = np.array(A, dtype=float)

    # eigh trả eigenvalues tăng dần → đảo lại để giảm dần (chuẩn SVD)
    eigenvalues, eigenvectors = np.linalg.eigh(A_np)

    # Đảo thứ tự: giảm dần theo eigenvalue
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

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