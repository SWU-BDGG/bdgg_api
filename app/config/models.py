from collections import namedtuple


Database = namedtuple(
    "Database",
    "host port user password database"
)

Metadata = namedtuple(
    "Metadata",
    "title"
)


##############################################
del namedtuple
__all__ = [model for model in dir() if not model.startswith("__")]
