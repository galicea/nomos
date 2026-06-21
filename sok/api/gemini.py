# backend0/api/gemini.py
import os
import logging
import requests

logger = logging.getLogger(__name__)

def gemini_q(query: str, prompt: dict) -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    system_instruction = prompt.get("system", "")
    user_content = prompt.get("user", "")

    if not api_key:
        logger.warning("GEMINI_API_KEY not found in environment. Returning mock response.")
        # Create a mock response for testing when API key is not present
        mock_response = (
            f"[MOCK RESPONSE - GEMINI_API_KEY not configured]\n"
            f"Otrzymano pytanie: {query}\n"
            f"System Prompt:\n{system_instruction[:200]}...\n"
            f"User Prompt:\n{user_content[:200]}...\n\n"
            f"Aby uzyskać rzeczywistą odpowiedź LLM, ustaw zmienną środowiskową GEMINI_API_KEY."
        )
        return {"response": mock_response}

    # If api_key is present, call the Gemini API via requests
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_content}]
            }
        ],
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 800
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"response": text}
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return {"response": f"Błąd komunikacji z API Gemini: {str(e)}"}
