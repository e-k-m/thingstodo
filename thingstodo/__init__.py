# TODO: Caching ETAGS.
# TODO: Concurrent locking.
# TODO: In detail look at hypothesis.
# TODO: More descriptive 404, via Marshmallow.
# TODO: More strict with input length.
# TODO: Rate Limiting.
# TODO: Rename is completed.

from flask import helpers

from thingstodo import application
from thingstodo import settings
from thingstodo import version

__author__ = "Eric Matti"
__version__ = version.__version__

config = (
    settings.DevConfig if helpers.get_debug_flag() else settings.ProdConfig
)
app = application.create_app(config)
