"""
PostgreSQL/Supabase connection for storing critical alerts.
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Optional[Client] = None

def get_supabase_client() -> Optional[Client]:
    """
    Get or create Supabase client instance.
    Returns None if credentials are not configured (graceful degradation).
    """
    global supabase
    if supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("Warning: SUPABASE_URL and SUPABASE_KEY not set. Alerts will not be saved to Supabase.")
            return None
        try:
            supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            print(f"Error creating Supabase client: {e}")
            return None
    return supabase


def create_alerts_table_if_not_exists():
    """
    Create the alerts table if it doesn't exist.
    This should be run once, or you can create it manually in Supabase dashboard.
    
    SQL to run in Supabase SQL Editor:
    
    CREATE TABLE IF NOT EXISTS alerts (
        id BIGSERIAL PRIMARY KEY,
        owner VARCHAR(255) NOT NULL,
        alert_type VARCHAR(100) NOT NULL,
        severity VARCHAR(50) NOT NULL,
        description TEXT NOT NULL,
        source_ip VARCHAR(45),
        metadata JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_alerts_owner ON alerts(owner);
    CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at DESC);
    """
    # For now, we'll assume the table is created manually in Supabase
    # This function is here for documentation purposes
    pass

