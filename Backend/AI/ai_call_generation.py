# Backend/ai/ai_call_generation.py

from typing import Optional, Dict, Any
from config import OPENAI_API_KEY, USE_AI

if USE_AI and OPENAI_API_KEY:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None


def generate_call_with_ai(issue_type: str) -> Optional[Dict[str, Any]]:
    """
    Generates AI-based call data.
    Returns:
    - transcript
    - sentiment
    - tone
    - summary
    - frustration_score
    """

    if not client:
        return None

    prompt = f"""
    Generate a realistic customer support conversation.

    Issue Type: {issue_type}

    Rules:
    - 5–8 dialogue lines
    - Customer and Agent format
    - Emotionally realistic
    - Return ONLY valid JSON

    JSON:
    {{
      "transcript": "...",
      "sentiment": "positive | neutral | negative",
      "tone": "calm | frustrated | confused",
      "summary": "...",
      "frustration_score": 0.0
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        result = eval(response.choices[0].message.content)

        required = {
            "transcript",
            "sentiment",
            "tone",
            "summary",
            "frustration_score",
        }

        if not required.issubset(result.keys()):
            return None

        return result

    except Exception as e:
        print("AI call generation error:", e)
        return None
