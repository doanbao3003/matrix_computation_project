"""
File: benchmark.py
Người làm: Phát
Vị trí: part3/benchmark.py

Nhiệm vụ:
- Tạo dữ liệu thử nghiệm cho Phần 3.
- Đo thời gian chạy trung bình 5 lần.
- Đo sai số tương đối ||Ax - b||₂ / ||b||₂.
- Lưu bảng kết quả JSON để analysis.ipynb phân tích.

Cấu trúc thư mục kỳ vọng (theo đề):
    Group_<ID>/
    ├── part1/
    │   ├── matrix.py
    │   └── gaussian.py
    ├── part2/
    │   └── decomposition.py
    └── part3/
        ├── solvers.py      ← import từ đây
        └── benchmark.py   ← file này

Phân công:
- Sau khi hoàn tất cần thống nhất format dữ liệu với Thoại (analysis.ipynb).

Cải tiến:
- Dùng NumPy để tăng tốc sinh ma trận và tính sai số.
- Các hàm sinh ma trận nội bộ dùng numpy array, chuyển về list khi trả ra
  (vì solvers.py yêu cầu list 2D và list phẳng).
"""

import json
import math
import os
import sys
import time

import numpy as np

# ---------------------------------------------------------------------------
# THIẾT LẬP PATH
# Thêm thư mục part3 (chứa solvers.py) vào sys.path để import được.
# ---------------------------------------------------------------------------
_part3_dir = os.path.dirname(os.path.abspath(__file__))
if _part3_dir not in sys.path:
    sys.path.insert(0, _part3_dir)

# Đảm bảo UTF-8 trên Windows (tránh lỗi UnicodeEncodeError với tiếng Việt)
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


# ===========================================================================
# PHẦN 1: SINH DỮ LIỆU THỬ NGHIỆM (dùng NumPy)
# ===========================================================================

def generate_random_matrix(n, seed=42):
    """
    Sinh ma trận ngẫu nhiên khả nghịch kích thước n×n.

    Kỹ thuật: Cộng thêm n vào đường chéo (dominant diagonal) để đảm bảo
    ma trận không suy biến và ổn định về mặt số học.

    Dùng NumPy: np.random thay vì random module → nhanh hơn ~100x cho n lớn.

    Tham số:
        n    : kích thước ma trận
        seed : hạt giống ngẫu nhiên (để kết quả tái lập được)

    Trả về: list of list (n×n)
    """
    rng = np.random.default_rng(seed)
    A = rng.uniform(-1.0, 1.0, size=(n, n))

    # Làm trội đường chéo → đảm bảo khả nghịch
    np.fill_diagonal(A, A.diagonal() + float(n))

    return A.tolist()


def generate_spd_matrix(n, seed=42):
    """
    Sinh ma trận SPD (Symmetric Positive Definite) kích thước n×n.

    Công thức: A = Bᵀ·B + α·I
        - B   : ma trận ngẫu nhiên
        - α=1 : đảm bảo xác định dương chặt

    Dùng NumPy: B.T @ B thay vì 3 vòng lặp lồng → O(n³) nhưng chạy ở C level.

    Tham số:
        n    : kích thước ma trận
        seed : hạt giống ngẫu nhiên

    Trả về: list of list (n×n)
    """
    rng = np.random.default_rng(seed)
    B = rng.uniform(-1.0, 1.0, size=(n, n))

    # A = Bᵀ·B  →  đối xứng và nửa xác định dương
    A = B.T @ B

    # Cộng α·I → đảm bảo xác định dương chặt
    alpha = 1.0
    A += alpha * np.eye(n)

    return A.tolist()


def generate_hilbert_matrix(n):
    """
    Sinh ma trận Hilbert kích thước n×n:
        H[i][j] = 1 / (i + j + 1)   (chỉ số từ 0)

    Đây là ma trận điều kiện kém (ill-conditioned) kinh điển,
    dùng để kiểm tra độ ổn định số của các phương pháp giải.

    Dùng NumPy: broadcasting thay vì list comprehension.

    Tham số:
        n : kích thước ma trận

    Trả về: list of list (n×n)
    """
    i = np.arange(n).reshape(-1, 1)  # cột
    j = np.arange(n).reshape(1, -1)  # hàng
    H = 1.0 / (i + j + 1)
    return H.tolist()


# ===========================================================================
# PHẦN 2: HÀM TIỆN ÍCH TÍNH TOÁN (dùng NumPy)
# ===========================================================================

def _mat_vec_mul(A, x):
    """
    Nhân ma trận A (n×n) với vector x (list dài n).

    Dùng NumPy: A @ x thay vì 2 vòng lặp → nhanh hơn ~1000x cho n=1000.

    Trả về: list dài n
    """
    return (np.asarray(A) @ np.asarray(x)).tolist()


def _vec_norm_l2(v):
    """
    Tính chuẩn L2: ||v||₂ = √(Σ vᵢ²)

    Dùng NumPy: np.linalg.norm thay vì sum + sqrt.
    """
    return float(np.linalg.norm(v))


def _relative_residual(A, x_computed, b):
    """
    Tính sai số tương đối theo chuẩn L2:
        sai_số = ||A·x - b||₂ / ||b||₂

    Dùng NumPy: tất cả phép tính chạy ở C level, không có Python loop.

    Trả về float (inf nếu ||b|| ≈ 0).
    """
    A_np = np.asarray(A, dtype=float)
    x_np = np.asarray(x_computed, dtype=float)
    b_np = np.asarray(b, dtype=float)

    residual = A_np @ x_np - b_np
    norm_b = np.linalg.norm(b_np)

    if norm_b < 1e-15:
        return float("inf")

    return float(np.linalg.norm(residual) / norm_b)


def build_rhs_from_known_solution(A, seed=42):
    """
    Tạo nghiệm thật x_true ngẫu nhiên, rồi tính b = A·x_true.

    Mục đích: kiểm soát được nghiệm đúng khi benchmark → đo sai số
    chính xác hơn so với dùng b ngẫu nhiên.

    Dùng NumPy: A @ x_true ở C level.

    Tham số:
        A    : ma trận hệ số (list 2D, n×n)
        seed : hạt giống (dùng seed+1000 để độc lập với A)

    Trả về: (b, x_true) — cả hai đều là list phẳng
    """
    A_np = np.asarray(A, dtype=float)
    n = A_np.shape[0]

    rng = np.random.default_rng(seed + 1000)
    x_true = rng.uniform(-5.0, 5.0, size=n)

    b = A_np @ x_true

    return b.tolist(), x_true.tolist()


# ===========================================================================
# PHẦN 3: LÕI BENCHMARK
# ===========================================================================

def benchmark_one_solver(solver_func, A, b, repeat=5):
    """
    Chạy solver_func(A, b) đúng `repeat` lần.
    Đo thời gian chạy trung bình và sai số tương đối trung bình.

    Yêu cầu: solver_func nhận (A, b) và trả về SolveResult (xem solvers.py).

    Tham số:
        solver_func : hàm giải hệ
        A           : ma trận hệ số (list 2D)
        b           : vế phải (list phẳng)
        repeat      : số lần chạy để lấy trung bình (mặc định 5 — theo đề)

    Trả về dict:
    {
        "method"             : tên phương pháp (str),
        "avg_time_sec"       : thời gian trung bình (float, giây),
        "avg_relative_error" : sai số tương đối trung bình (float),
        "converged"          : có hội tụ không (bool | None),
        "iterations"         : số vòng lặp nếu là phương pháp lặp (int | None),
        "success"            : ít nhất 1 lần thành công (bool),
        "note"               : ghi chú từ solver (str)
    }
    """
    times   = []
    errors  = []
    method_name = "unknown"
    converged   = None
    iterations  = None
    note        = ""
    success     = False

    for _ in range(repeat):
        try:
            t0 = time.perf_counter()
            result = solver_func(A, b)
            t1 = time.perf_counter()

            times.append(t1 - t0)
            method_name = result.method
            converged   = result.converged
            iterations  = result.iterations
            note        = result.note

            if result.x is not None and len(result.x) > 0:
                err = _relative_residual(A, result.x, b)
                errors.append(err)
                success = True

        except Exception as exc:
            note = f"Lỗi khi chạy: {exc}"

    avg_time  = sum(times)  / len(times)  if times  else float("inf")
    avg_error = sum(errors) / len(errors) if errors else float("inf")

    return {
        "method"            : method_name,
        "avg_time_sec"      : avg_time,
        "avg_relative_error": avg_error,
        "converged"         : converged,
        "iterations"        : iterations,
        "success"           : success,
        "note"              : note,
    }


def benchmark_suite(ds_kich_thuoc=None):
    """
    Chạy benchmark đầy đủ theo ba loại ma trận và nhiều kích thước.

    Kích thước theo yêu cầu đề: n ∈ {50, 100, 200, 500, 1000}
    Loại ma trận:
        - "random"  : ma trận ngẫu nhiên khả nghịch (well-conditioned)
        - "spd"     : ma trận xác định dương đối xứng (well-conditioned)
        - "hilbert" : ma trận Hilbert — ill-conditioned, kiểm tra ổn định số

    Lưu ý:
        Ma trận Hilbert với n > 12 thường đã rất kém điều kiện.

    Tham số:
        ds_kich_thuoc : list kích thước tùy chỉnh (None = dùng mặc định theo đề)

    Trả về: list các dict kết quả
    """
    # -----------------------------------------------------------------------
    # Kích thước theo đúng yêu cầu đề (Phần 3, mục 3.2)
    # -----------------------------------------------------------------------
    if ds_kich_thuoc is None:
        ds_kich_thuoc = [50, 100, 200, 500, 1000]

    # -----------------------------------------------------------------------
    # Import solvers muộn để không lỗi nếu solvers.py chưa hoàn thiện
    # -----------------------------------------------------------------------
    try:
        from solvers import get_all_solvers
        all_solvers = get_all_solvers() or []
        if not all_solvers:
            print("[CẢNH BÁO] get_all_solvers() trả về danh sách rỗng.")
    except ImportError as exc:
        print(f"[LỖI] Không thể import solvers.py: {exc}")
        print("       Đảm bảo solvers.py nằm cùng thư mục với benchmark.py (part3/).")
        all_solvers = []

    # -----------------------------------------------------------------------
    # Cấu hình loại ma trận
    # -----------------------------------------------------------------------
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
                res["n"]           = n
                res["matrix_type"] = mat_type
                ket_qua.append(res)

                status = "OK  " if res["success"] else "FAIL"
                iter_str = f"  iter={res['iterations']}" if res["iterations"] is not None else ""
                print(
                    f"  [{status}] {res['method']:<35}"
                    f"  avg_time={res['avg_time_sec']:.4f}s"
                    f"  err={res['avg_relative_error']:.2e}"
                    + iter_str
                    + (f"  note={res['note']}" if res["note"] else "")
                )

    return ket_qua


# ===========================================================================
# PHẦN 4: LƯU KẾT QUẢ
# ===========================================================================

def save_results_json(ket_qua, ten_file="benchmark_results.json"):
    """
    Lưu kết quả benchmark ra file JSON cùng thư mục part3/.

    Xử lý các giá trị đặc biệt (inf, nan) → null để JSON hợp lệ.
    Thoại sẽ đọc file này trong analysis.ipynb để vẽ biểu đồ log-log
    và bảng so sánh theo yêu cầu đề.

    Tham số:
        ket_qua  : list dict kết quả từ benchmark_suite()
        ten_file : tên file output (mặc định benchmark_results.json)

    Trả về: đường dẫn tuyệt đối của file đã lưu (str)
    """
    def _sanitize(val):
        """Chuyển inf/nan → None để JSON không bị lỗi serialize."""
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
    return save_path


# ===========================================================================
# ENTRY POINT
# ===========================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("  BENCHMARK PHẦN 3 – So sánh các phương pháp giải hệ Ax = b")
    print("  Kích thước: n ∈ {50, 100, 200, 500, 1000}")
    print("  Loại ma trận: Random | SPD | Hilbert (ill-conditioned)")
    print("  Số lần đo mỗi cấu hình: 5 lần (lấy trung bình)")
    print("=" * 70)

    ket_qua = benchmark_suite()

    if ket_qua:
        save_results_json(ket_qua)
    else:
        print("\n[CẢNH BÁO] Không có kết quả nào được ghi lại.")