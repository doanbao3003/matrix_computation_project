from gaussian import gaussian_eliminate, Matrix

def inverse(A): # Hàm tìm nghịch đảo ma trận bằng phương pháp Gauss-Jordan
    if A.rows != A.cols:
        raise ValueError(f"Ma trận {A.name} không phải ma trận vuông ({A.rows}x{A.cols}).")

    n = A.rows
    
    A_copy = A.copy(name=f"{A.name}_tmp")

    identity_data = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    I = Matrix(identity_data, "Identity")

    gaussian_eliminate(A_copy, I)

    for i in range(n):
        if abs(A_copy.data[i][i] - 1.0) > 1e-10:
            print(f"Ma trận {A.name} là ma trận suy biến (không có nghịch đảo).")
            return None

    # 6. Trả về kết quả
    I.name = f"({A.name})^-1"
    return I
