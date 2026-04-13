import os
import sys
import math
from dataclasses import dataclass
from typing import List, Optional

# THIẾT LẬP MÔI TRƯỜNG
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(_current_dir)  # thư mục gốc dự án
_part1_dir = os.path.join(_project_root, "part1")
_part2_dir = os.path.join(_project_root, "part2")

for _path in [_current_dir, _part1_dir, _part2_dir]:
    if _path not in sys.path:
        sys.path.insert(0, _path)

from part1.gaussian import gaussian_eliminate, back_substitution, Matrix
from part2.decomposition import svd, matmul, transpose, inverse_diagonal

# PHẦN 1: KIỂU DỮ LIỆU KẾT QUẢ CHUẨN HÓA
@dataclass
class SolveResult:
    """
    Kết quả chuẩn hóa cho mọi phương pháp giải hệ.

    Thuộc tính:
        x:          nghiệm tìm được (list số thực), rỗng nếu thất bại
        converged:  True nếu phương pháp hội tụ / thành công
        iterations: số vòng lặp (None nếu là phương pháp trực tiếp)
        method:     tên phương pháp (str)
        note:       ghi chú bổ sung (str)
    """
    x: List[float]
    converged: bool
    iterations: Optional[int]
    method: str
    note: str = ""

# PHẦN 2: HÀM TIỆN ÍCH
def relative_residual_l2(A, x, b):
    """
    Tính sai số tương đối theo chuẩn L2:

        sai_số = ||Ax - b||₂ / ||b||₂

    Tham số:
        A: ma trận hệ số, list 2D kích thước nxn
        x: nghiệm tính được, list phẳng dài n
        b: vế phải, list phẳng dài n

    Trả về:
        float: sai số tương đối (càng nhỏ càng tốt)
        inf nếu ||b|| ≈ 0
    """
    import numpy as np

    A_np = np.asarray(A, dtype=float)
    x_np = np.asarray(x, dtype=float)
    b_np = np.asarray(b, dtype=float)

    residual = A_np @ x_np - b_np
    norm_b = np.linalg.norm(b_np)

    if norm_b < 1e-15:
        return float("inf")

    return float(np.linalg.norm(residual) / norm_b)

# PHẦN 3: SOLVER 1 — GAUSS-JORDAN (TÁI SỬ DỤNG PART 1)


def solve_gauss_part1(A, b):
    """
    Giải hệ Ax = b bằng phương pháp khử Gauss-Jordan từ Part 1.

    Luồng xử lý:
        1. Chuyển A (list 2D) và b (list phẳng) → đối tượng Matrix
        2. Gọi gaussian_eliminate() → đưa [A|b] về dạng RREF
        3. Gọi back_substitution() → tìm nghiệm
        4. Kiểm tra: nghiệm duy nhất (toàn số) hay vô số nghiệm (có biến tự do)
        5. Đóng gói kết quả vào SolveResult

    Tham số:
        A: list 2D (nxn) — ma trận hệ số
        b: list phẳng (n,) — vế phải

    Trả về:
        SolveResult
    """
    n = len(A)

    # --- Bước 1: Tạo bản sao dưới dạng Matrix ---
    # Cần copy vì gaussian_eliminate sẽ thay đổi dữ liệu trực tiếp (in-place)
    A_mat = Matrix([row[:] for row in A], "A")

    # Chuyển b từ list phẳng [b1, b2, ...] → ma trận cột [[b1], [b2], ...]
    # vì gaussian_eliminate yêu cầu b là Matrix với mỗi hàng là 1 list
    b_mat = Matrix([[b[i]] for i in range(n)], "b")

    # --- Bước 2: Khử Gauss-Jordan → RREF ---
    gaussian_eliminate(A_mat, b_mat)

    # --- Bước 2.5: Dọn sai số dấu phẩy động ---
    # Với ma trận lớn (n >= 50), sau RREF các hàng cuối của A có thể
    # toàn giá trị gần 0 (vd: 1e-11) do tích lũy sai số floating point,
    # nhưng b tương ứng lại còn "rác" lớn hơn (vd: 1e-9).
    # back_substitution dùng ngưỡng 1e-10 để phân biệt:
    #   - Hàng A toàn 0 VÀ b ≠ 0 → kết luận vô nghiệm
    # Nên nếu hàng A gần 0, ta ép b về 0 luôn để tránh nhận nhầm.
    ZERO_ROW_TOL = 1e-9  # rộng hơn _PIVOT_TOL=1e-10 của gaussian.py
    m = A_mat.cols
    for i in range(A_mat.rows):
        if all(abs(A_mat.data[i][j]) < ZERO_ROW_TOL for j in range(m)):
            # Hàng A gần 0 → b tương ứng cũng chỉ là rác số học → ép về 0
            for k in range(b_mat.cols):
                b_mat.data[i][k] = 0.0

    # --- Bước 3: Giải hệ bậc thang ---
    # back_substitution trả về:
    #   - [] nếu vô nghiệm
    #   - list[float] nếu nghiệm duy nhất
    #   - list[float | str] nếu vô số nghiệm (biến tự do dạng "t1", "t2", ...)
    x_sol = back_substitution(A_mat, b_mat)

    # --- Bước 4: Xử lý kết quả ---

    # Trường hợp 1: Không có nghiệm (hệ vô nghiệm)
    if not x_sol:
        return SolveResult(
            x=[],
            converged=False,
            iterations=None,
            method="Gauss-Jordan (Part 1)",
            note="Hệ vô nghiệm"
        )

    # Trường hợp 2: Kiểm tra xem nghiệm có phải toàn số không
    has_free_vars = False
    numeric_x = []
    for val in x_sol:
        if isinstance(val, (int, float)):
            # Phần tử là số → giữ nguyên
            numeric_x.append(float(val))
        elif isinstance(val, str):
            has_free_vars = True
            # Trích phần hằng số từ biểu thức (vd: "2.5 + 1.0*t1 - 0.3*t2")
            # hoặc nếu là biến tự do thuần ("t1") → gán = 0
            try:
                # Nếu biểu thức bắt đầu bằng số (hằng số + các term)
                # → lấy phần hằng trước dấu cách đầu tiên
                parts = val.strip().split()
                first_token = parts[0] if parts else "0"
                # Kiểm tra token đầu có phải số không
                numeric_x.append(float(first_token))
            except (ValueError, IndexError):
                # Biến tự do thuần ("t1") hoặc expression phức tạp → gán 0
                numeric_x.append(0.0)
        else:
            numeric_x.append(0.0)

    if has_free_vars:
        return SolveResult(
            x=numeric_x,
            converged=True,
            iterations=None,
            method="Gauss-Jordan (Part 1)",
            note="Vô số nghiệm (ma trận kém điều kiện) — dùng nghiệm xấp xỉ (biến tự do = 0)"
        )

    # Trường hợp 3: Nghiệm duy nhất
    return SolveResult(
        x=numeric_x,
        converged=True,
        iterations=None,
        method="Gauss-Jordan (Part 1)"
    )


# PHẦN 4: SOLVER 2 — SVD DECOMPOSITION (TÁI SỬ DỤNG PART 2)

def solve_decomposition_part2(A, b):
    """
    Giải hệ Ax = b bằng phân rã SVD từ Part 2.

    Công thức:
        A = U x Σ x Vᵀ
        ⟹  x = V x Σ⁻¹ x Uᵀ x b

    Luồng xử lý:
        1. Gọi svd(A) → U, Σ, Vᵀ
        2. Tính Σ⁻¹ (nghịch đảo ma trận đường chéo, chỉ cần lật 1/σᵢ)
        3. Tính V = (Vᵀ)ᵀ  và  Uᵀ = transpose(U)
        4. Nhân chuỗi: x = V x Σ⁻¹ x Uᵀ x b

    Tham số:
        A: list 2D (nxn)
        b: list phẳng (n,)

    Trả về:
        SolveResult
    """
    n = len(A)

    try:
        # --- Bước 1: Phân rã SVD ---
        #     svd(A) trả về U (mxm), Sigma (mxn), Vt (nxn)
        #     trong đó A ≈ U x Sigma x Vt
        U, Sigma, Vt = svd(A)

        # --- Bước 2: Chuẩn bị các ma trận cần thiết ---
        Ut = transpose(U)        # Uᵀ: chuyển vị của U
        Sigma_inv = inverse_diagonal(Sigma)  # Σ⁻¹: nghịch đảo đường chéo
        V = transpose(Vt)        # V = (Vᵀ)ᵀ

        # --- Bước 3: Chuyển b thành ma trận cột ---
        # b là list phẳng [b1, b2, ...] → cần chuyển thành [[b1], [b2], ...]
        b_col = [[b[i]] for i in range(n)]

        # --- Bước 4: Tính x = V x Σ⁻¹ x Uᵀ x b ---
        # Nhân từ phải sang trái để tiết kiệm phép tính:
        step1 = matmul(Ut, b_col)           # Uᵀ x b       → (nx1)
        step2 = matmul(Sigma_inv, step1)     # Σ⁻¹ x (Uᵀb)  → (nx1)
        x_col = matmul(V, step2)             # V x (Σ⁻¹Uᵀb) → (nx1)

        # --- Bước 5: Chuyển kết quả về list phẳng ---
        x = [x_col[i][0] for i in range(len(x_col))]

        return SolveResult(
            x=x,
            converged=True,
            iterations=None,
            method="SVD Decomposition (Part 2)"
        )

    except Exception as e:
        # SVD có thể thất bại với ma trận điều kiện kém (ill-conditioned)
        return SolveResult(
            x=[],
            converged=False,
            iterations=None,
            method="SVD Decomposition (Part 2)",
            note=f"Lỗi SVD: {e}"
        )


# PHẦN 5: KIỂM TRA ĐIỀU KIỆN CHÉO TRỘI

def is_strictly_diagonally_dominant(A):
    """
    Kiểm tra ma trận A có chéo trội hàng nghiêm ngặt hay không.

    Điều kiện chéo trội hàng:
        Với mọi hàng i:  |a_ii| > Σ |a_ij|   (j ≠ i)

        Tức phần tử đường chéo phải lớn hơn (strict) tổng tất cả
        phần tử còn lại trên cùng hàng (tính theo giá trị tuyệt đối).

    Ý nghĩa:
        Nếu A chéo trội → Gauss-Seidel CHẮC CHẮN hội tụ (điều kiện đủ).
        Nếu không chéo trội → có thể hội tụ hoặc không (phải thử).

    Tham số:
        A: list 2D (nxn)

    Trả về:
        True nếu chéo trội, False nếu không
    """
    n = len(A)

    for i in range(n):
        # Giá trị tuyệt đối phần tử đường chéo a_ii
        diag = abs(A[i][i])

        # Tổng giá trị tuyệt đối các phần tử ngoài đường chéo trên hàng i
        off_diag_sum = sum(abs(A[i][j]) for j in range(n) if j != i)

        # Điều kiện nghiêm ngặt: must be strictly greater, not equal
        if diag <= off_diag_sum:
            return False

    return True

# PHẦN 6: SOLVER 3 — GAUSS-SEIDEL (VIẾT MỚI)

def solve_gauss_seidel(A, b, x0=None, max_iter=1000, tol=1e-10):
    """
    Giải hệ Ax = b bằng phương pháp lặp Gauss-Seidel.

    Ý tưởng:
        Gauss-Seidel là phương pháp lặp, cải tiến từ Jacobi.
        Tại mỗi bước, khi tính x_i mới, ta dùng NGAY các giá trị
        x_j đã được cập nhật trước đó (j < i), thay vì dùng toàn
        bộ giá trị cũ như Jacobi.

    Công thức cập nhật:
        x_i^(k+1) = (1/a_ii) x [ b_i
                                  - Σ a_ij x x_j^(k+1)   (j < i, đã cập nhật)
                                  - Σ a_ij x x_j^(k)     (j > i, chưa cập nhật) ]

    Điều kiện hội tụ:
        - Đủ: ma trận A chéo trội hàng nghiêm ngặt
        - Cần: bán kính phổ < 1 (khó kiểm tra trực tiếp)

    Tiêu chuẩn dừng:
        ||x^(k+1) - x^(k)||₂ < tol

    Tham số:
        A:        list 2D (nxn) — ma trận hệ số
        b:        list phẳng (n,) — vế phải
        x0:       list phẳng (n,) — nghiệm khởi tạo (mặc định = vector 0)
        max_iter: int — số vòng lặp tối đa (mặc định 1000)
        tol:      float — ngưỡng hội tụ (mặc định 1e-10)

    Trả về:
        SolveResult
    """
    n = len(A)

    # --- Kiểm tra điều kiện hội tụ (chéo trội) ---
    is_dominant = is_strictly_diagonally_dominant(A)

    # --- Bước 1: Khởi tạo nghiệm ban đầu ---
    # Nếu không truyền x0 thì bắt đầu từ vector 0
    if x0 is None:
        x = [0.0] * n
    else:
        x = x0[:]  # copy để không thay đổi dữ liệu gốc của caller

    # --- Bước 2: Vòng lặp Gauss-Seidel ---
    for iteration in range(1, max_iter + 1):
        # Lưu lại nghiệm cũ để so sánh kiểm tra hội tụ
        x_old = x[:]

        # Cập nhật từng phần tử x_i
        for i in range(n):
            # Kiểm tra phần tử đường chéo khác 0
            # (nếu a_ii = 0 thì không thể chia, phải dừng)
            if abs(A[i][i]) < 1e-15:
                return SolveResult(
                    x=x,
                    converged=False,
                    iterations=iteration,
                    method="Gauss-Seidel",
                    note="Phần tử đường chéo a[{i}][{i}] ≈ 0, không thể tiếp tục"
                )

            # Tính tổng sigma = Σ a_ij * x_j với j ≠ i
            # Lưu ý: x[j] với j < i đã được CẬP NHẬT ở bước trước trong cùng vòng lặp
            #         x[j] với j > i vẫn là giá trị CŨ
            # → Đây chính là điểm khác biệt so với phương pháp Jacobi
            sigma = 0.0
            for j in range(n):
                if j != i:
                    sigma += A[i][j] * x[j]

            # Công thức cập nhật: x_i = (b_i - sigma) / a_ii
            x[i] = (b[i] - sigma) / A[i][i]

        # --- Bước 3: Kiểm tra hội tụ ---
        # Tính chuẩn L2 của sai khác giữa nghiệm mới và nghiệm cũ
        diff = math.sqrt(sum((x[i] - x_old[i]) ** 2 for i in range(n)))

        if diff < tol:
            # Hội tụ thành công!
            return SolveResult(
                x=x,
                converged=True,
                iterations=iteration,
                method="Gauss-Seidel",
                note=f"Hội tụ sau {iteration} vòng lặp"
                     + (" (chéo trội)" if is_dominant else " (không chéo trội)")
            )

    # --- Không hội tụ sau max_iter vòng ---
    return SolveResult(
        x=x,
        converged=False,
        iterations=max_iter,
        method="Gauss-Seidel",
        note=f"Không hội tụ sau {max_iter} vòng lặp"
             + (" (không chéo trội — không đảm bảo hội tụ)" if not is_dominant else "")
    )

# PHẦN 7: DANH SÁCH SOLVER CHO BENCHMARK

def get_all_solvers():
    """
    Trả về danh sách tất cả các hàm solver sẽ được benchmark.

    benchmark.py gọi hàm này để lấy danh sách solver,
    giúp không phải viết cứng (hardcode) tên solver ở nhiều chỗ.

    Khi thêm solver mới, chỉ cần thêm vào list này.
    """
    return [
        solve_gauss_part1,
        solve_decomposition_part2,
        solve_gauss_seidel,
    ]
