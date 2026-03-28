def determinant(A):
    if A.rows != A.cols:
        raise ValueError(f"Ma trận {A.name} không phải ma trận vuông nên không có định thức.")

    n = A.rows
    temp_data = A.copy()
    
    det = 1.0
    swaps = 0

    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(temp_data[k][i]) > abs(temp_data[max_row][i]):
                max_row = k
        
        if max_row != i:
            temp_data[i], temp_data[max_row] = temp_data[max_row], temp_data[i]
            swaps += 1
            
        if abs(temp_data[i][i]) < 1e-10:
            return 0.0
            
        for k in range(i + 1, n):
            factor = temp_data[k][i] / temp_data[i][i]
            for j in range(i, n):
                temp_data[k][j] -= factor * temp_data[i][j]

    for i in range(n):
        det *= temp_data[i][i]

    return det * ((-1) ** swaps)
