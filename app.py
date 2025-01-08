"""Ziver Mining App Backend

This Flask application provides endpoints for user registration and login.
It uses PostgreSQL as the database and bcrypt for password hashing.

Endpoints:
- GET / : Health check.
- POST /register : Registers a new user.
- POST /login : Authenticates an existing user.
"""

from flask import Flask, request, jsonify
import psycopg2
import bcrypt
import os

# Initialize Flask app
app = Flask(__name__)

# Database connection configuration (use environment variables for security)
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_NAME = os.getenv("DB_NAME", "ziver_db")
DB_USER = os.getenv("DB_USER", "termux_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Function to establish a database connection
def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/", methods=["GET"])
def home():
    """Health check endpoint."""
    return jsonify({"message": "Welcome to Ziver Mining App Backend!"})

@app.route("/register", methods=["POST"])
def register():
    """Registration endpoint for new users."""
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    # Validate input
    if not email or not username or not password:
        return jsonify({"error": "Email, Username, and Password are required!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username or email already exists
        cursor.execute(
            "SELECT * FROM users WHERE email = %s OR username = %s", (email, username)
        )
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({"error": "Email or Username already exists!"}), 400

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Insert new user into the database
        cursor.execute(
            """
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
            """,
            (username, email, hashed_password.decode("utf-8"))
        )
        conn.commit()

        return jsonify({"message": f"User {username} registered successfully!"})

    except psycopg2.Error as db_error:
        return jsonify({"error": f"Database error: {db_error}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    finally:
        if conn:
            cursor.close()
            conn.close()

@app.route("/login", methods=["POST"])
def login():
    """Login endpoint for existing users."""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Validate input
    if not email or not password:
        return jsonify({"error": "Email and Password are required!"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute(
            "SELECT id, username, email, password, balance, streak FROM users WHERE email = %s", 
            (email,)
        )
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Invalid email or user does not exist!"}), 404

        # Extract user details
        user_id, username, email, hashed_password, balance, streak = user

        # Verify the password
        if not bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            return jsonify({"error": "Incorrect password!"}), 401

        return jsonify({
            "message": "Login successful!",
            "user": {
                "id": user_id,
                "username": username,
                "email": email,
                "balance": balance,
                "streak": streak
            }
        })

    except psycopg2.Error as db_error:
        return jsonify({"error": f"Database error: {db_error}"}), 500

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    finally:
        if conn:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)