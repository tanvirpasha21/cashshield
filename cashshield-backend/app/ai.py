import requests
from app.config import OPENROUTER_API_KEY

def run_llm(prompt: str) -> str:
    if not OPENROUTER_API_KEY:
        return "⚠️ OpenRouter API key not configured."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://cashshield.app",
        "X-Title": "CashShield"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a calm, supportive financial guide. Explain financial risk without jargon."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 800
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return "⚠️ AI explanation unavailable. Results shown without commentary."
