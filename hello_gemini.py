import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Load environment variables from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "paste-your-key-here":
    print("❌ Error: GEMINI_API_KEY is not set.")
    print("👉 Please open .env and replace 'paste-your-key-here' with your actual Gemini API key from https://aistudio.google.com/apikey")
    sys.exit(1)

try:
    client = genai.Client(api_key=api_key)

    print("Connecting to Gemini API...")
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Explain healthy eating to a 10-year-old in three lines.",
    )

    print("\n✅ Response from Gemini:")
    print(response.text)

except errors.APIError as e:
    print(f"\n❌ Gemini API Error ({e.code}): {e.message}")
except Exception as e:
    print(f"\n❌ Unexpected Error: {e}")
