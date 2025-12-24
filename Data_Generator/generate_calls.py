import random
from datetime import datetime
from supabase import create_client

from Backend.AI.ai_call_generation import generate_call_with_ai
from config import SUPABASE_URL, SUPABASE_KEY, USE_AI
from Data_Generator.sample_transcripts import (
    ISSUE_TYPES,
    TRANSCRIPTS,
    AGENTS,
    SENTIMENT_OPTIONS,
    TONE_OPTIONS,
)


def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# SINGLE CALL GENERATION (AI → Fallback)

def generate_single_call(use_ai: bool = False):
    agent = random.choice(AGENTS)
    issue_type = random.choice(ISSUE_TYPES)

    ai_result = None
    if use_ai and USE_AI:
        ai_result = generate_call_with_ai(issue_type)

    if ai_result:
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
            "created_at": datetime.utcnow().isoformat(),
        }

    # fallback
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
        "created_at": datetime.utcnow().isoformat(),
    }

# INSERT INTO SUPABASE
def insert_call(call, supabase):
    supabase.table("support_calls").insert(call).execute()


# MULTIPLE CALLS

def generate_calls(n: int = 5, use_ai: bool = False):
    supabase = get_supabase()

    for _ in range(n):
        call_event = generate_single_call(use_ai=use_ai)
        insert_call(call_event, supabase)
        print("Inserted:", call_event)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5)
    parser.add_argument("--use_ai", action="store_true")

    args = parser.parse_args()
    generate_calls(args.count, use_ai=args.use_ai)
