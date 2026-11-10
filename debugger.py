
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key missing in .env")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-3.5-flash"

def debug_code(code):
    prompt = f"""
You are an expert Python debugging assistant.

1. Identify errors in the code.
2. Explain why they occur.
3. Provide corrected Python code.

CODE:
{code}
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text

        except ServerError as error:
            print("Gemini server error:", error)

            if attempt < 2:
                print("Retrying in 10 seconds...")
                time.sleep(10)
            else:
                return "Gemini server is unavailable. Check the error above."


if __name__ == "__main__":

    code = """
number = 10
if number > 5
    print("Number is greater")
"""

    result = debug_code(code)

    print("\n===== AI DEBUGGING RESULT =====\n")
    print(result)
