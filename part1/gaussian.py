from __init__ import Matrix

def gaussian_eliminate(A, b):
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
