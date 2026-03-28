from gaussian import gaussian_eliminate_2
def rank_and_basic(A): # Hàm tìm hạng, cơ sở của không gian dòng, cột, nghiệm
    # Hàm sẽ trả về dictionary lưu lại cá giá trị hạng, cơ sở của không gian dòng, cột, nghiệm
    n = A.rows
    m = A.cols
    
    A_copy = copy(A)
    b_dummy = Matrix([[0.0] for _ in range(n)], "zero")
    gaussian_eliminate_2(A_copy, b_dummy)
    
    pivot_cols = []
    row_basis = []
    
    for i in range(n):
        is_zero_row = True
        for j in range(m):
            if abs(A_copy.data[i][j]) > 1e-10:
                if is_zero_row:
                    pivot_cols.append(j)
                    is_zero_row = False
                break
        if not is_zero_row:
            row_basis.append(A_copy.data[i])
            
    rank = len(pivot_cols)
    
    col_basis = []
    for j in pivot_cols:
        column = [A.data[i][j] for i in range(n)]
        col_basis.append(column)
        
    null_basis = []
    free_vars = [j for j in range(m) if j not in pivot_cols]
    
    for free_idx in free_vars:
        special_solution = [0.0] * m
        special_solution[free_idx] = 1.0
        
        for i in range(len(pivot_cols)):
            p_col = pivot_cols[i]
            special_solution[p_col] = -A_copy.data[i][free_idx]
            
        null_basis.append(special_solution)
        
    return {
        "rank": rank,
        "row_basis": row_basis,
        "col_basis": col_basis,
        "null_basis": null_basis
    }
