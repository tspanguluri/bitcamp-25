from fastapi import APIRouter, status
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import re

router = APIRouter()
dotenv_path = Path(__file__).resolve().parents[2] / ".env"
loaded = load_dotenv(dotenv_path=dotenv_path)
api_keyv = os.getenv("OPENAI_API_KEY")

@router.get(
    "/chatgpt",
    status_code=200,
    # response_model=#Create Response Model
)

def generate_chatgpt_stuff():
   client = OpenAI(api_key=api_keyv)
   mood = "happy"
   response = client.responses.create(
      model = "gpt-4o",
      input = "Give me the name and artist of 15 songs which align with the mood given: " + mood + "Return it in the following JSON schema: [{track: ___, artist: ___}, {track: ____, artist___}, …]. Response should be nothing but the JSON!!"
    )
   raw_output = response.output_text
   cleaned = re.sub(r"```json|```", "", raw_output).strip()
   try:
        parsed_json = json.loads(cleaned)
   except json.JSONDecodeError as e:
        return {"error": "Failed to parse JSON", "details": str(e), "raw": raw_output}
   return parsed_json

   
   





