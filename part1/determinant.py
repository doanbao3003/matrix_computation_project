def determinant(A): # Hàm tính định thức ma trận
    if A.rows != A.cols:
        raise ValueError("Chỉ tính được định thức của ma trận vuông.")
    
    n = A.rows
    A_copy = A.copy()
    det = 1.0
    
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(A_copy.data[k][i]) > abs(A_copy.data[max_row][i]):
                max_row = k
        
        if i != max_row:
            A_copy.swap_rows(i, max_row)
            det *= -1
            
        if abs(A_copy.data[i][i]) < 1e-10:
            return 0.0
        
        for k in range(i + 1, n):
            factor = -A_copy.data[k][i] / A_copy.data[i][i]
            A_copy.add_multiple_of_row(k, i, factor)
            
    for i in range(n):
        det *= A_copy.data[i][i]
        
    return round(det, 4)
