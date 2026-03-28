"""
File: decomposition.py
Người làm: Huỳnh Chí Thoại

Nhiệm vụ:
- Xây dựng SVD từ eigen decomposition
- Gọi eigen từ diagonalization.py
"""

from diagonalization import eigen_decomposition, compute_ata
import math # Thư viện sử dụng căn bậc 2

# Ngưỡng sai số học
EPSILON = 1e-10

def sqrt_list(values):
    """
    Input: list các số
    Output: list căn bậc hai
    """

    result = []
    for val in values:
        # Gia tri am rat nho do sai so -> xem nhu 0
        if val < 0 and abs(val) < EPSILON:
            result.append(0.0)
        elif val < 0:
            raise ValueError(f"Eigenvalue âm không hợp lệ cho SVD: {val}")
        else:
            result.append(math.sqrt(val))
    
    return result 


def build_sigma(singular_values, m, n):
    """
    Input:
        singular_values
        m, n (shape của A)
    Output:
        Sigma (matrix m x n)
    """
    
    # Tạo ma trận 0 m x n 
    Sigma = [[0.0 for _ in range(n)] for _ in range(m)]

    # Điền giá trị đường chéo
    for i in range(min(m, n, len(singular_values))): 
        Sigma[i][i] = singular_values[i]

    return Sigma


def transpose(A):
    """
    Input:
        Ma trận A (m x n)
    Output:
        Ma trận chuyển vị của A (n x m)
    """

    if not A or not A[0]:
        raise ValueError("Ma trận A rỗng")

    # Lay kich thuoc
    m = len(A)
    n = len(A[0])

    # Tạo ma trận có kích thước n x m
    result = [[0.0 for _ in range(m)] for _ in range(n)]

    # Hoán đổi vị trí
    for i in range(m):
        for j in range(n):
            result[j][i] = A[i][j]

    return result


def matmul(A, B):
    """
    Input:
        2 ma trận A và B
    Output:
        Ma trận tích của A và B
    """

    # Lấy kích thước
    m_A = len(A)
    n_A = len(A[0])
    m_B = len(B)
    n_B = len(B[0])

    # Kiểm tra điều kiện nhân
    if n_A != m_B:
        raise ValueError("Kích thước ma trân không hợp lệ để nhân")
    
    # Khởi tạo ma trận kết quả
    result = [[0.0 for _ in range(n_B)] for _ in range(m_A)]

    # Nhân 2 ma trận
    for i in range(m_A):
        for j in range(n_B):
            for k in range(n_A):
                result[i][j] += A[i][k] * B[k][j]

    return result


def inverse_diagonal(Sigma):
    """
    Input: Sigma (matrix đường chéo)
    Output: Sigma^-1
    """

    # Lấy kích thước
    m = len(Sigma)
    n = len(Sigma[0])

    # Khởi tạo ma trận kết quả
    result = [[0.0 for _ in range(m)] for _ in range(n)]

    # Xử lý nghịch đảo trên đường chéo
    for i in range(min(m, n)):
        singular_value =  Sigma[i][i]
        
        # Kiểm tra giá trị trên đường chéo có xắp xỉ hoặc bằng 0 hay không
        if singular_value > EPSILON:
            result[i][i] = 1.0 / singular_value    

    return result


def normalize_columns(U):
    """
    Input: U (matrix)
    Output: U đã chuẩn hóa cột
    """
    
    # Lấy kích thước
    m = len(U)
    n = len(U[0])

    # Khỏi tạo ma trận kết quả
    result = [[0.0 for _ in range(n)] for _ in range(m)]

    # Chuẩn hóa từng cột về norm = 1
    for j in range(n):
        # Khởi tạo norm của từng cột
        col_norm = 0.0

        # Tính norm
        for i in range(m):
            col_norm += U[i][j]**2
        
        col_norm = math.sqrt(col_norm)

        # Nếu norm qua nhỏ thì đặt cột bằng 0
        if col_norm > EPSILON:
            for i in range(m):
                result[i][j] = U[i][j] / col_norm    
        else:
            for i in range(m):
                result[i][j] = 0.0

    return result


def compute_U(A, V, Sigma):
    """
    Input:
        A
        V (eigenvectors)
        Sigma
    Output:
        U
    """

    # Tính nghịch đảo của Sigma    
    inv_Sigma = inverse_diagonal(Sigma)

    # Tính tích AV
    AV = matmul(A, V)

    # Tính U theo công thức U = A * V * Sigma^-1
    U = matmul(AV, inv_Sigma)

    # Chuẩn hóa U
    U = normalize_columns(U)

    return U 


def svd(A):
    """
    Input: A (matrix m x n)
    Output:
        U, Sigma, Vt
    """
    
    # Tính A^T A
    ATA = compute_ata(A)

    # Gọi eigen_decomposition
    eigenvalues, V = eigen_decomposition(ATA)

    # Tính singular values
    singular_values = sqrt_list(eigenvalues)

    # Xây dựng ma trận Sigma
    m = len(A)
    n = len(A[0])
    Sigma = build_sigma(singular_values, m, n)

    # Tính ma trận U
    U = compute_U(A, V, Sigma)

    # Tính Vt = transpose(V)
    Vt = transpose(V)
    
    return U, Sigma, Vt


def reconstruct(U, Sigma, Vt):
    """
    Input: 
        U, Sigma, Vt
    Output: 
        A reconstructed
    """

    # Lấy tích U và Sigma
    U_Sigma = matmul(U, Sigma)
    
    # Lấy tích của U, Sigma, Vt và lưu vào biến kết quả
    result = matmul(U_Sigma, Vt)

    return result
