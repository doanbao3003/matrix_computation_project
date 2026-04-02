"""
File: solvers.py
Người làm: Quang Phát

Nhiệm vụ:
- Cài đặt các hàm giải hệ phương trình cho Phần 3.
- Tái sử dụng:
    1. Gauss từ Phần 1
    2. Phân rã từ Phần 2
    3. Viết mới Gauss–Seidel
- Chuẩn hóa đầu ra để benchmark và notebook dùng chung được.

- Khi làm xong phải thống nhất API cho Khánh với Thoại.
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SolveResult:
    """
    Mục đích:
    - Gom kết quả của mọi phương pháp giải hệ về cùng một khuôn dạng.

    Thuộc tính:
    - x: nghiệm gần đúng tìm được
    - converged: có hội tụ hay không
    - iterations: số vòng lặp (nếu là phương pháp lặp)
    - method: tên phương pháp
    - note: ghi chú thêm
    """
    x: List[float]
    converged: bool
    iterations: Optional[int]
    method: str
    note: str = ""


def relative_residual_l2(A, x, b):
    """
    TODO:
    - Tính sai số tương đối theo đúng đề:
        ||Ax - b||_2 / ||b||_2

  

    Vai trò trong toàn bài:
    - Đây là hàm dùng chung để benchmark và phân tích kết quả.
    """
    pass


def solve_gauss_part1(A, b):
    """
    TODO:
    - Gọi lại code Gauss có partial pivoting từ Phần 1.
    - Không viết lại nếu nhóm đã có hàm hoàn chỉnh.

    Gợi ý triển khai:
    - import từ part1/gaussian.py
    - nhận nghiệm x
    - đóng gói vào SolveResult

    """
    pass


def solve_decomposition_part2(A, b):
    """
    TODO:
    - Gọi lại phương pháp phân rã mà nhóm đã chọn ở Phần 2.
    - Ví dụ:
        + LU
        + QR
        + SVD
        + Cholesky

    Gợi ý triển khai:
    - import từ part2/decomposition.py
    - dùng kết quả phân rã để giải Ax = b
    - đóng gói về SolveResult

    """
    pass


def is_strictly_diagonally_dominant(A):
    """
    TODO:
    - Kiểm tra điều kiện chéo trội hàng:
        |a_ii| > tổng |a_ij| với j != i

    Ý nghĩa:
    - Dùng để kiểm tra điều kiện hội tụ đủ cho Gauss–Seidel.

    """
    pass


def solve_gauss_seidel(A, b, x0=None, max_iter=100, tol=1e-9):
    """
    TODO:
    - Cài đặt Gauss–Seidel từ đầu.
    - Có kiểm tra điều kiện hội tụ.
    - Trả về:
        + nghiệm x
        + converged
        + số vòng lặp
        + ghi chú

    Các bước gợi ý:
    1. Nếu x0 là None thì khởi tạo vector 0
    2. Với mỗi vòng lặp:
       - cập nhật từng phần tử x_i theo công thức Gauss–Seidel
    3. Kiểm tra chuẩn sai khác giữa 2 lần lặp liên tiếp
    4. Nếu nhỏ hơn tol thì dừng


    """
    pass


def get_all_solvers():
    """
    TODO:
    - Trả về danh sách các solver sẽ được benchmark.

    Ví dụ:
    - [solve_gauss_part1, solve_decomposition_part2, solve_gauss_seidel]



    Vai trò:
    - Giúp benchmark.py không phải viết cứng nhiều chỗ.
    """
    pass
