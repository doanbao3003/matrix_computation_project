def gaussian_eliminate(A, b): # Hàm nhận ma trận A, b và thực hiện khử ma trận bằng Gauss-Jordan (REF)
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
    
def gaussian_eliminate_2(A, b): # Phiên bản thực hiện RREF thay vì REF của hàm gaussian_eliminate
    if A.rows != b.rows:
        raise ValueError("Số hàng của A và b phải bằng nhau.")

    n = A.rows
    m = A.cols
    
    aug_data = []
    for i in range(n):
        aug_data.append(A.data[i] + b.data[i])
    Ab = Matrix(aug_data, "Augmented_RREF")

    pivot_row = 0
    for j in range(m):
        if pivot_row >= n:
            break
            
        max_idx = pivot_row
        for k in range(pivot_row + 1, n):
            if abs(Ab.data[k][j]) > abs(Ab.data[max_idx][j]):
                max_idx = k
        
        if abs(Ab.data[max_idx][j]) < 1e-10:
            continue
            
        Ab.swap_rows(pivot_row, max_idx)
        
        pivot_val = Ab.data[pivot_row][j]
        Ab.multiply_row_with_real_number(pivot_row, 1.0 / pivot_val)
        
        for i in range(n):
            if i != pivot_row:
                factor = -Ab.data[i][j]
                Ab.add_multiple_of_row(i, pivot_row, factor)
        
        pivot_row += 1

    A.data = [row[:m] for row in Ab.data]
    b.data = [row[m:] for row in Ab.data]
    A.rows, A.cols = len(A.data), len(A.data[0])
    b.rows, b.cols = len(b.data), len(b.data[0])
    
def back_substitution(A, b): #Hàm giải hệ tam giác từ gaussian_eliminated với trường hợp ma trận b có kích thước n x 1.
    # Hàm sẽ trả về danh sách nghiệm.
    # Với trường hợp vô nghiệm, trả về list rỗng.
    # Với trường hợp vô số nghiệm, hàm sẽ trả về các nghiệm suy biến dưới định dạng string.
    
    if b.cols != 1:
        print("Lỗi: b phải là ma trận cột (n x 1).")
        return []

    n = A.rows
    m = A.cols
    
    for i in range(n):
        row_all_zeros = all(abs(A.data[i][j]) < 1e-10 for j in range(m))
        if row_all_zeros and abs(b.data[i][0]) > 1e-10:
            print("Hệ phương trình vô nghiệm.")
            return []

    pivot_col = {} 
    is_pivot_column = [False] * m
    for i in range(n):
        for j in range(m):
            if abs(A.data[i][j]) > 1e-10:
                pivot_col[i] = j
                is_pivot_column[j] = True
                break

    free_vars = {}
    t_idx = 1
    for j in range(m):
        if not is_pivot_column[j]:
            free_vars[j] = f"t{t_idx}"
            t_idx += 1

    res = [None] * m
    
    for j, name in free_vars.items():
        res[j] = name

    for i in range(n - 1, -1, -1):
        if i not in pivot_col:
            continue
        
        curr_col = pivot_col[i]
        constant_part = b.data[i][0]
        expression_parts = []
        
        for j in range(curr_col + 1, m):
            coeff = A.data[i][j]
            if abs(coeff) > 1e-10:
                if isinstance(res[j], (int, float)):
                    constant_part -= coeff * res[j]
                else:
                    expression_parts.append(f"({-coeff}*{res[j]})")

        pivot_val = A.data[i][curr_col]
        final_constant = constant_part / pivot_val
        
        if not expression_parts:
            res[curr_col] = round(final_constant, 4)
        else:
            expr = " + ".join(expression_parts)
            res[curr_col] = f"{round(final_constant, 4)} + {expr}"

    return res
