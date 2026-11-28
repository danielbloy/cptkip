from cptkip.core.environment import is_running_on_desktop
from cptkip.core.logging import warn, stacktrace

if is_running_on_desktop():
    from typing import Callable


def run(*funcs: Callable[[], bool],
        restart_on_exception: bool = True,
        continue_func: Callable[[], bool] | None = None) -> None:
    """
    Runs a list of functions and waits for them to finish, providing a configurable
    amount of error handling based on the passed in properties. The runner will
    execute for as long as continue_func returns True and there are functions running.

    NOTE: When continue_func returns False the runner returns immediately; the tasks
    are not called again. A task created with an end callback (periodic_task,
    triggered_task, triggered_events_task) only runs end when it sees its *own*
    continue_func return False. To guarantee end callbacks run, give the stop
    condition to the tasks rather than (or as well as) to the runner, e.g.
    runner.run(task) where task was created with continue_func=stop_condition.

    By default, where a task errors with an exception, the runner will consider the
    function to have not completed and keep it in the list of functions to execute.
    If restart_on_exception is False, the runner will remove the function from the
    list of functions to execute.

    :param restart_on_exception: If True, the runner will restart the task if it
      raises an exception.
    :param continue_func: A function that returns whether to continue executing or not.
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

            try:
                success = active[i]()
            except Exception as e:
                warn('Exception raised by task', i, "-", e)
                stacktrace(e)

                success = restart_on_exception
                if restart_on_exception:
                    warn('Rerunning task', i)

            if success:
                i += 1
            else:
                del active[i]
