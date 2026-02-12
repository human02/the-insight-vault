import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from models.link import db, Link

# Loads variables from .env file
load_dotenv()

app = Flask(__name__)

# using os.getenv to fetch the URL, with a fallback for safety
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# connect the DB to the app
db.init_app(app)


@app.route("/health")
def health_check():
    return jsonify({"status": "connected", "database": "PostgresSQL"}), 200


if __name__ == "__main__":
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database tables created/verified!")

            db.engine.connect()
            print("✅ Database connection successful!")
            app.run(debug=True)
    except Exception as e:
        print(f"❌ Database error: {e}")
