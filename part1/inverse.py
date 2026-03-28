from gaussian import gaussian_eliminate_2

def inverse(A): #Hàm tìm nghịch đảo của ma trận bằng sử dụng phép khử Gauss-Jordan
    if A.rows != A.cols:
        raise ValueError(f"Ma trận {A.name} không phải ma trận vuông."}

    n = A.rows
    
    A_copy = copy_from(A)

    identity_data = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    I = Matrix(identity_data, "Identity")

    gaussian_eliminate_2(A_copy, I)

    for i in range(n):
        if abs(A_copy.data[i][i] - 1.0) > 1e-10:
            print(f"Ma trận {A.name} là ma trận suy biến (không có nghịch đảo).")
            return None

    I.name = f"Inverse of {A.name}"
    return I
