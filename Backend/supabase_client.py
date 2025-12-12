
# Backend/supabase_client.py
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

_supabase_instance = None

def get_supabase_client():
    """
    Returns a persistent Supabase client shared across the backend.
    """
    global _supabase_instance
    if _supabase_instance is None:
        _supabase_instance = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_instance

