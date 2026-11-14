
from executor import execute_python_code


def test_successful_execution():
    code = """
number = 10

if number > 5:
    print("Number is greater than 5")
else:
    print("Number is smaller or equal to 5")
"""

    result = execute_python_code(code)

    print("\n===== TEST 1: SUCCESSFUL EXECUTION =====")
    print("Execution successful:", result["success"])
    print("Program output:")
    print(result["output"])

    if result["error"]:
        print("Error:", result["error"])


def test_syntax_error():
    code = """
if 10 > 5
    print("Hello")
"""

    result = execute_python_code(code)

    print("\n===== TEST 2: SYNTAX ERROR =====")
    print("Execution successful:", result["success"])
    print("Error detected:", bool(result["error"]))


def test_empty_code():
    code = ""

    result = execute_python_code(code)

    print("\n===== TEST 3: EMPTY CODE =====")
    print("Execution successful:", result["success"])
    print("Output:", result["output"])


if __name__ == "__main__":
    test_successful_execution()
    test_syntax_error()
    test_empty_code()
