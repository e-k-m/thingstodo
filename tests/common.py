import os
import unittest

import flask_jwt_extended as jwt

os.environ["THINGS_TODO_DATABASE"] = ""
os.environ["THINGS_TODO_SECRET"] = "robocop"

from thingstodo import application  # noqa
from thingstodo import database  # noqa
from thingstodo import settings  # noqa
from thingstodo.todos import models  # noqa

USER = "972e4b03-abf0-45df-8917-222b5b462f49"
OTHER_USER = "some-uuid-kind-of-thing"


app = application.create_app(settings.TestConfig)
app_context = app.test_request_context()
app_context.push()
with app.app_context():
    TOKEN = jwt.create_access_token(
        USER,
        expires_delta=False,
        user_claims={
            "id": USER,
            "email": "robocop@robocop.com",
            "username": "alexmurphy",
            "roles": ["user"],
            "permissions": ["todocrud"],
        },
    )

    OTHER_TOKEN = jwt.create_access_token(
        OTHER_USER,
        expires_delta=False,
        user_claims={
            "id": OTHER_USER,
            "email": "robocop@robocop.com",
            "username": "alexmurphy",
            "roles": ["user"],
            "permissions": ["todocrud"],
        },
    )


class TestFixure(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app_context = app_context
        self.client = self.app.test_client()
        with self.app.app_context():
            database.db.create_all()
        notes = []
        for i in range(10):
            note = models.Todo(text=f"{i} hacker", user=USER)
            note.save()
            notes.append(note)

        for i in range(2):
            note = models.Todo(text=f"{i} take it down", user=OTHER_USER)
            note.save()

        self.should = notes[0]

    def tearDown(self):
        database.db.drop_all()
