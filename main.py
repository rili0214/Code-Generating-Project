from flask import Flask
from app.routes import initialize_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

initialize_routes(app)

if __name__ == "__main__":
    app.run(debug=True)