from flask import Blueprint, request, jsonify
from database import get_db_connection

mining_blueprint = Blueprint("mining", __name__)

@mining_blueprint.route("/start", methods=["POST"])
def start_mining():
    """Start mining for a user."""
    data = request.json
    user_id = data.get("user_id")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Increment user balance
        cursor.execute("UPDATE users SET balance = balance + 10 WHERE id = %s", (user_id,))
        conn.commit()

        return jsonify({"message": "Mining started, balance updated!"})

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    finally:
        if conn:
            cursor.close()
            conn.close()