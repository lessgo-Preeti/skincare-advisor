import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection settings
DB_CONFIG = {
    "host": "localhost",
    "database": "skincare_advisor",
    "user": "postgres",
    "password": "Postgresql@2026",
    "port": "5432"
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
        print(f"Save failed: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_analysis_history():
    """Get all past analysis from database."""
    conn = get_connection()
    if not conn:
        return []

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
