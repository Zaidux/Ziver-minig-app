from flask import Blueprint, request, jsonify
from database import get_db_connection

referrals_blueprint = Blueprint("referrals", __name__)

@referrals_blueprint.route("/add", methods=["POST"])
def add_referral():
    """Adds a referral for a user."""
    data = request.json
    user_id = data.get("user_id")
    referred_id = data.get("referred_id")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO referrals (user_id, referred_id) VALUES (%s, %s)",
            (user_id, referred_id)
        )
        conn.commit()

        return jsonify({"message": "Referral added successfully!"})

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    finally:
        if conn:
            cursor.close()
            conn.close()