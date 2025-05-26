import cptkip.core.environment as environment

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable


def run(funcs: list[Callable[[], bool]]) -> None:
    """
    Simply runs a list of functions and waits for them to finish (by
    returning False). No error handling is performed.
    """

    while len(funcs):
        funcs = [func for func in funcs if func()]
