
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Load environment variables
load_dotenv()

# Gemini configuration
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.8-flash"

# Create client only when needed
_client = None


def get_client():
    global _client

    if not API_KEY:
        raise ValueError(
            "Gemini API key missing. Please check your .env file."
        )

    if _client is None:
        _client = genai.Client(api_key=API_KEY)

    return _client


def generate_response(prompt, retries=3):
    """Common Gemini API function with error handling."""

    try:
        client = get_client()

        for attempt in range(retries):
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt
                )

                if response.text:
                    return response.text

                return "Gemini returned an empty response."

            except errors.ServerError:
                if attempt == retries - 1:
                    return "Gemini server is busy. Please try again later."

                time.sleep(2 * (attempt + 1))

    except ValueError as error:
        return str(error)

    except Exception as error:
        return f"Gemini API error: {error}"


# ==========================================
# 1. AI CODE GENERATION
# ==========================================

def generate_code(task):

    if not task or not task.strip():
        return "Please enter a coding task."

    prompt = f"""
You are an expert Python coding assistant.

User Task:
{task}

Provide the following:

1. Correct and complete Python code.
2. Simple explanation.
3. Sample output.
4. Efficient solution.
5. Important edge cases.

Rules:
- Write beginner-friendly Python code.
- Use proper indentation.
- Include comments where necessary.
- Make sure the code is logically correct.
"""

    return generate_response(prompt)


# ==========================================
# 2. AI CODE DEBUGGER
# ==========================================

def debug_code(code):

    if not code or not code.strip():
        return "Please provide Python code to debug."

    prompt = f"""
You are an expert Python debugging assistant.

Analyze the following Python code.

Provide:

1. Errors found in the code.
2. Explanation of each error.
3. Corrected complete Python code.
4. Explanation of the corrections.
5. Suggestions to prevent similar errors.

If the code has no errors, explain that clearly.

Python Code:
```python
{code}
```
"""

    return generate_response(prompt)


# ==========================================
# 3. AI CODE EXPLANATION
# ==========================================

def explain_code(code):

    if not code or not code.strip():
        return "Please provide Python code to explain."

    prompt = f"""
You are an expert Python programming teacher.

Explain this Python code to a beginner.

Provide:

1. What does the program do?
2. Explain each line.
3. Explain the Python concepts used.
4. Give a simple dry run.
5. Explain the expected output.
6. Give one practical example.

Use simple English and beginner-friendly explanations.

Python Code:
```python
{code}
```
"""

    return generate_response(prompt)


# ==========================================
# 4. AI CODE REVIEW
# ==========================================

def review_code(code):

    if not code or not code.strip():
        return "Please provide code for review."

    prompt = f"""
You are a professional Python code reviewer.

Review the following code.

Check:

1. Code quality.
2. Bugs and logical errors.
3. Performance.
4. Security concerns.
5. Readability.
6. Best practices.

Give:
- Overall review.
- Issues found.
- Improvement suggestions.
- Improved code if necessary.

Python Code:
```python
{code}
```
"""

    return generate_response(prompt)
