# TODO: Validate
# TODO: Validate-performance
# TODO: Changelog

from cptkip.core.environment import is_running_on_desktop
from cptkip.core.logging import warn, stacktrace

if is_running_on_desktop():
    from typing import Callable


def run(*funcs: Callable[[], bool],
        terminate_on_exception: bool = True,
        restart_on_exception: bool = False) -> None:  # TODO: Add keep going function.
    """
    Runs a list of functions and waits for them to finish, providing a configurable
    amount of error handling based on the passed in properties.

    By default, if any of the functions raises an exception, the runner will terminate. This
    is controlled with terminate_on_exception. If terminate_on_exception is False, the runner
    will continue to run the remaining functions.

    By default, where a task errors with an exception, the runner will consider the function
    to have completed and remove it from the list of functions to execute. If
    restart_on_exception is True, the runner will keep the function in the list of functions
    to execute.
    """
    # Filter in place on a private copy instead of rebuilding a new list every
    # pass: the old list comprehension allocated a fresh list on every single
    # iteration of this loop (which can run for the program's whole lifetime),
    # even when nothing finished. del only shifts the underlying array and only
    # runs when a function actually completes.
    active = list(funcs)
    while active:
        i = 0
        success = False
        while i < len(active):

            try:
                success = active[i]()
            except Exception as e:
                warn('Exception: raised by task', i)
                stacktrace(e)

                if restart_on_exception:
                    warn('Rerunning task', i)
                    success = True

                elif terminate_on_exception:
                    return

            if success:
                i += 1
            else:
                del active[i]
