from flask import Blueprint, request, jsonify
from database import get_db_connection

tasks_blueprint = Blueprint("tasks", __name__)

@tasks_blueprint.route("/", methods=["GET"])
def get_tasks():
    """Fetches all tasks for a user."""
    user_id = request.args.get("user_id")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
        tasks = cursor.fetchall()

        return jsonify({"tasks": tasks})

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    finally:
        if conn:
            cursor.close()
            conn.close()

@tasks_blueprint.route("/add", methods=["POST"])
def add_task():
    """Adds a new task for a user."""
    data = request.json
    user_id = data.get("user_id")
    description = data.get("description")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tasks (user_id, description) VALUES (%s, %s)",
            (user_id, description)
        )
        conn.commit()

        return jsonify({"message": "Task added successfully!"})

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    finally:
        if conn:
            cursor.close()
            conn.close()