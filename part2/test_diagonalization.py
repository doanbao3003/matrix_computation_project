import math
from diagonalization import transpose, matmul, compute_ata, eigen_decomposition, sort_eigenpairs, build_diagonal

def is_close(a, b, rel_tol=1e-7):
    """Kiểm tra hai số hoặc hai ma trận có gần bằng nhau hay không."""
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=rel_tol, abs_tol=1e-9)
    
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): return False
        for i in range(len(a)):
            if not is_close(a[i], b[i], rel_tol): return False
        return True
    return a == b

def print_test_result(name, success, message=""):
    status = "SUCCESS" if success else "FAILED"
    print(f"[{status}] {name}: {message}")

def test_transpose():
    print("\n--- Testing transpose(A) ---")
    test_cases = [
        {"name": "Square Matrix", "input": [[1, 2], [3, 4]], "expected": [[1, 3], [2, 4]]},
        {"name": "Row Vector", "input": [[1, 2, 3]], "expected": [[1], [2], [3]]},
        {"name": "Column Vector", "input": [[1], [2], [3]], "expected": [[1, 2, 3]]},
        {"name": "Identity Matrix", "input": [[1, 0], [0, 1]], "expected": [[1, 0], [0, 1]]},
        {"name": "Zero Matrix", "input": [[0, 0], [0, 0]], "expected": [[0, 0], [0, 0]]}
    ]
    
    for case in test_cases:
        result = transpose(case["input"])
        success = is_close(result, case["expected"])
        print_test_result(case["name"], success)

def test_matmul():
    print("\n--- Testing matmul(A, B) ---")
    test_cases = [
        {"name": "Identity multiplication", "A": [[1, 2], [3, 4]], "B": [[1, 0], [0, 1]], "expected": [[1, 2], [3, 4]]},
        {"name": "Square matrices", "A": [[1, 2], [3, 4]], "B": [[2, 0], [1, 2]], "expected": [[4, 4], [10, 8]]},
        {"name": "Rectangular (2x3 * 3x2)", "A": [[1, 0, 1], [0, 2, 1]], "B": [[1, 2], [3, 4], [0, 1]], "expected": [[1, 3], [6, 9]]},
        {"name": "Zero multiplication", "A": [[1, 2], [3, 4]], "B": [[0, 0], [0, 0]], "expected": [[0, 0], [0, 0]]},
        {"name": "All ones", "A": [[1, 1]], "B": [[1], [1]], "expected": [[2]]}
    ]
    
    for case in test_cases:
        result = matmul(case["A"], case["B"])
        success = is_close(result, case["expected"])
        print_test_result(case["name"], success)

def test_compute_ata():
    print("\n--- Testing compute_ata(A) ---")
    test_cases = [
        {"name": "Identity", "input": [[1, 0], [0, 1]], "expected": [[1, 0], [0, 1]]},
        {"name": "2x1 Matrix", "input": [[1], [2]], "expected": [[5]]},
        {"name": "1x2 Matrix", "input": [[1, 2]], "expected": [[1, 2], [2, 4]]},
        {"name": "Zero Matrix", "input": [[0, 0], [0, 0]], "expected": [[0, 0], [0, 0]]},
        {"name": "All ones 2x2", "input": [[1, 1], [1, 1]], "expected": [[2, 2], [2, 2]]}
    ]
    
    for case in test_cases:
        result = compute_ata(case["input"])
        success = is_close(result, case["expected"])
        print_test_result(case["name"], success)

def test_eigen_decomposition():
    print("\n--- Testing eigen_decomposition(A) ---")
    # Kiểm tra tính đúng đắn qua định nghĩa: A * v = lambda * v
    test_cases = [
        {"name": "Identity 2x2", "input": [[1, 0], [0, 1]]},
        {"name": "Diagonal Matrix", "input": [[2, 0], [0, 5]]},
        {"name": "Symmetric 2x2", "input": [[2, 1], [1, 2]]}, # Eigenvalues 3, 1
        {"name": "Singular Symmetric", "input": [[1, 1], [1, 1]]}, # Eigenvalues 2, 0
        {"name": "Symmetric 3x3", "input": [[4, 2, 2], [2, 4, 2], [2, 2, 4]]} # Eigenvalues 8, 2, 2
    ]
    
    for case in test_cases:
        evals, evecs = eigen_decomposition(case["input"])
        # Verification: A * V == V * D
        # Transpose evecs to get columns back if needed, but in our implementation, evecs are COLUMNS
        # Let's verify each: A * v_i = lambda_i * v_i
        valid = True
        n = len(case["input"])
        for i in range(n):
            lambda_i = evals[i]
            v_i = [[evecs[j][i]] for j in range(n)] # column vector i
            
            # Left side: A * v_i
            left = matmul(case["input"], v_i)
            # Right side: lambda_i * v_i
            right = [[lambda_i * v_i[j][0]] for j in range(n)]
            
            if not is_close(left, right):
                valid = False
                break
        
        print_test_result(case["name"], valid)

def test_sort_eigenpairs():
    print("\n--- Testing sort_eigenpairs() ---")
    test_cases = [
        {
            "name": "Unsorted mixture",
            "evals": [1, 5, 2],
            "evecs": [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
            "expected_evals": [5, 2, 1],
            "expected_evecs": [[1, 0, 0], [0, 0, 1], [0, 1, 0]]
        },
        {
            "name": "Already sorted",
            "evals": [10, 5, 1],
            "evecs": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "expected_evals": [10, 5, 1],
            "expected_evecs": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        },
        {
            "name": "Duplicate values",
            "evals": [2, 1, 2],
            "evecs": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "expected_evals": [2, 2, 1],
            "expected_evecs": [[1, 0, 0], [0, 0, 1], [0, 1, 0]]
        },
        {
            "name": "Single element",
            "evals": [5],
            "evecs": [[1]],
            "expected_evals": [5],
            "expected_evecs": [[1]]
        },
        {
            "name": "All zeros",
            "evals": [0, 0],
            "evecs": [[1, 0], [0, 1]],
            "expected_evals": [0, 0],
            "expected_evecs": [[1, 0], [0, 1]]
        }
    ]
    
    for case in test_cases:
        res_evals, res_evecs = sort_eigenpairs(case["evals"], case["evecs"])
        success = is_close(res_evals, case["expected_evals"]) and is_close(res_evecs, case["expected_evecs"])
        print_test_result(case["name"], success)

if __name__ == "__main__":
    print("=== DIAGONALIZATION TESTING SYSTEM ===")
    test_transpose()
    test_matmul()
    test_compute_ata()
    test_eigen_decomposition()
    test_sort_eigenpairs()
    print("\n=== TESTING COMPLETED ===")
