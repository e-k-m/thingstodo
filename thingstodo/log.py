import json
import logging
import logging.config
import datetime

from werkzeug import local
import flask

logger = local.LocalProxy(lambda: flask.current_app.logger)


class StructuredMessage(object):
    def __init__(self, event, **kwargs):
        self.event = event
        self.kwargs = kwargs

    def to_dict(self):
        res = self.kwargs.copy()
        res["event"] = self.event
        return res

    def __str__(self):
        if self.kwargs:
            return "{}={}".format(self.event, json.dumps(self.kwargs))
        return self.event


m = StructuredMessage


class JSONFormatter(logging.Formatter):
    def __init__(self, name=None):
        self.name = name

    def format(self, record):
        res = {
            "application": self.name,
            "level": record.levelname,
            "logger": record.name,
            "timestamp": datetime.datetime.utcnow()
            .replace(tzinfo=datetime.timezone.utc)
            .isoformat(),
        }

        if isinstance(record.msg, StructuredMessage):
            res.update(record.msg.to_dict())
        else:
            res["event"] = record.getMessage()

        if hasattr(record, "exc_info") and record.exc_info:
            res["exception"] = repr(super().formatException(record.exc_info))

        if isinstance(record.msg, StructuredMessage):
            k = "{}.{}.{}".format(
                res["application"], res["logger"], res["event"]
            )
        else:
            k = "{}.{}".format(res["application"], res["logger"])
        return json.dumps({k: res})


def init_app(app):
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "production": {"()": JSONFormatter, "name": app.name},
                "development": {
                    "format": (
                        "[%(asctime)s] %(levelname)s in "
                        "%(module)s: %(message)s"
                    ),
                },
            },
            "handlers": {
                "main": {
                    "class": "logging.StreamHandler",
                    "formatter": app.config["ENV"],
                }
            },
            "root": {"level": app.config["LOG_LEVEL"], "handlers": ["main"]},
        }
    )
