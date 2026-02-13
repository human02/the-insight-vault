import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from models.link import db, Link
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

# Loads variables from .env file
load_dotenv()

app = Flask(__name__)

# using os.getenv to fetch the URL, with a fallback for safety
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# connect the DB to the app
db.init_app(app)


# --- Global Error Handlers ---


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Handles standard Flask errors (like 404, 405)."""
    return jsonify({"error": e.name, "message": e.description}), e.code


@app.errorhandler(SQLAlchemyError)
def handle_db_error(e):
    """Handles Database specific errors."""
    db.session.rollback()
    print(f"Database Error: {e}")  # Log for you
    return jsonify(
        {"error": "Database Error", "message": "A database operation failed."}
    ), 500


@app.errorhandler(Exception)
def handle_generic_exception(e):
    """Catch-all for everything else (the 500s)."""
    print(f"Unhandled Exception: {e}")
    return jsonify(
        {"error": "Internal Server Error", "message": "An unexpected error occurred."}
    ), 500


# --- Routes ---


@app.route("/")
def homepage():
    return jsonify({"message": "Welcome to the Insight Vault", "version": "0.0.1"}), 200


@app.route("/health")
def health_check():
    return jsonify({"status": "connected", "database": "PostgresSQL"}), 200


@app.route("/links", methods=["POST"])
def create_link():
    data = request.get_json()

    # safety check - validation
    if not data or "url" not in data:
        return jsonify({"error": "Bad Request", "message": "URL is required"}), 400

    new_link = Link(
        url=data["url"],
        title=data.get("title"),
        description=data.get("description"),
    )

    db.session.add(new_link)
    db.session.commit()

    return jsonify(new_link.to_dict()), 201


@app.route("/links", methods=["GET"])
def get_all_links():
    data = Link.query.order_by(Link.created_at.desc()).all()
    return jsonify([link.to_dict() for link in data]), 200


if __name__ == "__main__":  # pragma: no cover
    try:
        with app.app_context():
            db.create_all()
            print("✅ Database tables created/verified!")

            db.engine.connect()
            print("✅ Database connection successful!")
            app.run(debug=True)
    except Exception as e:
        print(f"❌ Database error: {e}")
