import cptkip.core.environment as environment

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable


def run(funcs: list[Callable[[], bool]]) -> None:
    """
    Simply runs a list of functions and waits for them to finish (by
    returning False). No error handling is performed.
    """

    # Filter in place on a private copy instead of rebuilding a new list every
    # pass: the old list comprehension allocated a fresh list on every single
    # iteration of this loop (which can run for the program's whole lifetime),
    # even when nothing finished. del only shifts the underlying array and only
    # runs when a function actually completes.
    active = list(funcs)
    while active:
        i = 0
        while i < len(active):
            if active[i]():
                i += 1
            else:
                del active[i]
