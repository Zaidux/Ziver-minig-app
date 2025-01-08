# Ziver-minig-backend

app.py

"""
Ziver Mining App Backend

This Flask application provides endpoints for user registration and login.
It uses PostgreSQL as the database and bcrypt for password hashing.

Endpoints:
- GET `/` : Health check.
- POST `/register` : Registers a new user.
- POST `/login` : Authenticates an existing user.
"""

from flask import Flask, request, jsonify
import psycopg2
import bcrypt

# Initialize Flask app
app = Flask(__name__)

# Database connection configuration
DB_HOST = "127.0.0.1"
DB_NAME = "ziver_db"
DB_USER = "termux_user"
DB_PASSWORD = ""  # Add your password if set


def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database.

    Returns:
        psycopg2.extensions.connection: Database connection object.
    """
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/", methods=["GET"])
def home():
    """
    Health check endpoint.

    Returns:
        JSON: A welcome message.
    """
    return jsonify({"message": "Welcome to Ziver Mining App Backend!"})


@app.route("/register", methods=["POST"])
def register():
    """
    Registration endpoint for new users.

    Expects:
        JSON payload with 'email', 'username', and 'password'.

    Returns:
        JSON: Success or error message.
    """
    data = request.json
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")  # Accept password input

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

    except Exception as e:  # General exception catch for unexpected issues
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    finally:
        if conn:
            cursor.close()
            conn.close()


@app.route("/login", methods=["POST"])
def login():
    """
    Login endpoint for existing users.

    Expects:
        JSON payload with 'email' and 'password'.

    Returns:
        JSON: Success message with user details or an error message.
    """
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

        # If successful
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

    except psycopg2.Error as db_error:  # Specific database error handling
        return jsonify({"error": f"Database error: {db_error}"}), 500

    except Exception as e:  # General exception for unexpected issues
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)        