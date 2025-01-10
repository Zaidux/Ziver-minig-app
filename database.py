import psycopg2
import os

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("DB_NAME", "ziver_db")
DB_USER = os.getenv("DB_USER", "termux_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )