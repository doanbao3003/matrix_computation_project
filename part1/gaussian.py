import builtins
_PIVOT_TOL = 1e-10

class Matrix:
    def __init__(self, data, name = "Unknown"): # Khởi tạo class ma trận bao gồm các thuộc tính: 1 list 2 chiều để lưu trữ ma trận, số hàng, số cột, tên
        self.data = data # list 2 chiều để lưu trữ ma trận
        self.rows = len(data) # Số hàng
        self.cols = len(data[0]) if self.rows > 0 else 0 # Số cột
        self.name = name # Tên ma trận

    def print_matrix(self): # Hàm in ma trận
        print(f"Ma trận {self.name} kích thước ({self.rows}x{self.cols}):")
        for row in self.data:
            print(row)
        print("-" * 20)

    def __repr__(self):
        return f"Matrix(name={self.name!r}, rows={self.rows}, cols={self.cols}, data={self.data!r})"

    def __add__(self, other): # Hàm cộng ma trận
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(f"Kích thước ma trận {self.name} không khớp với {other.name} để cộng.")

        new_data = [
            [self.data[r][c] + other.data[r][c] for c in range(self.cols)]
            for r in range(self.rows)
        ]
        return Matrix(new_data, f"({self.name} + {other.name})")

    def __sub__(self, other): # Hàm trừ ma trận
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(f"Kích thước ma trận {self.name} không khớp với {other.name} để trừ.")

        new_data = [
            [self.data[r][c] - other.data[r][c] for c in range(self.cols)]
            for r in range(self.rows)
        ]
        return Matrix(new_data, f"({self.name} - {other.name})")

    def __mul__(self, other): # Hàm nhân ma trận
        if isinstance(other, (int, float)): # Nhân ma trận cho một số thực
            new_data = [[val * other for val in row] for row in self.data]
            return Matrix(new_data, f"{self.name} * {other}")

        if isinstance(other, Matrix): # Nhân ma trận cho một ma trận khác
            if self.cols != other.rows:
                raise ValueError(f"Kích thước {self.name} không khớp với {other.name} để nhân.")

            new_data = []
            for i in range(self.rows):
                new_row = []
                for j in range(other.cols):
                    element = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                    new_row.append(element)
                new_data.append(new_row)
            return Matrix(new_data, f"({self.name} * {other.name})")
        raise TypeError("Chỉ hỗ trợ nhân Matrix với Matrix hoặc số thực.")

    def __rmul__(self, other):
        return self.__mul__(other)

    def copy_from(self, other): # Hàm copy ma trận
        if not self.data:
            self.data = [row[:] for row in other.data]
            self.rows = other.rows
            self.cols = other.cols
            self.name = other.name
        else:
            if self.cols != other.cols or self.rows != other.rows:
               raise ValueError("Kích thước không khớp để sao chép.")
            for i in range(other.rows):
               for j in range(other.cols):
                   self.data[i][j] = other.data[i][j]

    def copy(self, name=None):
        return Matrix([row[:] for row in self.data], self.name if name is None else name)

    def swap_rows(self, i, j): # Hàm hoán đổi hàng
        if 0 <= i < self.rows and 0 <= j < self.rows:
            self.data[i], self.data[j] = self.data[j], self.data[i]
        else:
            raise IndexError("Chỉ số hàng không hợp lệ")

    def swap_cols(self, a, b): # Hàm hoán đổi cột
        if 0 <= a < self.cols and 0 <= b < self.cols:
            for i in range(self.rows):
                self.data[i][a], self.data[i][b] = self.data[i][b], self.data[i][a]
        else:
            raise IndexError("Chỉ số cột không hợp lệ.")

    def multiply_row_with_real_number(self, i, k): # Nhân hàng i với số thực k
        if k == 0:
            raise ValueError("Số thực dùng để nhân với ma trận không được bằng 0.")

        if 0 <= i < self.rows:
            for j in range(self.cols):
                self.data[i][j] *= k
        else:
            raise IndexError("Chỉ số hàng không hợp lệ.")

    def add_multiple_of_row(self, i, j, k): # Lấy hàng thứ i + k*hàng thứ j
        if not (0 <= i < self.rows and 0 <= j < self.rows):
            raise IndexError(f"Chỉ số hàng không hợp lệ.")
        for c in range(self.cols):
            self.data[i][c] += k * self.data[j][c]

    def get_Tran(self): # Hàm lấy ma trận chuyển vị
        new_data = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(new_data, name=f"{self.name}^T")

builtins.Matrix = Matrix


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
                    val = abs(reduced_coeff)
                    expression_parts.append(f"{sign} {val}*{res[j]}")

        final_constant = constant_part / pivot_val
        
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
