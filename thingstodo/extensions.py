import os

from wtoolzexceptions import exceptions
import flask
import flask_cors
import flask_jwt_extended
import flask_migrate
import flask_sqlalchemy


class CRUDMixin(flask_sqlalchemy.Model):
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        return True


directory_migrations = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "migrations"
)

db = flask_sqlalchemy.SQLAlchemy(model_class=CRUDMixin)

migrate = flask_migrate.Migrate(db=db, directory=directory_migrations)
cors = flask_cors.CORS()
jwt = flask_jwt_extended.JWTManager()


def response(e):
    resp = flask.jsonify(e.to_dict())
    resp.status_code = e.http_status_code
    return resp


@jwt.expired_token_loader
def expired_token_loader(_):
    return response(exceptions.Unauthorized("The token has expired."))


@jwt.invalid_token_loader
def invalid_token_loader(_):
    return response(exceptions.UnprocessableEntity("The token is invalid."))


@jwt.unauthorized_loader
def unauthorized_loader(_):
    return response(exceptions.Unauthorized())


@jwt.needs_fresh_token_loader
def needs_fresh_token_loader():
    return response(exceptions.Unauthorized())
