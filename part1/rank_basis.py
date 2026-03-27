def rank_and_basic(A): # Hàm tính hạng của ma trận, sau đấy tìm cơ sở cho không gian dòng và cơ sở cho không gian cột.
  # Hàm sẽ trả về list gồm 2 phần tử: [không gian dòng, không gian cột] và hạng của ma trận sẽ là len của list đó.
  n = A.rows
  b = Matrix([0] x n)
  new_b = get_Tran(b)
  gaussian_eliminate(A, b)
