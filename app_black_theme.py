
import streamlit as st
import ast
import re

from agent import generate_code, debug_code, explain_code
from executor import execute_python_code, run_function_tests


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ABDH | Smart Coding Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULTS = {
    "generated_code": "",
    "generation_response": "",
    "generated_tests": "",
    "debug_result": "",
    "explanation_result": "",
    "execution_result": None,
    "test_report": None,
    "page": "Dashboard",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# PREMIUM UI THEME
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 80% 0%, #21133c 0%, transparent 35%),
        linear-gradient(135deg, #080810, #10101d);
    color: #f5f3ff;
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

h1, h2, h3, h4 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

p, li, label {
    color: #d9d4e7;
}

[data-testid="stSidebar"] {
    background: #100e1a;
    border-right: 1px solid #35244f;
}

[data-testid="stSidebar"] * {
    color: #eee9ff;
}

[data-testid="stSidebar"] .stRadio label {
    padding: 9px;
    border-radius: 9px;
}

.stTextArea textarea,
.stTextInput input {
    background: #191426 !important;
    color: #ffffff !important;
    border: 1px solid #6845a9 !important;
    border-radius: 12px !important;
    caret-color: #00e5ff !important;
}

.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #a99bbd !important;
}

.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: #00e5ff !important;
    box-shadow: 0 0 10px #00e5ff33 !important;
}

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(100deg, #7045c7, #47218c);
    color: white !important;
    border: 1px solid #9870e8;
    border-radius: 10px;
    padding: 0.55rem 1rem;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(100deg, #00bcd4, #7045c7);
    border-color: #00e5ff;
    transform: translateY(-1px);
}

[data-testid="stMetric"] {
    background: #191426;
    border: 1px solid #49316d;
    padding: 17px;
    border-radius: 13px;
}

[data-testid="stMetricValue"] {
    color: #00e5ff;
}

.stCodeBlock {
    border: 1px solid #563b80;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    color: #d0b9f5;
}

.stTabs [aria-selected="true"] {
    color: #00e5ff !important;
}

.stAlert {
    border-radius: 12px;
}

hr {
    border-color: #39284e;
}

.hero-card {
    background: linear-gradient(120deg, #211339, #151326);
    border: 1px solid #6845a9;
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 22px;
}

.hero-label {
    color: #00e5ff;
    font-weight: 700;
    letter-spacing: 2px;
    font-size: 12px;
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    color: white;
    margin-top: 8px;
}

.hero-subtitle {
    color: #c7b5eb;
    font-size: 15px;
    margin-top: 8px;
}

.feature-card {
    background: #171323;
    border: 1px solid #44315f;
    border-radius: 14px;
    padding: 18px;
    min-height: 125px;
}

.feature-title {
    color: #ffffff;
    font-weight: 700;
    font-size: 16px;
}

.feature-description {
    color: #b9accf;
    font-size: 13px;
    margin-top: 8px;
}

.small-caption {
    color: #9c8eb5;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def extract_python_code(response):
    """Extract Python code from Gemini response."""

    if not response:
        return None

    matches = re.findall(
        r"```(?:python)?\s*(.*?)```",
        str(response),
        re.DOTALL | re.IGNORECASE
    )

    if matches:
        return matches[0].strip()

    cleaned = str(response).strip()

    # Do not treat ordinary explanations as executable code.
    try:
        ast.parse(cleaned)
        return cleaned
    except SyntaxError:
        return None


def validate_python_code(code):
    try:
        ast.parse(code)
        return True, "Python syntax is valid."
    except SyntaxError as error:
        return False, f"Line {error.lineno}: {error.msg}"
    except Exception as error:
        return False, str(error)


def show_execution_result(result):
    if not result:
        st.warning("No execution result available.")
        return

    if not isinstance(result, dict):
        st.error("Unexpected execution result format.")
        st.write(result)
        return

    if result.get("success"):
        st.success("Code executed successfully!")

        output = result.get("output")

        if output:
            st.code(output, language="text")
        else:
            st.info("Code executed without producing output.")

    else:
        st.error("Code execution failed.")

        if result.get("error"):
            st.code(result["error"], language="text")


def page_header(title, description):
    st.markdown(f"## {title}")
    st.markdown(
        f"<p style='color:#a99bbd'>{description}</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown(
        "<h1 style='color:#a879ff'>🤖 ABDH</h1>",
        unsafe_allow_html=True
    )

    st.caption("SMART CODING AGENT")

    st.markdown("---")
    st.markdown("### WORKSPACE")

    pages = [
        "Dashboard",
        "AI Code Generator",
        "AI Debugger",
        "Code Explainer",
        "Automatic Testing",
        "Python Executor",
    ]

    selected_page = st.radio(
        "Navigation",
        pages,
        key="page",
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### TECHNOLOGY")

    st.markdown("""
    🐍 Python

    ⚡ Streamlit

    🧠 Google Gemini AI

    🔍 AST Validation
    """)

    st.markdown("---")

    st.caption("GLOBAL AI HACKATHON")
    st.caption("Developed by ABDH")


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero-card">
    <div class="hero-label">GLOBAL AI HACKATHON · ABDH</div>
    <div class="hero-title">🤖 SMART CODING AGENT</div>
    <div class="hero-subtitle">
        Your intelligent AI workspace for coding,
        debugging, testing and learning Python.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# DASHBOARD
# =========================================================

if selected_page == "Dashboard":

    page_header(
        "🚀 Dashboard",
        "Welcome to your AI-powered development workspace."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Generated Code",
        "Ready" if st.session_state["generated_code"] else "0"
    )

    col2.metric(
        "AI Debugger",
        "Ready"
    )

    col3.metric(
        "Code Executor",
        "Ready"
    )

    st.markdown("### Explore your workspace")

    row1 = st.columns(2)

    with row1[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">💻 AI Code Generator</div>
            <div class="feature-description">
                Generate Python code using natural language prompts.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with row1[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🐞 AI Debugger</div>
            <div class="feature-description">
                Analyze errors and receive corrected code suggestions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    row2 = st.columns(2)

    with row2[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📖 Code Explainer</div>
            <div class="feature-description">
                Understand Python code with beginner-friendly explanations.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with row2[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🧪 Automatic Testing</div>
            <div class="feature-description">
                Generate and run function test cases.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Current generated code")

    if st.session_state["generated_code"]:
        st.code(
            st.session_state["generated_code"],
            language="python"
        )
    else:
        st.info("No code generated yet. Open AI Code Generator to begin.")


# =========================================================
# AI CODE GENERATOR
# =========================================================

elif selected_page == "AI Code Generator":

    page_header(
        "💻 AI Code Generator",
        "Describe your task and generate Python code with Gemini AI."
    )

    task = st.text_area(
        "Describe your coding task",
        placeholder="Example: Create a Python program to check prime numbers.",
        height=130,
        key="coding_task"
    )

    if st.button("✨ Generate Python Code", use_container_width=True):

        if not task.strip():
            st.warning("Please enter a coding task.")

        else:
            with st.spinner("Gemini AI is generating your code..."):

                response = generate_code(task)

                st.session_state["generation_response"] = str(response)

                extracted = extract_python_code(response)

                if extracted:
                    st.session_state["generated_code"] = extracted
                    st.session_state["generated_tests"] = ""
                    st.session_state["test_report"] = None
                    st.session_state["execution_result"] = None
                    st.success("Code generated successfully!")
                else:
                    st.warning(
                        "Could not identify a valid Python code block. "
                        "Check the complete AI response below."
                    )

    if st.session_state["generated_code"]:

        st.markdown("### Generated Python Code")

        st.code(
            st.session_state["generated_code"],
            language="python"
        )

        st.download_button(
            "⬇️ Download Python File",
            data=st.session_state["generated_code"],
            file_name="generated_code.py",
            mime="text/x-python"
        )

        valid, message = validate_python_code(
            st.session_state["generated_code"]
        )

        if valid:
            st.success(message)
        else:
            st.error(message)

    if st.session_state["generation_response"]:
        with st.expander("View complete AI response"):
            st.markdown(st.session_state["generation_response"])


# =========================================================
# AI DEBUGGER
# =========================================================

elif selected_page == "AI Debugger":

    page_header(
        "🐞 AI Code Debugger",
        "Find programming errors and get corrected code suggestions."
    )

    debug_input = st.text_area(
        "Paste your Python code",
        placeholder="""def greet():
    print("Hello")

if True
    greet()
""",
        height=220,
        key="debug_input"
    )

    if st.button("🔧 Debug My Code", use_container_width=True):

        if not debug_input.strip():
            st.warning("Please enter Python code.")

        else:
            with st.spinner("AI is analyzing your code..."):
                st.session_state["debug_result"] = debug_code(debug_input)

    if st.session_state["debug_result"]:
        st.markdown("### Debugging Analysis")
        st.markdown(st.session_state["debug_result"])


# =========================================================
# CODE EXPLAINER
# =========================================================

elif selected_page == "Code Explainer":

    page_header(
        "📖 AI Code Explainer",
        "Understand Python programs with simple explanations."
    )

    explain_input = st.text_area(
        "Paste Python code to explain",
        placeholder="""def add(a, b):
    return a + b

print(add(5, 10))
""",
        height=220,
        key="explain_input"
    )

    if st.button("📚 Explain My Code", use_container_width=True):

        if not explain_input.strip():
            st.warning("Please enter Python code.")

        else:
            with st.spinner("Gemini AI is explaining your code..."):
                st.session_state["explanation_result"] = explain_code(
                    explain_input
                )

    if st.session_state["explanation_result"]:
        st.markdown("### Code Explanation")
        st.markdown(st.session_state["explanation_result"])


# =========================================================
# AUTOMATIC TESTING
# =========================================================

elif selected_page == "Automatic Testing":

    page_header(
        "🧪 Automatic Testing",
        "Generate suggested test cases and execute function tests."
    )

    code = st.session_state["generated_code"]

    if not code:
        st.info("Generate Python code first using AI Code Generator.")

    else:

        st.markdown("### Current generated function")
        st.code(code, language="python")

        if st.button("✨ Generate Test Cases", use_container_width=True):

            prompt = f"""
You are a Python software testing expert.

Analyze this Python code:

{code}

Generate:
1. Normal test case.
2. Boundary test case.
3. Edge test case.

Show function name, input and expected output.
Use a Markdown table.

Do not claim that tests were executed.
"""

            with st.spinner("Generating test cases..."):
                st.session_state["generated_tests"] = generate_code(prompt)

        if st.session_state["generated_tests"]:
            st.markdown("### AI-generated test cases")
            st.markdown(st.session_state["generated_tests"])
            st.caption(
                "These are AI suggestions and are not necessarily executed."
            )

        st.markdown("---")
        st.markdown("### Execute function tests")

        function_name = st.text_input(
            "Function name",
            placeholder="Enter the actual function name",
            key="test_function_name"
        )

        st.warning(
            "Enter the function name from your generated code. "
            "The test inputs and expected outputs must match that function."
        )

        test_inputs = st.text_area(
            "Test cases configuration",
            value="""[
    {"args": [10], "expected": 11},
    {"args": [1], "expected": 2},
    {"args": [-5], "expected": 2}
]""",
            height=150,
            key="test_cases_json"
        )

        if st.button("▶️ Run Function Tests", use_container_width=True):

            import json

            try:
                test_cases = json.loads(test_inputs)

                if not isinstance(test_cases, list):
                    raise ValueError("Test cases must be a JSON list.")

                if not function_name.strip():
                    st.warning("Enter a function name.")
                else:
                    with st.spinner("Running function tests..."):

                        report = run_function_tests(
                            code,
                            function_name.strip(),
                            test_cases
                        )

                        st.session_state["test_report"] = report

            except Exception as error:
                st.error(f"Test execution failed: {error}")

        if st.session_state["test_report"]:

            report = st.session_state["test_report"]

            if not isinstance(report, dict):
                st.error("Unexpected test report format.")
            else:
                results = report.get("results", [])

                total = len(results)
                passed = sum(
                    1 for item in results if item.get("passed")
                )
                failed = total - passed

                rate = (passed / total * 100) if total else 0

                st.markdown("### 📊 Test Report")

                c1, c2, c3, c4 = st.columns(4)

                c1.metric("Total", total)
                c2.metric("Passed", passed)
                c3.metric("Failed", failed)
                c4.metric("Success Rate", f"{rate:.1f}%")

                st.progress(rate / 100 if total else 0)

                for index, item in enumerate(results, start=1):

                    if item.get("passed"):
                        st.success(f"Test {index}: PASSED")
                    else:
                        st.error(f"Test {index}: FAILED")

                    st.write("Input:", item.get("args"))
                    st.write("Expected:", item.get("expected"))
                    st.write("Actual:", item.get("actual"))
                    st.markdown("---")


# =========================================================
# PYTHON EXECUTOR
# =========================================================

elif selected_page == "Python Executor":

    page_header(
        "🚀 Python Code Executor",
        "Execute Python programs and inspect their output."
    )

    manual_code = st.text_area(
        "Python code editor",
        placeholder="""name = "ABDH"

print("Welcome", name)
print("Smart Coding Agent is working!")
""",
        height=260,
        key="manual_code"
    )

    st.warning(
        "Security notice: This executor may run code with the "
        "application's permissions. Do not execute untrusted code. "
        "Use an isolated sandbox for public deployment."
    )

    if st.button("▶️ Execute Python Code", use_container_width=True):

        if not manual_code.strip():
            st.warning("Please enter Python code.")

        else:
            with st.spinner("Executing Python code..."):

                try:
                    st.session_state["execution_result"] = (
                        execute_python_code(manual_code)
                    )

                except Exception as error:
                    st.session_state["execution_result"] = {
                        "success": False,
                        "error": str(error)
                    }

    if st.session_state["execution_result"]:
        st.markdown("### Execution Result")
        show_execution_result(
            st.session_state["execution_result"]
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<div style="
    text-align:center;
    padding:25px;
    background:#151122;
    border:1px solid #39284e;
    border-radius:15px;
">
    <h3 style="color:#a879ff;">🤖 SMART CODING AGENT</h3>
    <p style="color:#00e5ff;">
        AI Coding · Debugging · Testing · Code Explanation
    </p>
    <p style="color:#ffffff;">DEVELOPED BY ABDH</p>
    <p style="color:#999999;font-size:12px;">
        GLOBAL AI HACKATHON
    </p>
</div>
""", unsafe_allow_html=True)
