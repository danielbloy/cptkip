# To reduce memory footprint of logging to as small as possible on CircuitPython
# devices, this is about as trivial as logging can get.
CRITICAL: int = 0
ERROR: int = 1
WARNING: int = 2
INFO: int = 3
DEBUG: int = 4
LEVEL = WARNING

C = "CRITICAL"
E = "ERROR   "
W = "WARN    "
# noinspection PyPep8
I = "INFO    "
D = "DEBUG   "


def set_log_level(level) -> None:
    """
    Sets the logging level to use in the same way as Logging. Defaults to WARNING.

    :param level: A number, usually one of CRITICAL, ERROR, WARNING, INFO, DEBUG.
    """
    global LEVEL
    LEVEL = level


def stacktrace(e: Exception) -> None:
    """
    Puts a stacktrace out for the exception using the DEBUG log level.

    :param e: The exception whose stack trace we want to log.
    """
    import traceback
    for s in traceback.format_exception(e):
        debug(s)


def log(level, *args):
    """Writes message at the specified log level."""
    if level <= LEVEL:

        prefix = D
        if level == CRITICAL:
            prefix = C
        elif level == ERROR:
            prefix = E
        elif level == WARNING:
            prefix = W
        elif level == INFO:
            prefix = I
        elif level == DEBUG:
            prefix = D

        print(prefix, ":", *args)


def debug(*args) -> None:
    """Writes message at the DEBUG log level."""
    log(DEBUG, *args)


def info(*args) -> None:
    """Writes message at the INFO log level."""
    log(INFO, *args)


def warn(*args) -> None:
    """Writes message at the WARNING log level."""
    log(WARNING, *args)


def error(*args) -> None:
    """Writes message at the ERROR log level."""
    log(ERROR, *args)


def critical(*args) -> None:
    """Writes message at the CRITICAL log level."""
    log(CRITICAL, *args)
