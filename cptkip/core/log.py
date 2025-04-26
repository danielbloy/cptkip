# To reduce memory footprint of logging to as small as possible on CircuitPython
# devices, this is about as trivial as logging can get. If you want a more
# comprehensive logging mechanism for both desktop and CircuitPython then use
# the `cptkip.logging` package.
import cptkip.core.environment as environment

CRITICAL: int = 0
ERROR: int = 1
WARNING: int = 2
INFO: int = 3
DEBUG: int = 4
LEVEL = WARNING

C = "CRITICAL"
E = "ERROR"
W = "WARN "
I = "INFO "
D = "DEBUG"
N = "NONE "


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
    if environment.is_running_on_desktop():
        # This is to support Python 3.9 as well as Python 3.12.
        for s in traceback.format_exception(e, value=None, tb=None):
            debug(s)
    else:
        for s in traceback.format_exception(e):
            debug(s)


def log(level, message: str):
    """Writes message at the specified log level."""
    if level <= LEVEL:

        l = N
        if level == CRITICAL:
            l = C
        elif level == ERROR:
            l = E
        elif level == WARNING:
            l = W
        elif level == INFO:
            l = I
        elif level == DEBUG:
            l = D

        print(l, ": ", message)


def debug(message: str) -> None:
    """Writes message at the DEBUG log level."""
    log(DEBUG, message)


def info(message: str) -> None:
    """Writes message at the INFO log level."""
    log(INFO, message)


def warn(message: str) -> None:
    """Writes message at the WARNING log level."""
    log(WARNING, message)


def error(message: str) -> None:
    """Writes message at the ERROR log level."""
    log(ERROR, message)


def critical(message: str) -> None:
    """Writes message at the CRITICAL log level."""
    log(CRITICAL, message)
