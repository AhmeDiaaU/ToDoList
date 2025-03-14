from datetime import datetime, timezone
from app import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    archived = db.Column(db.Boolean)
    Days_of_week = db.Column(db.String(100))
    Created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Task {self.id}>"