from flask import Flask
from app.routes import app_routes 

app = Flask(__name__)
app.register_blueprint(app_routes) 

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000)