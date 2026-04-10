def gaussian_eliminate(A, b): # Hàm nhận 2 ma trận A, b, gộp 2 ma trận này lại và đưa ma trận về dạng chuẩn tắc (RREF), sau đó tách 2 ma trận ra.
    n, m = A.rows, A.cols
    aug_data = [A.data[i] + b.data[i] for i in range(n)]
    Ab = Matrix(aug_data, "Augmented")

    pivot_row = 0
    for j in range(m):
        if pivot_row >= n: break
        
        max_idx = pivot_row
        for k in range(pivot_row + 1, n):
            if abs(Ab.data[k][j]) > abs(Ab.data[max_idx][j]):
                max_idx = k
        
        if abs(Ab.data[max_idx][j]) < 1e-8: continue
        
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
    return A, b

def back_substitution(A, b): # Hàm giải hệ phương trình bậc thang.
    if b.cols != 1:
        print("Lỗi: b phải là ma trận cột.")
        return []

    n, m = A.rows, A.cols
    
    for i in range(n):
        if all(abs(A.data[i][j]) < 1e-8 for j in range(m)) and abs(b.data[i][0]) > 1e-8:
            print("Hệ phương trình vô nghiệm.")
            return []

    pivot_col = {} 
    is_pivot_column = [False] * m
    for i in range(n):
        for j in range(m):
            if abs(A.data[i][j]) > 1e-8:
                pivot_col[i] = j
                is_pivot_column[j] = True
                break

    res = [None] * m
    t_idx = 1
    for j in range(m):
        if not is_pivot_column[j]:
            res[j] = f"t{t_idx}"
            t_idx += 1

    for i in range(n - 1, -1, -1):
        if i not in pivot_col: continue
        
        curr_col = pivot_col[i]
        pivot_val = A.data[i][curr_col]
        constant_part = b.data[i][0]
        expression_parts = []
        
        for j in range(curr_col + 1, m):
            coeff = A.data[i][j]
            if abs(coeff) > 1e-8:
                if isinstance(res[j], (int, float)):
                    constant_part -= coeff * res[j]
                else:
                    reduced_coeff = -coeff / pivot_val
                    sign = "+" if reduced_coeff > 0 else "-"
                    val = abs(round(reduced_coeff, 4))
                    expression_parts.append(f"{sign} {val}*{res[j]}")

        final_constant = round(constant_part / pivot_val, 4)
        
        if not expression_parts:
            res[curr_col] = final_constant
        else:
            expr = " ".join(expression_parts)
            if final_constant == 0:
                if expr.startswith("+ "): 
                    expr = expr[2:]
                res[curr_col] = expr
            else:
                res[curr_col] = f"{final_constant} {expr}"

    return res
