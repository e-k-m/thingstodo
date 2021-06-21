import os

import flask


def main():
    os.environ["FLASK_APP"] = "thingstodo"
    flask.cli.main()


if __name__ == "__main__":
    main()
