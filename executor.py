
import json
import subprocess
import sys
import tempfile
import os


TIMEOUT_SECONDS = 5


def execute_python_code(code):
    """Execute Python code and return its output."""

    if not isinstance(code, str) or not code.strip():
        return {
            "success": False,
            "output": "",
            "error": "Please provide valid Python code.",
            "return_code": None
        }

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
            timeout=TIMEOUT_SECONDS
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
            try:
                os.remove(temp_file)
            except OSError:
                pass


def run_function_tests(code, function_name, test_cases):
    """Execute function tests and generate a pass/fail report."""

    temp_file = None

    try:
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Python code cannot be empty.")

        if not isinstance(function_name, str):
            raise ValueError("Function name must be a string.")

        if not function_name.isidentifier():
            raise ValueError("Invalid function name.")

        if not isinstance(test_cases, list) or not test_cases:
            raise ValueError("No test cases provided.")

        for index, case in enumerate(test_cases, start=1):

            if not isinstance(case, dict):
                raise ValueError(
                    f"Test case {index} must be a dictionary."
                )

            if not isinstance(case.get("args"), list):
                raise ValueError(
                    f"Test case {index} must contain an args list."
                )

            if "expected" not in case:
                raise ValueError(
                    f"Test case {index} is missing expected output."
                )

        # Build isolated test runner process.
        runner_code = f'''
import json
import traceback

namespace = {{}}

try:
    exec({code!r}, namespace)

    function = namespace.get({function_name!r})

    if not callable(function):
        raise ValueError(
            "Function not found: {function_name}"
        )

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

        print(
            "SMART_TEST_RESULT:"
            + json.dumps(result, default=str)
        )

except Exception as error:
    print(
        "SMART_TEST_ERROR:"
        + str(error)
    )
    raise
'''

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
            timeout=TIMEOUT_SECONDS
        )

        results = []
        runner_error = ""

        for line in process.stdout.splitlines():

            if line.startswith("SMART_TEST_RESULT:"):

                result_json = line.split(
                    "SMART_TEST_RESULT:", 1
                )[1]

                results.append(json.loads(result_json))

            elif line.startswith("SMART_TEST_ERROR:"):

                runner_error = line.split(
                    "SMART_TEST_ERROR:", 1
                )[1]

        if process.returncode != 0:

            return {
                "success": False,
                "results": results,
                "error": (
                    runner_error
                    or process.stderr
                    or "Test runner failed."
                )
            }

        if len(results) != len(test_cases):

            return {
                "success": False,
                "results": results,
                "error": (
                    runner_error
                    or "Some test results were missing."
                )
            }

        passed_count = sum(
            1 for result in results
            if result.get("passed")
        )

        all_passed = passed_count == len(test_cases)

        return {
            "success": all_passed,
            "results": results,
            "error": "" if all_passed else (
                f"{len(test_cases) - passed_count} test(s) failed."
            )
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "results": [],
            "error": "Test execution timed out after 5 seconds."
        }

    except Exception as error:
        return {
            "success": False,
            "results": [],
            "error": str(error)
        }

    finally:
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass
