from cptkip.core.environment import is_running_on_desktop

if is_running_on_desktop():
    from typing import Callable


def run(*funcs: Callable[[], bool],
        continue_func: Callable[[], bool] | None = None) -> None:
    """
    Simply runs a list of functions and waits for them to finish (by
    returning False). No error handling is performed. The runner will
    execute for as long as continue_func returns True.

    :param continue_func: A function that returns whether to cancel the task or not.
    """

    # Filter in place on a private copy instead of rebuilding a new list every
    # pass: the old list comprehension allocated a fresh list on every single
    # iteration of this loop (which can run for the program's whole lifetime),
    # even when nothing finished. del only shifts the underlying array and only
    # runs when a function actually completes.
    active = list(funcs)
    while active:
        if continue_func and not continue_func():
            return

        i = 0
        while i < len(active):
            if active[i]():
                i += 1
            else:
                del active[i]
