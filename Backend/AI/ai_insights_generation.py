from typing import Optional, Dict, Any
from config import OPENAI_API_KEY, USE_AI

if USE_AI and OPENAI_API_KEY:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None


def generate_insights_with_ai(call: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Generates AI-based insights.
    Returns:
    - risk_level
    - summary
    - recommended_action
    """

    if not client:
        return None

    prompt = f"""
    Analyze this customer support interaction.

    Transcript:
    {call.get("transcript")}

    Sentiment: {call.get("sentiment")}
    Tone: {call.get("tone")}
    Frustration Score: {call.get("frustration_score")}
    Resolution Status: {call.get("resolution_status")}

    Return ONLY JSON:

    {{
      "risk_level": "low | medium | high",
      "summary": "...",
      "recommended_action": "..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )

        result = eval(response.choices[0].message.content)

        required = {
            "risk_level",
            "summary",
            "recommended_action",
        }

        if not required.issubset(result.keys()):
            return None

        return result

    except Exception as e:
        print("AI insights error:", e)
        return None
