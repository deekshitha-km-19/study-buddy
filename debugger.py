
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "Gemini API key missing. Please check your .env file."
    )

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash"


def debug_code(code):
    """
    Analyze Python code, identify errors,
    explain them, and provide corrected code.
    """

    if not code or not code.strip():
        return "Please enter Python code to debug."

    prompt = f"""
You are an expert Python debugging assistant.

Analyze the following Python code.

Provide your answer in this format:

1. ERROR DETECTION
   Identify syntax errors, runtime errors, and logical errors.

2. WHY THE ERROR OCCURS
   Explain each error in simple beginner-friendly language.

3. CORRECTED PYTHON CODE
   Provide the complete corrected code inside a Python code block.

4. EXPLANATION
   Explain what you changed and why.

5. SAMPLE OUTPUT
   Show the expected output if the code is executed.

If the code has no errors, clearly mention that.

PYTHON CODE:
{code}
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            if response and response.text:
                return response.text

            return "Gemini returned an empty response. Please try again."

        except ServerError as error:
            print("Gemini server error:", error)

            if attempt < 2:
                wait_time = 5 * (attempt + 1)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                return "Gemini server is unavailable. Please try again later."

        except Exception as error:
            return f"Debugging failed: {str(error)}"


if __name__ == "__main__":

    sample_code = """
number = 10

if number > 5
    print("Number is greater")
"""

    result = debug_code(sample_code)

    print("\n===== SMART CODING AGENT =====")
    print("===== AI DEBUGGING RESULT =====\n")
    print(result)
