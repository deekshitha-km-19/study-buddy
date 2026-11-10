
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API key missing. Check your .env file.")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash-lite"


def generate_code(task):

    prompt = f"""
    You are an expert Python coding assistant.

    Task: {task}

    Provide:
    1. Correct Python code.
    2. Simple explanation.
    3. Sample output.
    4. Efficient solution.
    """

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text

        except errors.ServerError:
            if attempt == 2:
                return "Gemini server is busy. Please try again later."

            time.sleep(5 * (attempt + 1))

def debug_code(code):
    prompt = f"""
You are an expert Python debugging assistant.

1. Find errors in the code.
2. Explain each error simply.
3. Provide corrected Python code.
4. Explain the correction.

Code:
{code}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text


def explain_code(code):
    prompt = f"""
You are an expert Python teacher.

Explain this code to a beginner.

1. What does the program do?
2. Explain each line.
3. Explain the Python concepts used.
4. Give a simple dry run.
5. Explain the output.

Python Code:
{code}
"""

    try:
        # Primary model
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:
        print("Primary model failed:", error)

        # Backup model
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        return response.text
