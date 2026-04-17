import os
import sys
import math

from part1.gaussian import Matrix

# PHẦN 1: CÁC HÀM MA TRẬN

def transpose(A):
    """
    Thực hiện chuyển vị ma trận A.
    Tái sử dụng lớp Matrix từ Part 1 để đảm bảo tính nhất quán.
    """
    # --- Bước 1: Khởi tạo đối tượng Matrix từ dữ liệu đầu vào ---
    mat = Matrix([row[:] for row in A], "tmp")
    
    # --- Bước 2: Gọi phương thức get_Tran() và trả về dữ liệu ---
    return mat.get_Tran().data


def matmul(A, B):
    """
    Thực hiện nhân hai ma trận A và B.
    Tái sử dụng nạp chồng toán tử * của lớp Matrix từ Part 1.
    """
    # --- Bước 1: Khởi tạo hai đối tượng Matrix ---
    mat_a = Matrix(A, "A")
    mat_b = Matrix(B, "B")
    
    # --- Bước 2: Thực hiện phép nhân và trả về dữ liệu kết quả ---
    return (mat_a * mat_b).data


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


def compute_ata(A):
    """
    Input: A (list 2D)
    Output: A^T * A (list 2D)
    """
    # --- Bước 1: Tìm ma trận chuyển vị A^T ---
    AT = transpose(A)
    
    # --- Bước 2: Thực hiện nhân AT với A ---
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

    # --- Bước 1: Khởi tạo dữ liệu ---
    # S là ma trận sẽ dần biến thành ma trận đường chéo
    S = [row[:] for row in A]
    # V là ma trận tích lũy các phép xoay, cuối cùng sẽ là ma trận eigenvectors
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    max_sweeps = 100 # Số lượt duyệt tối đa để tránh lặp vô tận
    tol = 1e-12      # Ngưỡng hội tụ (Tolerance)

    # --- Bước 2: Vòng lặp chính của thuật toán Jacobi ---
    for sweep in range(max_sweeps):
        # 2.1: Kiểm tra độ hội tụ bằng cách tính tổng các phần tử ngoài đường chéo
        off_norm = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                off_norm += S[i][j] ** 2

        if off_norm < tol:
            break

        # 2.2: Duyệt qua tất cả các cặp (p, q) ngoài đường chéo
        for p in range(n):
            for q in range(p + 1, n):
                # Bỏ qua nếu phần tử S[p][q] đã đủ nhỏ
                if abs(S[p][q]) < tol / n:
                    continue

                # 2.3: Tính toán góc xoay theta phù hợp
                if abs(S[p][p] - S[q][q]) < 1e-15:
                    theta = math.pi / 4.0
                else:
                    theta = 0.5 * math.atan2(2.0 * S[p][q], S[p][p] - S[q][q])

                c = math.cos(theta)
                s = math.sin(theta)

                # 2.4: Áp dụng phép xoay Jacobi: S' = J^T · S · J
                # Chỉ thay đổi các phần tử ở hàng/cột p và q
                spp, sqq, spq = S[p][p], S[q][q], S[p][q]

                for i in range(n):
                    if i != p and i != q:
                        sip, siq = S[i][p], S[i][q]
                        # Cập nhật cả cột p và q (đồng thời là hàng p, q do đối xứng)
                        S[i][p] = S[p][i] = c * sip + s * siq
                        S[i][q] = S[q][i] = -s * sip + c * siq

                # Cập nhật các phần tử tại các điểm giao nhau (p,p), (q,q), (p,q)
                S[p][p] = c * c * spp + 2 * s * c * spq + s * s * sqq
                S[q][q] = s * s * spp - 2 * s * c * spq + c * c * sqq
                S[p][q] = S[q][p] = 0.0 # Triệt tiêu triệt để phần tử ngoài đường chéo

                # 2.5: Cập nhật ma trận vector riêng V = V · J
                for i in range(n):
                    vip, viq = V[i][p], V[i][q]
                    V[i][p] = c * vip + s * viq
                    V[i][q] = -s * vip + c * viq

    # --- Bước 3: Thu hoạch kết quả trị riêng từ đường chéo của S ---
    eigenvalues = [S[i][i] for i in range(n)]

    # --- Bước 4: Sắp xếp kết quả theo thứ tự trị riêng giảm dần ---
    # Lý do: Phục vụ cho phân rã SVD sau này (các giá trị đơn lẻ phải giảm dần)
    indices = sorted(range(n), key=lambda i: eigenvalues[i], reverse=True)
    sorted_eigenvalues = [eigenvalues[i] for i in indices]
    sorted_V = [[V[row][indices[col]] for col in range(n)] for row in range(n)]

    return sorted_eigenvalues, sorted_V


# PHẦN 3: XỬ LÝ VÀ SẮP XẾP

def sort_eigenpairs(eigenvalues, eigenvectors):
    """
    Sắp xếp lại các cặp (eigenvalue, eigenvector) theo thứ tự trị riêng giảm dần.
    Đảm bảo tính nhất quán của dữ liệu.
    """
    # --- Bước 1: Gộp cặp (trị riêng, vector riêng) bằng cách zip ---
    # eigenvectors được chuyển vị để lấy theo cột trước khi gộp
    pairs = list(zip(eigenvalues, zip(*eigenvectors)))

    # --- Bước 2: Thực hiện sắp xếp giảm dần ---
    pairs.sort(key=lambda x: x[0], reverse=True)

    # --- Bước 3: Giải nén và định cấu hình lại dữ liệu trả về ---
    sorted_values = [pair[0] for pair in pairs]
    # Chuyển các cột trở lại thành hàng cho danh sách lồng nhau chuẩn
    sorted_vectors = list(zip(*[pair[1] for pair in pairs]))
    sorted_vectors = [list(row) for row in sorted_vectors]

    return sorted_values, sorted_vectors


