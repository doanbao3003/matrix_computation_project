# Matrix Computation Project
## 🚀 Hướng dẫn cài đặt và chạy

### 1. Clone Repo
Mở terminal và chạy lệnh sau để tải mã nguồn về máy:
```bash
git clone https://github.com/doanbao3003/matrix_computation_project.git
cd matrix_computation_project
```

### 2. Cài đặt môi trường
Khuyến khích sử dụng môi trường ảo (virtual environment):
```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo (Windows)
.venv\Scripts\activate

# Kích hoạt môi trường ảo (Linux/macOS)
source .venv/bin/activate
```

Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### 3. Cách chạy các module
#### Chạy Benchmark (Phần 3)
Để thực thi đo lường hiệu năng của các bộ giải hệ phương trình:

```bash
python part3/benchmark.py
```
Kết quả sẽ được lưu vào file `part3/benchmark_results.json`.

#### Trực quan hóa Manim (Phần 2)
Để render video minh họa SVD:
```bash
manim -pql part2/manim_scene.py SVDScene
```

#### Xem Notebook phân tích
Sử dụng VS Code hoặc Jupyter Lab để mở và chạy các file:
- `part1/Part1_demo.ipynb`
- `part3/analysis.ipynb` (Yêu cầu đã chạy `benchmark.py` trước đó để có dữ liệu).

---