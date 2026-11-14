
from generated_code import is_prime

test_cases = [
    (11, True),
    (2, True),
    (1, False),
    (0, False),
    (-7, False),
    (9, False)
]

print("\n===== SMART CODING AGENT =====")
print("===== AUTOMATIC TEST EXECUTION =====\n")

passed = 0
failed = 0

for number, expected in test_cases:
    try:
        actual = is_prime(number)

        if actual == expected:
            print(f"PASS: Input {number}")
            passed += 1
        else:
            print(f"FAIL: Input {number}")
            print(f"Expected: {expected}, Got: {actual}")
            failed += 1

    except Exception as error:
        print(f"ERROR: Input {number}")
        print("Reason:", error)
        failed += 1

total = len(test_cases)
success_rate = (passed / total) * 100

print("\n===== TEST SUMMARY =====")
print("Total Tests:", total)
print("Passed:", passed)
print("Failed:", failed)
print(f"Success Rate: {success_rate:.2f}%")

if failed == 0:
    print("\nALL TESTS PASSED SUCCESSFULLY!")
else:
    print("\nSOME TESTS FAILED!")
