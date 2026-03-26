def Inverse(A): # Hàm tính A^(-1) bằng phương pháp Gauss-Jordan
   n = A.rows # Lấy số hàng của A
   I_n = [[0 for _ in range(n)] for _ in range(n)] # Tạo ma trận đơn vị I_n
   for i in range(A.rows):
      I_n[i][i] = 1
   gaussian_eliminated_2(new_matrix, I_n) # Thực hiện RREF trên [new_matrix | I_n]
   return I_n
