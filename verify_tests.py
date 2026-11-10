
from generated_code import is_prime

# Test cases
test_cases = [
    (11, True),
    (2, True),
    (1, False),
    (0, False),
    (-7, False),
    (9, False)
]

print("\n===== AUTOMATIC TEST EXECUTION =====\n")

passed = 0
failed = 0

for number, expected in test_cases:

    actual = is_prime(number)

    if actual == expected:
        print(f"PASS: Input {number}")
        passed += 1
    else:
        print(f"FAIL: Input {number}")
        print(f"Expected: {expected}, Got: {actual}")
        failed += 1

print("\n===== TEST SUMMARY =====")
print("Total Tests:", len(test_cases))
print("Passed:", passed)
print("Failed:", failed)

if failed == 0:
    print("\nALL TESTS PASSED SUCCESSFULLY!")
else:
    print("\nSOME TESTS FAILED!")
