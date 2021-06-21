import datetime
import uuid

from thingstodo import database

db = database.db


class Todo(db.Model):
    __tablename__ = "todo"

    id = db.Column(db.String, primary_key=True)
    text = db.Column(db.Text)
    user = db.Column(db.Text)
    completed = db.Column(db.Boolean)
    date = db.Column(db.Text)

    def __init__(self, text, user):
        self.id = str(uuid.uuid4())
        self.text = text
        self.user = user
        self.completed = False
        self.date = str(datetime.datetime.now())

    def __repr__(self):
        return (
            f"Todo(id={self.id}, text={self.text}, "
            f"user={self.user}, completed={self.completed}, date={self.date})"
        )
