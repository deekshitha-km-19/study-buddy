# 🤖 SMART CODING AGENT

### AI Coding, Validation & Testing

**Smart Coding Agent** is an AI-powered Python assistant designed to help developers generate, validate, debug, explain, and test Python code using AI.

## 🚀 Features

- **AI Code Generator** – Generate Python code from natural-language prompts.
- **Syntax Validation** – Identify Python syntax errors.
- **AI Test Case Generation** – Generate test cases for Python functions.
- **Automatic Test Execution** – Execute test cases and compare actual and expected results.
- **Test Report Dashboard** – View passed tests, failed tests, and success rate.
- **AI Code Debugger** – Identify errors and suggest corrected code.
- **AI Code Explainer** – Understand Python code step by step.
- **Python Code Executor** – Execute Python code and view the output.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google GenAI SDK
- Python-dotenv

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_SMART_CODING_AGENT_GITHUB_URL
```

### 2. Open the project folder

```bash
cd YOUR_PROJECT_FOLDER
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API key

Create a `.env` file in the project folder:

```env
GEMINI_API_KEY=your_api_key_here
```

Keep your actual API key private. Never upload `.env` to GitHub.

### 5. Run the application

```bash
streamlit run app_black_theme.py
```

## 🧪 Example Python Testing

Example function to check whether a number is prime:

```python
def is_prime(n):
    if n <= 1:
        return False

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True
```

### Example Test Cases

| Input | Expected Output |
|---|---|
| `is_prime(7)` | `True` |
| `is_prime(10)` | `False` |
| `is_prime(13)` | `True` |
| `is_prime(1)` | `False` |
| `is_prime(2)` | `True` |

## ⚠️ Security Notice

The Python code executor is a prototype and is not a secure sandbox. Execute only trusted code. Do not use it to run untrusted code in a public deployment.

## 👩‍💻 Developed By

**ABDH**

Global AI Hackathon | Smart Coding Agent