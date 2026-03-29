from gaussian import gaussian_eliminate_2
def rank_and_basic(A):
    n, m = A.rows, A.cols
    A_copy = A.copy()
    
    b_dummy = Matrix([[0.0] for _ in range(n)], "zero")
    
    gaussian_eliminate_2(A_copy, b_dummy)
    
    pivot_cols = []
    row_basis = []
    col_basis = []
    
    for i in range(n):
        found_pivot = False
        for j in range(m):
            if abs(A_copy.data[i][j]) > 1e-10:
                if not found_pivot:
                    pivot_cols.append(j)
                    found_pivot = True
        
        if found_pivot:
            row_basis.append(A_copy.data[i])
            
    rank = len(pivot_cols)
    
    for j in pivot_cols:
        column = [A.data[i][j] for i in range(n)]
        col_basis.append(column)
        
    null_basis = []
    is_pivot_col = [False] * m
    for j in pivot_cols:
        is_pivot_col[j] = True
        
    free_vars = [j for j in range(m) if not is_pivot_col[j]]
    
    for free_idx in free_vars:
        special_solution = [0.0] * m
        special_solution[free_idx] = 1.0
        
        for i in range(rank):
            p_col = pivot_cols[i]
            special_solution[p_col] = -A_copy.data[i][free_idx]
            
        null_basis.append(special_solution)
        
    return {
        "rank": rank,
        "row_basis": row_basis,
        "col_basis": col_basis,
        "null_basis": null_basis
    }
