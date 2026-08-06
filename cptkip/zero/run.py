import time

import cptkip.core.environment as environment

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable


def run_for(seconds: float | int, func: Callable[[], None]):
    """
    Runs the func for the given number of seconds.
    """
    if seconds <= 0:
        raise ValueError(f"Argument {seconds} is not positive")
    
    finish = time.monotonic() + seconds

    while time.monotonic() < finish:
        func()


def update_for(seconds: float | int, *args):
    """
    Runs update/animate on the arguments for the given number of seconds.
    """

    def func():
        for arg in args:
            if hasattr(arg, "update"):
                arg.update()
            elif hasattr(arg, "animate"):
                arg.animate()
            else:
                raise ValueError(f"Argument {arg} is not callable")

    run_for(seconds, func)
