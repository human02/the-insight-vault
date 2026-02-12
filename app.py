import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Loads variables from .env file
load_dotenv()

app = Flask(__name__)

# using os.getenv to fetch the URL, with a fallback for safety
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialise the DB
db = SQLAlchemy(app)


@app.route("/health")
def health_check():
    return jsonify({"status": "connected", "database": "PostgresSQL"}), 200


if __name__ == "__main__":
    try:
        with app.app_context():
            db.engine.connect()
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
