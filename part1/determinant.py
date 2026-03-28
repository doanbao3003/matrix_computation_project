def determinant(A): # Hàm tính định thức ma trận
    if A.rows != A.cols:
        raise ValueError(f"Ma trận {A.name} không phải ma trận vuông nên không có định thức.")

    n = A.rows
    temp_matrix = A.copy()
    m_data = temp_matrix.data
    
    det = 1.0
    swaps = 0

    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(m_data[k][i]) > abs(m_data[max_row][i]):
                max_row = k
        
        if max_row != i:
            temp_matrix.swap_rows(i, max_row)
            swaps += 1
            
        if abs(m_data[i][i]) < 1e-10:
            return 0.0
            
        for k in range(i + 1, n):
            factor = m_data[k][i] / m_data[i][i]
            for j in range(i, n):
                m_data[k][j] -= factor * m_data[i][j]

    for i in range(n):
        det *= m_data[i][i]

    return det * ((-1) ** swaps)
