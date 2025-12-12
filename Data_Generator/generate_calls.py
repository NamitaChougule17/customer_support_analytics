import random
import json
from datetime import datetime

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY
from Data_Generator.sample_transcripts import (
    ISSUE_TYPES,
    TRANSCRIPTS,
    AGENTS,
    SENTIMENT_OPTIONS,
    TONE_OPTIONS
)

# AI client (optional)
if OPENAI_API_KEY:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None


# -------------------------------------------------------------------
# GET SUPABASE CLIENT
# -------------------------------------------------------------------
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# -------------------------------------------------------------------
# AI CALL GENERATION (only used if use_ai = True)
# -------------------------------------------------------------------
def generate_ai_call(issue_type):
    if not client:
        return None  # AI not configured

    prompt = f"""
    Generate a realistic customer support conversation.
    Issue type: {issue_type}

    It must:
    - Be a dialog between Customer and Agent
    - 5 to 8 lines
    - Include emotional cues
    - Include frustration if natural

    Then output JSON ONLY:

    {{
        "transcript": "...",
        "sentiment": "positive | neutral | negative",
        "tone": "calm | frustrated | confused",
        "summary": "...",
        "frustration_score": 0.0 - 1.0
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content
        ai_json = json.loads(content)
        return ai_json

    except Exception as e:
        print("AI Error:", e)
        return None


# -------------------------------------------------------------------
# SINGLE CALL GENERATION (AI → Fallback)
# -------------------------------------------------------------------
def generate_single_call(use_ai=False):
    agent = random.choice(AGENTS)
    issue_type = random.choice(ISSUE_TYPES)

    ai_result = None
    if use_ai:
        ai_result = generate_ai_call(issue_type)

    if ai_result:
        # AI succeeded
        return {
            "agent": agent,
            "issue_type": issue_type,
            "transcript": ai_result["transcript"],
            "sentiment": ai_result["sentiment"],
            "tone": ai_result["tone"],
            "resolution_status": random.choice(["resolved", "unresolved"]),
            "call_duration": random.randint(30, 300),
            "summary": ai_result["summary"],
            "frustration_score": ai_result["frustration_score"],
            "created_at": datetime.utcnow().isoformat()
        }

    else:
        # Fallback only
        return {
            "agent": agent,
            "issue_type": issue_type,
            "transcript": random.choice(TRANSCRIPTS),
            "sentiment": random.choice(SENTIMENT_OPTIONS),
            "tone": random.choice(TONE_OPTIONS),
            "resolution_status": random.choice(["resolved", "unresolved"]),
            "call_duration": random.randint(30, 300),
            "summary": "Basic customer support interaction.",
            "frustration_score": round(random.random(), 2),
            "created_at": datetime.utcnow().isoformat()
        }


# -------------------------------------------------------------------
# INSERT INTO SUPABASE
# -------------------------------------------------------------------
def insert_call(call, supabase):
    supabase.table("support_calls").insert(call).execute()


# -------------------------------------------------------------------
# MULTIPLE CALLS
# -------------------------------------------------------------------
def generate_calls(n=5, use_ai=False):
    supabase = get_supabase()

    for _ in range(n):
        call_event = generate_single_call(use_ai=use_ai)
        insert_call(call_event, supabase)
        print("Inserted:", call_event)


# -------------------------------------------------------------------
# RUN SCRIPT
# -------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--use_ai", action="store_true")

    args = parser.parse_args()

    generate_calls(args.count, use_ai=args.use_ai)
8
14