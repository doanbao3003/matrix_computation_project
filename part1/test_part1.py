from __init__ import Matrix
from gaussian import solve_linear_system
from determinant import determinant
from inverse import inverse
from rank_basis import rank_and_basis
from verify import (
    verify_solution,
    verify_determinant,
    verify_inverse,
    verify_rank_and_basis,
)


def print_matrix(M, title=None):
    if title:
        print(title)
    if M is None:
        print("None")
        return
    for row in M.data:
        print(row)
    print()


print("=== TEST 1: HE CO NGHIEM DUY NHAT ===")
A1 = Matrix([[2, 1], [1, 3]], "A1")
b1 = Matrix([[5], [6]], "b1")
result1 = solve_linear_system(A1, b1)
print(result1["type"], result1["message"])
if result1["type"] == "unique":
    print_matrix(result1["solution"], "Nghiem:")
print("Verify:", verify_solution(A1, b1))
print("-" * 50)


print("=== TEST 2: HE VO SO NGHIEM ===")
A2 = Matrix([[1, 2, -1], [2, 4, -2]], "A2")
b2 = Matrix([[3], [6]], "b2")
result2 = solve_linear_system(A2, b2)
print(result2["type"], result2["message"])
if result2["type"] == "infinite":
    print_matrix(result2["particular_solution"], "Mot nghiem rieng:")
    print("Co so khong gian nghiem:")
    for i, vec in enumerate(result2["nullspace_basis"], 1):
        print_matrix(vec, f"Vector co so {i}:")
print("Verify:", verify_solution(A2, b2))
print("-" * 50)


print("=== TEST 3: HE VO NGHIEM ===")
A3 = Matrix([[1, 1], [1, 1]], "A3")
b3 = Matrix([[2], [3]], "b3")
result3 = solve_linear_system(A3, b3)
print(result3["type"], result3["message"])
print("Verify:", verify_solution(A3, b3))
print("-" * 50)


print("=== TEST 4: DINH THUC ===")
A4 = Matrix([[1, 2], [3, 4]], "A4")
print("det(A4) =", determinant(A4))
print("Verify:", verify_determinant(A4))
print("-" * 50)


print("=== TEST 5: NGHICH DAO ===")
A5 = Matrix([[4, 7], [2, 6]], "A5")
A5_inv = inverse(A5)
print_matrix(A5_inv, "A5^(-1):")
print("Verify:", verify_inverse(A5))
print("-" * 50)


print("=== TEST 6: HANG + CO SO ===")
A6 = Matrix([[1, 2, 3], [2, 4, 6], [1, 1, 1]], "A6")
rank, row_basis, col_basis = rank_and_basis(A6)
print("rank =", rank)
print_matrix(row_basis, "Co so khong gian dong:")
print_matrix(col_basis, "Co so khong gian cot:")
print("Verify:", verify_rank_and_basis(A6, rank, row_basis, col_basis))
print("-" * 50)
