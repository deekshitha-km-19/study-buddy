
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


def check_gemini_models():

    if not api_key:
        print("ERROR: Gemini API key not found in .env")
        return

    try:
        client = genai.Client(api_key=api_key)

        print("\n===== GEMINI MODEL CHECKER =====\n")
        print("Checking available Gemini models...\n")

        found = False

        for model in client.models.list():
            actions = model.supported_actions or []

            if "generateContent" in actions:
                print("Available model:", model.name)
                found = True

        if not found:
            print("No models supporting generateContent were found.")

        print("\n===== CHECK COMPLETED =====")

    except Exception as error:
        print("\nUnable to retrieve Gemini models.")
        print("Error:", error)


if __name__ == "__main__":
    check_gemini_models()
