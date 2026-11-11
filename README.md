
# 🤖 SMART CODING AGENT

### AI Coding, Validation & Testing

**Smart Coding Agent** is an AI-powered Python assistant designed to help developers generate, validate, debug, explain, and test Python code.

## 🚀 Features

- **AI Code Generator** – Generate Python code from natural-language prompts.
- **Syntax Validation** – Check Python code for syntax errors.
- **AI Test Case Generation** – Generate test cases for Python functions.
- **Automatic Test Execution** – Run test cases and check expected results.
- **Test Report Dashboard** – View passed tests, failed tests, and success rate.
- **AI Code Debugger** – Identify errors and suggest corrections.
- **AI Code Explainer** – Understand code step by step.
- **Python Code Executor** – Execute Python code.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google GenAI SDK
- Python-dotenv

## ⚙️ Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/deekshitha-km-19/study-buddy.git
   ```

2. Open the project folder:

   ```bash
   cd study-buddy
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project folder and add your Gemini API key:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

   Keep your actual API key private. Never upload `.env` to GitHub.

5. Run the application:

   ```bash
   streamlit run app.py
   ```

## 🧪 Testing

The project includes automatic test execution. Example test cases:

| Input | Expected Output |
|---|---:|
| `generate_prime_above(10)` | `11` |
| `generate_prime_above(1)` | `2` |
| `generate_prime_above(-5)` | `2` |

## ⚠️ Security Notice

The Python code executor is a prototype and is not a secure sandbox. Execute only trusted code.

## 👩‍💻 Developed By

**ABDH**

Global AI Hackathon | Smart Coding Agent
