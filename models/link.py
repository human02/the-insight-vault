from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# We'll initialize this in app.py and import it here
db = SQLAlchemy()


class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
        }
