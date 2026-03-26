
# Đọc kĩ init trước.

def gaussian_eliminate(A, b): # Hàm nhận ma trận A và ma trận b để thực hiện Gauss-Jordan dạng bậc thang (REF).
  # Cách khai báo Matrix b kích thước n x 1 để thực hiện Gauss-Jordan và giải phương trình nghiệm: b_data = ([[x_1],[x_2],....])
  # hoặc b_data = ([x_1, x_2, ...]) rồi dùng hàm get_Tran ở init để lấy chuyển vị.
  
  # M có thể thực hiện gộp 2 ma trận lại rồi sau đó thực hiện thuật như trong hướng dẫn rồi sau đó tách ma trận ra lại rồi sửa lại thằng b

  # Hoặc có thể thực hiện thao tác giống hệt nhau ở A và b luôn. Sau khi làm xong thì nhắn cho t biết m làm theo hướng nào, rồi xóa comment này đi.

  # Nhớ cập nhật thằng b sau khi thực hiện hàm, như vậy code t ở mấy phần sau mới chạy được

def back_substitution(A, b): # Hàm giải hệ tam giác thu được từ gaussian_eliminate.
  # Nhớ check xem kích thước của b có phải là n x 1 chưa rồi mới thực hiện
  
  # Tập nghiệm trả về Matrix kích thước n x 1 hoặc 1 x n rồi gọi hàm in ra ma trận trong init, hoặc m tự viết hàm in ra cũng được.
  
def gaussian_eliminate_2(A, b): # Hàm nhận ma trận A và ma trận b để thực hiện Gauss-Jordan dạng chuẩn tắc (RREF)

  # Nhớ cập nhật thằng b sau khi thực hiện hàm, như vậy code t ở mấy phần sau mới chạy được
