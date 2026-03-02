import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection settings from .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "skincare_advisor"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
    "port": os.getenv("DB_PORT", "5432")
}

def get_connection():
    """Create and return database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def save_analysis(skin_type, safety_score, confidence, verdict, total_ingredients, total_matched):
    """Save analysis result to database."""
    conn = get_connection()
    if not conn:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO analysis_history 
            (skin_type, safety_score, confidence, verdict, total_ingredients, total_matched)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (skin_type, safety_score, confidence, verdict, total_ingredients, total_matched))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Save failed: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        conn.close()

def get_analysis_history():
    """Get all past analysis from database."""
    conn = get_connection()
    if not conn:
        return []

    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM analysis_history 
            ORDER BY created_at DESC 
            LIMIT 50
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"Fetch failed: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        conn.close()

def test_connection():
    """Test database connection."""
    conn = get_connection()
    if conn:
        print("Database connected successfully!")
        conn.close()
        return True
    else:
        print("Database connection failed!")
        return False
