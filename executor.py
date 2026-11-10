import json
import subprocess
import sys
import tempfile
import os


def execute_python_code(code):
    temp_file = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as file:
            file.write(code)
            temp_file = file.name

        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Execution timed out after 5 seconds.",
            "return_code": None
        }

    except Exception as error:
        return {
            "success": False,
            "output": "",
            "error": str(error),
            "return_code": None
        }

    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)

def run_function_tests(code, function_name, test_cases):
    import json
    import subprocess
    import sys
    import tempfile
    import os

    temp_file = None

    try:
        if not function_name.isidentifier():
            raise ValueError("Invalid function name.")

        if not isinstance(test_cases, list) or not test_cases:
            raise ValueError("No test cases provided.")

        # Prepare the automatic test runner
        runner_code = f"""
import json

namespace = {{}}

exec({code!r}, namespace)

function = namespace.get({function_name!r})

if not callable(function):
    raise ValueError("Function not found: {function_name}")

test_cases = {test_cases!r}

for index, case in enumerate(test_cases, 1):
    try:
        actual = function(*case["args"])
        expected = case["expected"]

        passed = actual == expected

        result = {{
            "test": index,
            "args": case["args"],
            "expected": expected,
            "actual": actual,
            "passed": passed
        }}

    except Exception as error:
        result = {{
            "test": index,
            "args": case.get("args", []),
            "expected": case.get("expected"),
            "actual": str(error),
            "passed": False
        }}

    print("SMART_TEST_RESULT:" + json.dumps(result))
"""

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as file:

            file.write(runner_code)
            temp_file = file.name

        process = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )

        results = []

        for line in process.stdout.splitlines():
            if line.startswith("SMART_TEST_RESULT:"):
                result_json = line.replace(
                    "SMART_TEST_RESULT:", "", 1
                )
                results.append(json.loads(result_json))

        if process.returncode != 0:
            return {
                "success": False,
                "results": results,
                "error": process.stderr or "Test execution failed."
            }

        return {
            "success": True,
            "results": results,
            "error": ""
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "results": [],
            "error": "Test execution timed out."
        }

    except Exception as error:
        return {
            "success": False,
            "results": [],
            "error": str(error)
        }

    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
