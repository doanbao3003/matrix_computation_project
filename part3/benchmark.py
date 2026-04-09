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
import math
import os
import random
import sys
import time
from solvers import get_all_solvers

# Thêm thư mục hiện tại vào path để import được solvers.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Sinh dữ liệu thử nghiệm
# ---------------------------------------------------------------------------

def generate_random_matrix(n, seed=42):
    """
    Sinh ma trận ngẫu nhiên khả nghịch kích thước n x n.

    Cộng thêm n vào đường chéo (dominant diagonal) để đảm bảo
    ma trận không suy biến và ổn định về mặt số học.

    Trả về: list of list (n x n)
    """
    random.seed(seed)
    A = [[random.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(n)]

    # Đảm bảo khả nghịch bằng cách làm trội đường chéo
    for i in range(n):
        A[i][i] += float(n)

    return A


def generate_spd_matrix(n, seed=42):
    """
    Sinh ma trận SPD (Symmetric Positive Definite) kích thước n x n.

    Công thức: A = B^T * B + alpha * I
        - B: ma trận ngẫu nhiên
        - alpha: hệ số nhỏ để đảm bảo positive definite chặt

    Trả về: list of list (n x n)
    """
    random.seed(seed)
    B = [[random.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(n)]

    # A = B^T * B (đối xứng và nửa xác định dương)
    A = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0.0
            for k in range(n):
                s += B[k][i] * B[k][j]
            A[i][j] = s

    # Cộng alpha * I để đảm bảo xác định dương chặt
    alpha = 1.0
    for i in range(n):
        A[i][i] += alpha

    return A


def generate_hilbert_matrix(n):
    """
    Sinh ma trận Hilbert kích thước n x n:
        H[i][j] = 1 / (i + j + 1)   (chỉ số từ 0)

    Đây là ma trận điều kiện kém (ill-conditioned) dùng để kiểm tra
    độ ổn định số của các phương pháp giải hệ phương trình.

    Trả về: list of list (n x n)
    """
    H = [[1.0 / (i + j + 1) for j in range(n)] for i in range(n)]
    return H


# ---------------------------------------------------------------------------
# Các hàm tiện ích tính toán thuần Python (không dùng numpy)
# ---------------------------------------------------------------------------

def mat_vec_mul(A, x):
    """
    Nhân ma trận A (n x n) với vector x (list dài n).

    Trả về: vector b = A * x (list dài n)
    """
    n = len(A)
    b = [0.0] * n
    for i in range(n):
        s = 0.0
        for j in range(n):
            s += A[i][j] * x[j]
        b[i] = s
    return b


def _vec_norm_l2(v):
    """Tính chuẩn L2 của vector v (dùng nội bộ)."""
    return math.sqrt(sum(vi * vi for vi in v))


def _relative_residual(A, x_computed, b):
    """
    Tính sai số tương đối: ||A*x - b||_2 / ||b||_2

    Dùng nội bộ trong benchmark_one_solver để đánh giá chất lượng nghiệm.
    """
    Ax = mat_vec_mul(A, x_computed)
    residual = [Ax[i] - b[i] for i in range(len(b))]
    norm_res = _vec_norm_l2(residual)
    norm_b = _vec_norm_l2(b)
    if norm_b < 1e-15:
        return float("inf")
    return norm_res / norm_b


def build_rhs_from_known_solution(A, seed=42):
    """
    Tạo nghiệm thật x_true ngẫu nhiên, rồi tính b = A * x_true.

    Mục đích: kiểm soát được nghiệm đúng khi benchmark, giúp đo
    sai số chính xác hơn so với dùng b ngẫu nhiên.

    Trả về: (b, x_true)
        - b     : list dài n (vế phải)
        - x_true: list dài n (nghiệm thật)
    """
    n = len(A)
    # Dùng seed khác để x_true độc lập với A
    random.seed(seed + 1000)
    x_true = [random.uniform(-5.0, 5.0) for _ in range(n)]
    b = mat_vec_mul(A, x_true)
    return b, x_true


# ---------------------------------------------------------------------------
# Lõi benchmark
# ---------------------------------------------------------------------------

def benchmark_one_solver(solver_func, A, b, repeat=5):
    """
    Chạy solver_func(A, b) repeat lần.
    Đo thời gian chạy trung bình và sai số tương đối trung bình.

    Yêu cầu: solver_func trả về SolveResult (xem solvers.py).

    Trả về dict:
    {
        "method"             : tên phương pháp (str),
        "avg_time_sec"       : thời gian trung bình (float, giây),
        "avg_relative_error" : sai số tương đối trung bình (float),
        "converged"          : có hội tụ không (bool | None),
        "success"            : ít nhất 1 lần chạy cho ra nghiệm (bool),
        "note"               : ghi chú từ solver (str)
    }
    """
    times = []
    errors = []
    method_name = "unknown"
    converged = None
    note = ""
    success = False

    for _ in range(repeat):
        try:
            t0 = time.perf_counter()
            result = solver_func(A, b)
            t1 = time.perf_counter()

            times.append(t1 - t0)
            method_name = result.method
            converged = result.converged
            note = result.note

            if result.x is not None and len(result.x) > 0:
                err = _relative_residual(A, result.x, b)
                errors.append(err)
                success = True

        except Exception as exc:
            note = f"Lỗi khi chạy: {exc}"

    avg_time = sum(times) / len(times) if times else float("inf")
    avg_error = sum(errors) / len(errors) if errors else float("inf")

    return {
        "method": method_name,
        "avg_time_sec": avg_time,
        "avg_relative_error": avg_error,
        "converged": converged,
        "success": success,
        "note": note,
    }


def benchmark_suite(ds_kich_thuoc=None):
    """
    Chạy benchmark đầy đủ theo ba loại ma trận và nhiều kích thước.

    Các kích thước mặc định: n = 50, 100, 200, 500, 1000
    Các loại ma trận:
        - "random"  : ma trận ngẫu nhiên khả nghịch
        - "spd"     : ma trận xác định dương đối xứng
        - "hilbert" : ma trận Hilbert (điều kiện kém)

    Lưu ý:
        - Ma trận Hilbert với n > 200 bị bỏ qua vì điều kiện quá kém,
          các solver có thể cho kết quả vô nghĩa.

    Trả về: list các dict kết quả (mỗi dict là 1 cặp solver - ma trận - kích thước)
    """
    if ds_kich_thuoc is None:
        ds_kich_thuoc = [50, 100, 200, 300]

    # --- Import solvers (muộn để không lỗi nếu solvers.py chưa hoàn thiện) ---
    try:
        from solvers import get_all_solvers
        all_solvers = get_all_solvers() or []
        if not all_solvers:
            print("[CẢNH BÁO] get_all_solvers() trả về danh sách rỗng.")
    except ImportError as exc:
        print(f"[LỖI] Không thể import solvers.py: {exc}")
        all_solvers = []

    # --- Cấu hình loại ma trận ---
    HILBERT_MAX_N = 200  # Giới hạn kích thước cho Hilbert

    matrix_configs = [
        ("random",  lambda n: generate_random_matrix(n, seed=42)),
        ("spd",     lambda n: generate_spd_matrix(n, seed=42)),
        ("hilbert", generate_hilbert_matrix),
    ]

    ket_qua = []
    tong_cau_hinh = len(ds_kich_thuoc) * len(matrix_configs)
    dem = 0

    for n in ds_kich_thuoc:
        for mat_type, mat_gen_func in matrix_configs:
            dem += 1
            header = f"[{dem:>2}/{tong_cau_hinh}] n={n:>4}, loại={mat_type}"

            # Bỏ qua Hilbert kích thước lớn
            if mat_type == "hilbert" and n > HILBERT_MAX_N:
                print(f"{header} => Bỏ qua (Hilbert n>{HILBERT_MAX_N} điều kiện quá kém)")
                continue

            print(f"{header} =>")

            # Tạo ma trận và vế phải
            try:
                A = mat_gen_func(n)
                b, _ = build_rhs_from_known_solution(A, seed=42)
            except Exception as exc:
                print(f"  [LỖI sinh ma trận] {exc}")
                continue

            if not all_solvers:
                print("  [skip] Chưa có solver nào.")
                continue

            # Chạy từng solver
            for solver_func in all_solvers:
                res = benchmark_one_solver(solver_func, A, b, repeat=5)
                res["n"] = n
                res["matrix_type"] = mat_type
                ket_qua.append(res)

                status = "OK  " if res["success"] else "FAIL"
                print(
                    f"  [{status}] {res['method']:<30} "
                    f"avg_time={res['avg_time_sec']:.4f}s  "
                    f"err={res['avg_relative_error']:.2e}"
                    + (f"  note={res['note']}" if res["note"] else "")
                )

    return ket_qua


# ---------------------------------------------------------------------------
# Lưu kết quả
# ---------------------------------------------------------------------------

def save_results_json(ket_qua, ten_file="benchmark_results.json"):
    """
    Lưu kết quả benchmark ra file JSON cùng thư mục với benchmark.py.

    Xử lý các giá trị đặc biệt (inf, nan) sang null để JSON hợp lệ.
    Thoại sẽ đọc file này trong notebook phân tích.
    """
    def _sanitize(val):
        """Chuyển inf/nan về None để JSON không bị lỗi."""
        if isinstance(val, float) and (math.isinf(val) or math.isnan(val)):
            return None
        return val

    ket_qua_sach = [
        {k: _sanitize(v) for k, v in entry.items()}
        for entry in ket_qua
    ]

    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ten_file)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(ket_qua_sach, f, ensure_ascii=False, indent=2)

    print(f"\n[✓] Đã lưu {len(ket_qua_sach)} kết quả vào: {save_path}")
    return save_path


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 65)
    print("  BENCHMARK PHẦN 3 – So sánh các phương pháp giải hệ Ax = b")
    print("=" * 65)

    ket_qua = benchmark_suite()

    if ket_qua:
        save_results_json(ket_qua)
    else:
        print("\n[CẢNH BÁO] Không có kết quả nào được ghi lại.")
        print("Hãy đảm bảo solvers.py đã được hoàn thiện và get_all_solvers()")
        print("trả về danh sách hàm giải hệ hợp lệ.")
