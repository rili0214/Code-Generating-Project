from flask import Flask
from app.routes import app_routes  # Import the blueprint

app = Flask(__name__)
app.register_blueprint(app_routes)  # Register the blueprint with the Flask app

# Entry point for running the Flask application
if __name__ == "__main__":
    # Ensure Flask runs on host 0.0.0.0 to accept external traffic if needed
    app.run(host="0.0.0.0", port=8000)
