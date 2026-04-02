"""
File: benchmark.py
Người làm: Khánh

Nhiệm vụ:
- Tạo dữ liệu thử nghiệm cho Phần 3.
- Đo thời gian chạy trung bình 5 lần.
- Đo sai số tương đối.
- Lưu bảng kết quả để notebook phân tích.

Phân công gợi ý:
- Sau khi hoàn tất cần thống nhất format dữ liệu với Thoại
"""

import json
import random
import time


def generate_random_matrix(n, seed=42):
    """
    TODO:
    - Sinh ma trận ngẫu nhiên khả nghịch kích thước n x n.

    Gợi ý:
    - Có thể cộng thêm giá trị lớn vào đường chéo để ma trận ổn định hơn.

    """
    pass


def generate_spd_matrix(n, seed=42):
    """
    TODO:
    - Sinh ma trận SPD để phục vụ phân tích ổn định số.

    Gợi ý:
    - Tạo B ngẫu nhiên rồi đặt A = B^T B + alpha I

    """
    pass


def generate_hilbert_matrix(n):
    """
    TODO:
    - Sinh ma trận Hilbert:
        H[i][j] = 1 / (i + j + 1)

    Ý nghĩa:
    - Đây là ma trận điều kiện kém để kiểm tra độ ổn định số.

    """
    pass


def mat_vec_mul(A, x):
    """
    TODO:
    - Nhân ma trận với vector.

    """
    pass


def build_rhs_from_known_solution(A, seed=42):
    """
    TODO:
    - Tạo nghiệm thật x_true ngẫu nhiên.
    - Tính b = A x_true.

    Ý nghĩa:
    - Giúp kiểm soát dữ liệu khi benchmark.

    """
    pass


def benchmark_one_solver(solver_func, A, b, repeat=5):
    """
    TODO:
    - Chạy solver repeat lần
    - Đo thời gian trung bình
    - Tính sai số tương đối trung bình

    Gợi ý:
    - Dùng time.perf_counter()

    """
    pass


def benchmark_suite(ds_kich_thuoc=None):
    """
    TODO:
    - Chạy benchmark cho các kích thước:
        n = 50, 100, 200, 500, 1000
    - Thu kết quả của tất cả solver

    """
    pass


def save_results_json(ket_qua, ten_file="benchmark_results.json"):
    """
    TODO:
    - Lưu kết quả benchmark ra file JSON.


    Vai trò:
    - Thoại sẽ đọc file này trong notebook phân tích.
    """
    pass


if __name__ == "__main__":
    """
    TODO:
    - Gọi benchmark_suite()
    - Lưu dữ liệu kết quả
    """
    pass
