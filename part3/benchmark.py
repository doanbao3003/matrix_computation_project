import json
import math
import os
import sys
import time

import numpy as np

# PHẦN 1: CÁC HÀM SINH DỮ LIỆU THỬ NGHIỆM (DÙNG NUMPY)

def generate_random_matrix(n, seed=42):
    """
    Sinh ma trận ngẫu nhiên khả nghịch kích thước n x n.

    Kỹ thuật: Cộng thêm n vào đường chéo (dominant diagonal) để đảm bảo
    ma trận không suy biến và ổn định về mặt số học.

    Dùng NumPy: np.random thay vì random module → cho ra tốc độ nhanh hơn 

    Tham số:
        n    : kích thước ma trận vuông
        seed : hạt giống ngẫu nhiên để kết quả có thể tái lập

    Trả về:
        list of list (n x n)
    """
    # Bước 1: Khởi tạo generator với seed cố định 
    rng = np.random.default_rng(seed)

    # Bước 2: Sinh các phần tử ngẫu nhiên trong khoảng [-1, 1] 
    A = rng.uniform(-1.0, 1.0, size=(n, n))

    # Bước 3: Làm trội đường chéo để đảm bảo khả nghịch 
    np.fill_diagonal(A, A.diagonal() + float(n))

    return A.tolist()


def generate_spd_matrix(n, seed=42):
    """
    Sinh ma trận SPD (Symmetric Positive Definite - Đối xứng xác định dương).

    Công thức: A = Bᵀ·B + α·I
    Ý nghĩa: Đảm bảo ma trận luôn có nghiệm duy nhất và hội tụ tốt khi dùng
    phương pháp lặp như Gauss-Seidel.

    Tham số:
        n    : kích thước ma trận
        seed : hạt giống ngẫu nhiên

    Trả về:
        list of list (n x n)
    """
    # Bước 1: Sinh ma trận cơ sở B ngẫu nhiên 
    rng = np.random.default_rng(seed)
    B = rng.uniform(-1.0, 1.0, size=(n, n))

    # Bước 2: Tạo ma trận đối xứng A = Bᵀ · B 
    A = B.T @ B

    # --- Bước 3: Cộng thêm α·I để đảm bảo xác định dương chặt ---
    alpha = 1.0
    A += alpha * np.eye(n)

    return A.tolist()


def generate_hilbert_matrix(n):
    """
    Sinh ma trận Hilbert kích thước n x n: H[i][j] = 1 / (i + j + 1).

    Đặc điểm: Đây là ma trận "kém điều kiện" (ill-conditioned) kinh điển.
    Được dùng để thử thách độ chính xác của các thuật toán giải hệ phương trình.
    """
    # --- Bước 1: Tạo chỉ số hàng và cột 
    i = np.arange(n).reshape(-1, 1)
    j = np.arange(n).reshape(1, -1)

    # --- Bước 2: Tính toán toàn bộ phần tử ma trận 
    H = 1.0 / (i + j + 1)

    return H.tolist()


# PHẦN 2: CÁC HÀM TIỆN ÍCH TÍNH TOÁN SAI SỐ (DÙNG NUMPY)

def _mat_vec_mul(A, x):
    """Nhân ma trận A với vector x dùng NumPy để tối ưu hiệu năng."""
    return (np.asarray(A) @ np.asarray(x)).tolist()


def _vec_norm_l2(v):
    """Tính chuẩn L2 của vector: ||v||₂."""
    return float(np.linalg.norm(v))


def _relative_residual(A, x_computed, b):
    """
    Tính sai số tương đối (Relative Residual) theo chuẩn L2:
        error = ||A·x_computed - b||₂ / ||b||₂
    """
    # --- Bước 1: Chuyển đổi dữ liệu sang dạng NumPy ---
    A_np = np.asarray(A, dtype=float)
    x_np = np.asarray(x_computed, dtype=float)
    b_np = np.asarray(b, dtype=float)

    # --- Bước 2: Tính vector dư r = A·x - b ---
    residual = A_np @ x_np - b_np

    # --- Bước 3: Tính chuẩn của vector b làm gốc so sánh ---
    norm_b = np.linalg.norm(b_np)

    # --- Bước 4: Trả về sai số tương đối (tránh chia cho 0) ---
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
        A    : ma trận hệ số (list 2D, n x n)
        seed : hạt giống (dùng seed+1000 để độc lập với A)

    Trả về: (b, x_true) — cả hai đều là list phẳng
    """
    A_np = np.asarray(A, dtype=float)
    n = A_np.shape[0]

    rng = np.random.default_rng(seed + 1000)
    n = len(A)
    x_true = rng.uniform(-5.0, 5.0, size=n)

    # --- Bước 2: Tính b = A · x_true ---
    b = np.asarray(A) @ x_true

    return b.tolist(), x_true.tolist()


# PHẦN 3: LÕI BENCHMARK

def benchmark_one_solver(solver_func, A, b, repeat=5):
    """
    Chạy solver_func(A, b) đúng `repeat` lần.
    Đo thời gian chạy trung bình và sai số tương đối trung bình.

    Yêu cầu: solver_func nhận (A, b) và trả về SolveResult.

    Tham số:
        solver_func : hàm giải hệ
        A           : ma trận hệ số (list 2D)
        b           : vế phải (list phẳng)
        repeat      : số lần chạy để lấy trung bình (mặc định 5)

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
    # Khởi tạo các biến
    times   = []
    errors  = []
    method_name = "unknown"
    converged   = None
    iterations  = None
    note        = ""
    success     = False

    # --- Bước 2: Thực thi vòng lặp lặp đo lường ---
    for _ in range(repeat):
        try:
            # Đo thời gian bắt đầu
            t0 = time.perf_counter()
            result = solver_func(A, b)
            t1 = time.perf_counter()

            # Lưu trữ thông tin
            times.append(t1 - t0)
            method_name = result.method
            converged   = result.converged
            iterations  = result.iterations
            note        = result.note

            # Tính toán sai số nếu giải ra kết quả
            if result.x is not None and len(result.x) > 0:
                err = _relative_residual(A, result.x, b)
                errors.append(err)
                success = True

        except Exception as exc:
            note = f"Lỗi thực thi: {exc}"

    # --- Bước 3: Tính toán trung bình cộng các chỉ số ---
    avg_time  = sum(times)  / len(times)  if times  else float("inf")
    avg_error = sum(errors) / len(errors) if errors else float("inf")

    # --- Bước 4: Trả về kết quả đóng gói theo mẫu ---
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
        - "hilbert" : ma trận Hilbert (ill-conditioned), kiểm tra ổn định số

    Lưu ý:
        Ma trận Hilbert với n > 12 thường đã rất kém điều kiện.

    Tham số:
        ds_kich_thuoc : list kích thước tùy chỉnh (None = dùng mặc định theo đề)

    Trả về: list các dict kết quả
    """
    # Kích thước theo đúng yêu cầu đề (Phần 3, mục 3.2)
    if ds_kich_thuoc is None:
        ds_kich_thuoc = [50, 100, 200, 500, 1000]

    # Nạp các solvers từ file solvers.py
    try:
        from solvers import get_all_solvers
        all_solvers = get_all_solvers() or []
    except ImportError:
        print("[LỖI] Không thể nạp solvers.py. Hãy kiểm tra lại file.")
        all_solvers = []

    matrix_configs = [
        ("random",  lambda n: generate_random_matrix(n, seed=42)),
        ("spd",     lambda n: generate_spd_matrix(n, seed=42)),
        ("hilbert", generate_hilbert_matrix),
    ]

    # --- Bước 2: Thực hiện vòng lặp qua từng kịch bản thử nghiệm ---
    ket_qua = []
    tong_cau_hinh = len(ds_kich_thuoc) * len(matrix_configs)
    id_test = 0

    for n in ds_kich_thuoc:
        for mat_type, mat_gen_func in matrix_configs:
            id_test += 1
            print(f"[{id_test}/{tong_cau_hinh}] Đang thử nghiệm n={n}, loại={mat_type}...")

            # Bước 2.1: Sinh ma trận và vế phải b
            try:
                A = mat_gen_func(n)
                b, _ = build_rhs_from_known_solution(A, seed=42)
            except Exception as exc:
                print(f"  [LỖI sinh ma trận] {exc}")
                continue

            # Bước 2.2: Chạy benchmark từng thuật toán
            for solver in all_solvers:
                res = benchmark_one_solver(solver, A, b, repeat=5)
                res["n"] = n
                res["matrix_type"] = mat_type
                ket_qua.append(res)

                # In kết quả trực tiếp ra màn hình
                status = "X" if res["success"] else "FAIL"
                iter_info = f" (itr: {res['iterations']})" if res["iterations"] else ""
                print(f"  [{status}] {res['method']:<30} | Time: {res['avg_time_sec']:.4f}s | Err: {res['avg_relative_error']:.2e}{iter_info}")

    return ket_qua


# PHẦN 4: LƯU TRỮ VÀ XUẤT DỮ LIỆU

def save_results_json(ket_qua, ten_file="benchmark_results.json"):
    """Lưu kết quả ra file JSON để dùng cho analysis.ipynb."""
    # --- Bước 1: Khử các giá trị Infinity/NaN để JSON hợp lệ ---
    def _sanitize(val):
        if isinstance(val, float) and (math.isinf(val) or math.isnan(val)):
            return None
        return val

    ket_qua_sach = [{k: _sanitize(v) for k, v in res.items()} for res in ket_qua]

    # --- Bước 2: Ghi file xuống ổ đĩa ---
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ten_file)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(ket_qua_sach, f, ensure_ascii=False, indent=2)

    print(f"\n[XONG] Toàn bộ kết quả đã lưu vào: {save_path}")
    return save_path


# ENTRY POINT

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