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
    
    def copy_from(self, other): # Hàm copy ma trận
        if not self.data: 
            self.data = [row[:] for row in other.data]
        else:
            if self.cols != other.cols or self.rows != other.rows:
               raise ValueError("Kích thước không khớp để sao chép.")
            for i in range(other.rows):
               for j in range(other.cols):
                   self.data[i][j] = other.data[i][j]
                 
    def swap_rows(self, i, j): # Hàm hoán đổi hàng
        if 0 <= i < self.rows and 0 <= j < self.rows:
            self.data[i], self.data[j] = self.data[j], self.data[i]
        else:
            print("Chỉ số hàng không hợp lệ")

    def swap_cols(self, a, b): # Hàm hoán đổi cột
        if 0 <= a < self.cols and 0 <= b < self.cols:
            for i in range(self.rows):
                self.data[i][a], self.data[i][b] = self.data[i][b], self.data[i][a]
        else:
            print("Chỉ số cột không hợp lệ.")
            
    def multiply_row_with_real_number(self, i, k): # Nhân hàng i với số thực k
        if k == 0:
            raise ValueError("Số thực dùng để nhân với ma trận không được bằng 0.")
            
        if 0 <= i < self.rows:
            for j in range(self.cols):
                self.data[i][j] *= k
        else:
            print("Chỉ số hàng không hợp lệ.")

    def add_multiple_of_row(self, i, j, k): # Lấy hàng thứ i + k*hàng thứ j
        if not (0 <= i < self.rows and 0 <= j < self.rows):
            raise IndexError(f"Chỉ số hàng không hợp lệ.")
        for c in range(self.cols):
            self.data[i][c] += k * self.data[j][c]
            
    def get_Tran(self): # Hàm lấy ma trận chuyển vị
        new_data = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(new_data)
