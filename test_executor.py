
from executor import execute_python_code

code = """
number = 10
if number > 5:
    print("Number is greater than 5")
else:
    print("Number is smaller or equal to 5")
"""

result = execute_python_code(code)

print("Execution successful:", result["success"])
print("Program output:")
print(result["output"])

if result["error"]:
    print("Error:")
    print(result["error"])
