from flask import Flask, request, jsonify
from database import get_db_connection
from tasks import tasks_blueprint
from mining import mining_blueprint
from referrals import referrals_blueprint

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """Health check endpoint."""
    return jsonify({"message": "Welcome to Ziver Mining App Backend!"})

# Blueprints for modular feature integration
app.register_blueprint(tasks_blueprint, url_prefix="/tasks")
app.register_blueprint(mining_blueprint, url_prefix="/mining")
app.register_blueprint(referrals_blueprint, url_prefix="/referrals")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)