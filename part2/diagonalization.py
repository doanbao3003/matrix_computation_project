"""
File: diagonalization.py
Người làm: Khánh Trần

Nhiệm vụ:
- Tính eigenvalues và eigenvectors
- Phục vụ cho SVD (trên A^T A)
"""


def transpose(A):
    """
    Input: A (matrix)
    Output: A^T

    TODO:
    - Viết hàm chuyển vị ma trận
    """
    pass


def matmul(A, B):
    """
    Input: A, B (matrix)
    Output: A * B

    TODO:
    - Viết phép nhân ma trận
    """
    pass


def compute_ata(A):
    """
    Input: A
    Output: A^T A

    TODO:
    - Dùng transpose + matmul
    """
    pass


def eigen_decomposition(A):
    """
    Input: A (matrix vuông, thường là A^T A)
    Output:
        eigenvalues: list[float]
        eigenvectors: matrix (các vector cột)

    TODO:
    - Có thể dùng numpy để lấy eigenvalues/eigenvectors
    - Convert về list nếu cần
    - Đảm bảo output đúng format

    Lưu ý:
    - Đây là hàm CHÍNH mà decomposition.py sẽ gọi
    """
    pass


def sort_eigenpairs(eigenvalues, eigenvectors):
    """
    Input:
        eigenvalues
        eigenvectors
    Output:
        eigenvalues, eigenvectors (đã sort giảm dần)

    TODO:
    - Sort theo eigenvalues giảm dần
    - reorder eigenvectors tương ứng
    """
    pass


def build_diagonal(eigenvalues):
    """
    Input: eigenvalues
    Output: ma trận đường chéo D

    TODO:
    - D[i][i] = eigenvalues[i]
    """
    pass
