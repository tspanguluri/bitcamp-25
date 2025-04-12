import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parents[2] / ".env"
print(f"🔍 Loading .env from: {dotenv_path}")
loaded = load_dotenv(dotenv_path=dotenv_path)
print("✅ .env loaded:", loaded)

api_keyv = os.getenv("OPENAI_API_KEY")
print("🔑 Found key:", api_keyv[:10] if api_keyv else "None")

if not api_keyv:
    raise ValueError("OPENAI_API_KEY not found in .env file.")
client = OpenAI(api_key=api_keyv)

response = client.responses.create(
    model="gpt-4o",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)