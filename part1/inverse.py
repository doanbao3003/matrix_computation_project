from gaussian import gaussian_eliminate_2

def inverse(A):
    if A.rows != A.cols:
        print(f"Lỗi: Ma trận {A.name} không phải ma trận vuông.")
        return None

    n = A.rows
    
    A_copy = Matrix([row[:] for row in A.data], A.name)
    
    identity_data = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    I = Matrix(identity_data, "Identity")

    rref_gaussian_eliminate(A_copy, I)

    for i in range(n):
        if abs(A_copy.data[i][i] - 1.0) > 1e-10:
            print(f"Ma trận {A.name} là ma trận suy biến (không có nghịch đảo).")
            return None

    I.name = f"Inverse of {A.name}"
    return I
