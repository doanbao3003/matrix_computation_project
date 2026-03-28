from __init__ import Matrix

def gaussian_eliminate(A, b):
    if A.rows != b.rows:
        raise ValueError("Số hàng của A và b phải bằng nhau.")

    n_cols_a = A.cols
    n_cols_b = b.cols

    aug_data = []
    for i in range(A.rows):
        aug_data.append(A.data[i] + b.data[i])
    
    Ab = Matrix(aug_data, "Augmented")
    n = Ab.rows
    m = Ab.cols

    for i in range(min(n, n_cols_a)):
        max_row = i
        for k in range(i + 1, n):
            if abs(Ab.data[k][i]) > abs(Ab.data[max_row][i]):
                max_row = k
        Ab.swap_rows(i, max_row)

        if abs(Ab.data[i][i]) < 1e-10:
            continue

        for k in range(i + 1, n):
            factor = -Ab.data[k][i] / Ab.data[i][i]
            Ab.add_multiple_of_row(k, i, factor)

    A.data = [row[:n_cols_a] for row in Ab.data]
    b.data = [row[n_cols_a:] for row in Ab.data]
    A.rows, A.cols = len(A.data), len(A.data[0])
    b.rows, b.cols = len(b.data), len(b.data[0])
    
def gaussian_eliminate_2(A, b):
    if A.rows != b.rows:
        raise ValueError("Số hàng của A và b phải bằng nhau.")

    n = A.rows
    m = A.cols
    
    # Tạo ma trận bổ sung Ab bằng cách ghép A và b
    aug_data = []
    for i in range(n):
        aug_data.append(A.data[i] + b.data[i])
    Ab = Matrix(aug_data, "Augmented_RREF")

    pivot_row = 0
    for j in range(m): # Duyệt qua từng cột của A
        if pivot_row >= n:
            break
            
        # 1. Tìm hàng có phần tử lớn nhất ở cột j (tính từ hàng pivot_row trở xuống)
        max_idx = pivot_row
        for k in range(pivot_row + 1, n):
            if abs(Ab.data[k][j]) > abs(Ab.data[max_idx][j]):
                max_idx = k
        
        # Nếu cột toàn số 0 (hoặc rất nhỏ), bỏ qua cột này
        if abs(Ab.data[max_idx][j]) < 1e-10:
            continue
            
        # 2. Hoán đổi hàng hiện tại với hàng chứa phần tử lớn nhất
        Ab.swap_rows(pivot_row, max_idx)
        
        # 3. CHUẨN HÓA: Đưa phần tử chốt về 1
        pivot_val = Ab.data[pivot_row][j]
        Ab.multiply_row_with_real_number(pivot_row, 1.0 / pivot_val)
        
        # 4. KHỬ CẢ TRÊN VÀ DƯỚI: Biến các phần tử khác trong cột j về 0
        for i in range(n):
            if i != pivot_row: # Khử cả hàng trên và hàng dưới pivot
                factor = -Ab.data[i][j]
                Ab.add_multiple_of_row(i, pivot_row, factor)
        
        pivot_row += 1

    # Cập nhật lại dữ liệu cho A và b từ ma trận Ab đã biến đổi
    A.data = [row[:m] for row in Ab.data]
    b.data = [row[m:] for row in Ab.data]
    A.rows, A.cols = len(A.data), len(A.data[0])
    b.rows, b.cols = len(b.data), len(b.data[0])
    
def back_substitution(A, b):
    # 1. Kiểm tra kích thước b (phải là n x 1)
    if b.cols != 1:
        print("Lỗi: b phải là ma trận cột (n x 1).")
        return []

    n = A.rows
    m = A.cols
    
    # 2. Kiểm tra hệ vô nghiệm
    for i in range(n):
        row_all_zeros = all(abs(A.data[i][j]) < 1e-10 for j in range(m))
        if row_all_zeros and abs(b.data[i][0]) > 1e-10:
            print("Hệ phương trình vô nghiệm.")
            return []

    # 3. Tìm vị trí các phần tử chốt (pivot)
    pivot_col = {} # Lưu {hàng: cột_chốt}
    is_pivot_column = [False] * m
    for i in range(n):
        for j in range(m):
            if abs(A.data[i][j]) > 1e-10:
                pivot_col[i] = j
                is_pivot_column[j] = True
                break

    # 4. Xác định biến tự do (các cột không có chốt)
    free_vars = {}
    t_idx = 1
    for j in range(m):
        if not is_pivot_column[j]:
            free_vars[j] = f"t{t_idx}"
            t_idx += 1

    # 5. Thực hiện thế ngược (Back-substitution)
    # Kết quả sẽ lưu dưới dạng chuỗi để mô tả nghiệm suy biến
    res = [None] * m
    
    # Gán biến tự do trước
    for j, name in free_vars.items():
        res[j] = name

    # Giải từ dưới lên cho các biến cơ sở
    for i in range(n - 1, -1, -1):
        if i not in pivot_col:
            continue
        
        curr_col = pivot_col[i]
        constant_part = b.data[i][0]
        expression_parts = []
        
        # Biểu diễn: x_i = (b_i - sum(a_ij * x_j)) / a_ii
        for j in range(curr_col + 1, m):
            coeff = A.data[i][j]
            if abs(coeff) > 1e-10:
                # Nếu là số thực (đã giải xong)
                if isinstance(res[j], (int, float)):
                    constant_part -= coeff * res[j]
                # Nếu là biến tự do (chuỗi)
                else:
                    expression_parts.append(f"({-coeff}*{res[j]})")

        pivot_val = A.data[i][curr_col]
        final_constant = constant_part / pivot_val
        
        if not expression_parts:
            res[curr_col] = round(final_constant, 4)
        else:
            # Tạo chuỗi biểu thức cho nghiệm suy biến
            expr = " + ".join(expression_parts)
            res[curr_col] = f"{round(final_constant, 4)} + {expr}"

    return res
