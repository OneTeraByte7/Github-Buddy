# llm_client.py

import requests
import json

class LLMClient:
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        self.api_key = api_key
        self.model = model
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        headers = {
            "Content-Type": "application/json"
        }

        body = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }

        url = f"{self.base_url}?key={self.api_key}"
        response = requests.post(url, headers=headers, json=body)

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            print("API Error:", response.status_code)
            print("Response JSON:", response.json())
            raise

        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]

