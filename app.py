
import streamlit as st
import ast
import re

from agent import generate_code, debug_code, explain_code
from executor import execute_python_code, run_function_tests


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Smart Coding Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 SMART CODING AGENT")
st.subheader("AI Coding, Validation & Testing")

st.write(
    "Generate code, validate syntax, debug errors, "
    "explain Python code, create test cases and execute code."
)


# ---------------- SESSION STATE ----------------

if "result" not in st.session_state:
    st.session_state["result"] = None

if "task" not in st.session_state:
    st.session_state["task"] = ""

if "tests" not in st.session_state:
    st.session_state["tests"] = None

if "generated_code" not in st.session_state:
    st.session_state["generated_code"] = None


# ---------------- CODE EXTRACTION ----------------

def extract_python_code(response):
    pattern = r"```(?:python)?\s*(.*?)```"

    matches = re.findall(
        pattern,
        response,
        re.DOTALL | re.IGNORECASE
    )

    return matches[0].strip() if matches else None


# ---------------- CODE GENERATION ----------------

st.header("💻 AI Code Generator")

task = st.text_area(
    "Enter your coding task:",
    placeholder="Example: Write a Python program to check prime numbers.",
    height=120
)

if st.button("🚀 Generate Code", use_container_width=True):

    if not task.strip():
        st.warning("Please enter a coding task.")

    else:
        with st.spinner("Gemini AI is generating code..."):

            result = generate_code(task)

        if not result or result.startswith("Gemini server is busy"):
            st.error(result or "No response received.")

        else:
            st.session_state["result"] = result
            st.session_state["task"] = task
            st.session_state["tests"] = None
            st.session_state["generated_code"] = None

            st.rerun()


# ---------------- DISPLAY GENERATED CODE ----------------

if st.session_state["result"]:

    result = st.session_state["result"]

    st.success("Code generated successfully!")

    st.subheader("🧠 AI Generated Solution")
    st.markdown(result)

    code = extract_python_code(result)

    if code:

        st.session_state["generated_code"] = code

        # ---------------- SYNTAX VALIDATION ----------------

        st.divider()
        st.subheader("🔍 Syntax Validation")

        try:
            ast.parse(code)
            st.success("Python syntax is valid!")

        except SyntaxError as error:
            st.error(f"Syntax error: {error}")

        st.code(code, language="python")

        # ---------------- DOWNLOAD CODE ----------------

        st.download_button(
            "⬇️ Download Python Code",
            data=code,
            file_name="generated_code.py",
            mime="text/x-python"
        )

        # ---------------- TEST CASE GENERATION ----------------

        st.divider()
        st.subheader("🧪 Automatic Test Case Generation")

        if st.button("Generate Test Cases", use_container_width=True):

            test_prompt = f"""
You are a software testing expert.

Original task:
{st.session_state['task']}

Generated Python solution:
{code}

Generate exactly 3 useful test cases:
1. Normal input
2. Boundary input
3. Edge case

For each test case provide:
- Input
- Expected output
- Explanation

Present the result in a clear Markdown table.
Do not execute the code.
"""

            with st.spinner("AI is creating test cases..."):

                tests = generate_code(test_prompt)

            st.session_state["tests"] = tests

            st.rerun()

        if st.session_state["tests"]:

            st.success("Test cases generated!")
            st.markdown(st.session_state["tests"])

            st.info(
                "These are AI-generated expected results. "
                "They have not yet been executed or verified."
            )


        # ---------------- AUTOMATIC TEST EXECUTION ----------------

        st.divider()
        st.subheader("🧪 Automatic Test Execution")

        function_name = st.text_input(
            "Function name to test:",
            value="generate_prime_above"
        )

        test_cases = [
            {"args": [10], "expected": 11},
            {"args": [1], "expected": 2},
            {"args": [-5], "expected": 2}
        ]

        st.write("Test cases to execute:")

        st.code(
            """
Test 1: generate_prime_above(10) -> 11
Test 2: generate_prime_above(1)  -> 2
Test 3: generate_prime_above(-5) -> 2
""",
            language="text"
        )

        if st.button(
            "▶️ Run Automatic Tests",
            use_container_width=True
        ):

            if not function_name.strip():
                st.warning("Enter a function name.")

            else:
                with st.spinner("Executing automatic tests..."):

                    test_report = run_function_tests(
                        code,
                        function_name.strip(),
                        test_cases
                    )

                if test_report["success"]:

                    results = test_report["results"]

                    passed = sum(
                        1 for result in results if result["passed"]
                    )

                    failed = len(results) - passed

                    
                    st.subheader("📊 Test Report Dashboard")

                    total = len(results)
                    success_rate = (passed / total * 100) if total else 0

                    # Dashboard metrics
                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric("Total Tests", total)
                    col2.metric("Passed", passed)
                    col3.metric("Failed", failed)
                    col4.metric(
                        "Success Rate",
                        f"{success_rate:.1f}%"
                    )

                    # Visual progress
                    st.write("### Test Success Progress")
                    st.progress(success_rate / 100)

                    if failed == 0:
                        st.success("🎉 All automatic tests passed!")
                    else:
                        st.warning(f"{failed} test(s) failed.")

                    # Downloadable report
                    report = f"""
SMART CODING AGENT - TEST REPORT

Function: {function_name}

Total Tests: {total}
Passed: {passed}
Failed: {failed}
Success Rate: {success_rate:.1f}%

DETAILED RESULTS
"""

                    for result in results:
                        status = "PASS" if result["passed"] else "FAIL"

                        report += (
                            f"\nTest {result['test']}: {status}"
                            f"\nInput: {result['args']}"
                            f"\nExpected: {result['expected']}"
                            f"\nActual: {result['actual']}\n"
                        )

                    st.download_button(
                        label="⬇️ Download Test Report",
                        data=report,
                        file_name="smart_coding_agent_test_report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )


                    col1, col2, col3 = st.columns(3)

                    col1.metric("Total Tests", len(results))
                    col2.metric("Passed", passed)
                    col3.metric("Failed", failed)

                    for result in results:

                        if result["passed"]:
                            st.success(
                                f"PASS - Test {result['test']} | "
                                f"Input: {result['args']} | "
                                f"Expected: {result['expected']} | "
                                f"Actual: {result['actual']}"
                            )
                        else:
                            st.error(
                                f"FAIL - Test {result['test']} | "
                                f"Input: {result['args']} | "
                                f"Expected: {result['expected']} | "
                                f"Actual: {result['actual']}"
                            )

                    if failed == 0:
                        st.success("🎉 All automatic tests passed!")
                    else:
                        st.warning(f"{failed} test(s) failed.")

                else:
                    st.error("Automatic test execution failed.")
                    st.code(test_report["error"])

        # ---------------- EXECUTE GENERATED CODE ----------------

        st.divider()
        st.subheader("🚀 Run Generated Code")

        st.warning(
            "Only execute code you trust. This prototype does not "
            "isolate code from your computer."
        )

        if st.button(
            "▶️ Execute Generated Code",
            use_container_width=True
        ):

            with st.spinner("Executing generated code..."):

                execution_result = execute_python_code(code)

            if execution_result["success"]:

                st.success("Generated code executed successfully!")

                st.subheader("📤 Actual Output")

                st.code(
                    execution_result["output"] or "No output produced.",
                    language="text"
                )

            else:
                st.error("Generated code execution failed!")

                st.subheader("⚠️ Error Details")

                st.code(
                    execution_result["error"] or "Unknown execution error.",
                    language="text"
                )

    else:
        st.warning(
            "No Python code block found in the AI response."
        )

# ---------------- AI CODE DEBUGGER ----------------

st.divider()
st.header("🐞 AI Code Debugger")

debug_input = st.text_area(
    "Paste Python code with an error:",
    placeholder="Paste your incorrect Python code here...",
    height=150,
    key="debug_input"
)

if st.button("🔧 Debug My Code", use_container_width=True):

    if not debug_input.strip():

        st.warning("Please enter Python code to debug.")

    else:

        with st.spinner("AI is analyzing your code..."):

            debug_result = debug_code(debug_input)

        st.subheader("🐞 Debugging Results")
        st.markdown(debug_result)


# ---------------- AI CODE EXPLAINER ----------------

st.divider()
st.header("📖 AI Code Explainer")

explain_input = st.text_area(
    "Paste Python code to understand:",
    placeholder="Paste your Python code here...",
    height=150,
    key="explain_input"
)

if st.button("📚 Explain My Code", use_container_width=True):

    if not explain_input.strip():

        st.warning("Please enter Python code to explain.")

    else:

        with st.spinner("AI is explaining your code..."):

            explanation = explain_code(explain_input)

        st.subheader("📖 Code Explanation")
        st.markdown(explanation)


# ---------------- STANDALONE CODE EXECUTOR ----------------

st.divider()
st.header("▶️ Python Code Executor")

manual_code = st.text_area(
    "Enter Python code to execute:",
    placeholder='print("Hello DEEKSHITHA!")',
    height=150,
    key="manual_code"
)

st.warning(
    "Execute only trusted code. This is not a secure sandbox."
)

if st.button("▶️ Run Python Code", use_container_width=True):

    if not manual_code.strip():

        st.warning("Please enter Python code.")

    else:

        try:
            with st.spinner("Running Python code..."):

                manual_result = execute_python_code(manual_code)

            if manual_result["success"]:

                st.success("Code executed successfully!")

                st.subheader("📤 Program Output")

                st.code(
                    manual_result["output"] or "No output produced.",
                    language="text"
                )

            else:

                st.error("Execution failed!")

                st.code(
                    manual_result["error"] or "Unknown execution error.",
                    language="text"
                )

        except Exception as error:
            st.error(f"Execution error: {error}")


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    "<h3 style='text-align:center;'>Developed by ABDH</h3>",
    unsafe_allow_html=True
)

st.caption(
    "Global AI Hackathon | Smart Coding Agent"
)
