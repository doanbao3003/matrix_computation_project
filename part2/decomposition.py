"""
File: decomposition.py
Người làm: Huỳnh Chí Thoại

Nhiệm vụ:
- Xây dựng SVD từ eigen decomposition
- Gọi eigen từ diagonalization.py
"""

from diagonalization import eigen_decomposition, compute_ata


def sqrt_list(values):
    """
    Input: list các số
    Output: list căn bậc hai

    TODO:
    - xử lý sqrt
    - nếu giá trị âm rất nhỏ → coi như 0
    """
    pass


def build_sigma(singular_values, m, n):
    """
    Input:
        singular_values
        m, n (shape của A)
    Output:
        Sigma (matrix m x n)

    TODO:
    - tạo ma trận 0
    - điền singular_values vào đường chéo
    """
    pass


def transpose(A):
    """
    TODO:
    - copy lại hoặc import từ file kia (nhưng KHÔNG phụ thuộc quá nhiều)
    """
    pass


def matmul(A, B):
    """
    TODO:
    - nhân ma trận
    """
    pass


def inverse_diagonal(Sigma):
    """
    Input: Sigma (matrix đường chéo)
    Output: Sigma^-1

    TODO:
    - chỉ đảo các phần tử trên đường chéo
    """
    pass


def normalize_columns(U):
    """
    Input: U (matrix)
    Output: U đã chuẩn hóa cột

    TODO:
    - mỗi vector cột có norm = 1
    """
    pass


def compute_U(A, V, Sigma):
    """
    Input:
        A
        V (eigenvectors)
        Sigma
    Output:
        U

    TODO:
    - U = A * V * Sigma^-1
    - normalize U
    """
    pass


def svd(A):
    """
    Input: A (matrix m x n)
    Output:
        U, Sigma, Vt

    TODO:
    1. Tính A^T A
    2. Gọi eigen_decomposition
    3. Lấy singular values = sqrt(eigenvalues)
    4. Tạo Sigma
    5. Tính U
    6. Tính Vt = transpose(V)

    7. (Optional) verify:
        A ≈ U * Sigma * Vt
    """
    pass


def reconstruct(U, Sigma, Vt):
    """
    Input: U, Sigma, Vt
    Output: A reconstructed

    TODO:
    - nhân lại 3 ma trận
    """
    pass
