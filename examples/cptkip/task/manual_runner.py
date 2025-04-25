import asyncio

import cptkip.core.environment as environment
import cptkip.core.log as log
import cptkip.core.memory as memory
from cptkip.task.scheduler import new_scheduled_task

__running = False
cancel = False
cancel_on_exception = False
restart_on_exception = True
restart_on_completion = True
callback_frequency = 10


def __new_task_handler(task: Callable[[], Awaitable[None]]) -> Callable[[], Awaitable[None]]:
    """
    This wraps any task and provides the exception and completion handling
    such as restart as defined by the Runners properties.

    :param task: The task that is to be wrapped.
    """

    async def handler():
        global cancel

        while not cancel:
            try:
                # This sleep both delays the start of the handler but also throttles the
                # task if it gets into a greedy loop where it does not await itself. This
                # can happen if the task keeps ending with restarts on or if it keeps
                # raising exceptions.
                await asyncio.sleep(0.001)
                if not cancel:
                    await task()
                    log.info(f'Task completed {task}')

                if restart_on_completion:
                    log.info(f'Rerunning task {task}')
                else:
                    return

            except asyncio.CancelledError:
                log.error(f'Caught CancelledError exception for task {task}')
                return

            except Exception as e:
                log.warn(f'Exception: {e} raised by task {task}')
                log.stacktrace(e)

                if restart_on_exception:
                    log.warn(f'Rerunning task {task}')

                elif cancel_on_exception:
                    cancel = True

                else:
                    return

    return handler


def cancel_func() -> bool:
    return cancel


def __new_scheduled_task_handler(task: Callable[[], Awaitable[None]]) -> Callable[[], Awaitable[None]]:
    """
    Performs the scheduling invocation of the provided callback based on self.callback_frequency.
    If the callback raises an exception then the Runner will be set to cancel; irrespective of
    the rest of the task configuration. This is intended to be used to schedule tasks internal
    to the task only (such as scheduling invocation of the callback).

    Note: This function will complete once it detects that self.cancel is set so cannot be used
          for cleanup during cancellation.

    :param task: Called once every cycle based on the callback frequency.
    """

    async def handler() -> None:
        global cancel
        try:
            if not cancel:
                await task()

        except asyncio.CancelledError:
            log.error(f'Caught CancelledError exception for scheduled task {task}, cancelling task')
            cancel = True

        except Exception as e:
            log.error(f'Exception: {e} raised by scheduled task {task}, cancelling task')
            log.stacktrace(e)
            cancel = True

    return new_scheduled_task(handler, cancel_func, 10)


def __cancel_tasks(tasks: list[asyncio.Task]) -> None:
    """
    Cancels all the specified tasks.

    :param tasks: The tasks to cancel.
    """
    global cancel
    cancel = True
    log.info(f'Cancelling {len(tasks)} tasks:')
    for task in tasks:
        log.info(f'  {task}')
        task.cancel()


def __cancellation_handler(tasks: list[asyncio.Task]) -> Callable[[], Awaitable[None]]:
    """
    This handler runs in the background and monitors which tasks from the passed in
    list have completed. Once all have completed, the Runner will be cancelled.

    :param tasks: The list of background tasks to monitor.
    """

    async def wait_for_finished_tasks() -> None:
        global cancel

        completed: int = 0
        pending: int = 0
        for task in tasks:
            if task.done():
                completed += 1
                tasks.remove(task)
            else:
                pending += 1

        log.debug(f'Background tasks: Done: {completed}, Pending: {pending}')

        # If all the tasks have completed then cancel the task.
        if pending <= 0:
            cancel = True

    async def cancel_handler() -> None:
        # Monitor in the background for all tasks to complete.
        await __new_scheduled_task_handler(wait_for_finished_tasks)()

        log.debug(f'Pausing to allow the remaining {len(tasks)} tasks to complete...')
        # Loop, allowing all other tasks to complete after seeing self.cancel is set
        for i in range(len(tasks) * 2):
            await asyncio.sleep(0.001)

        # Remove any tasks that have completed from the list.
        await wait_for_finished_tasks()

        # Cancel the remaining tasks.
        __cancel_tasks(tasks)

    return cancel_handler


if __name__ == '__main__':

    memory.report_memory_usage()

    log.set_log_level(log.CRITICAL)
    log.info(f'Is running on a microcontroller: {environment.is_running_on_microcontroller()}')


    async def runs_forever_task():
        while True:
            log.debug("LOOP: runs_forever_task")
            await asyncio.sleep(2.0)


    async def completes_task():
        log.debug("START: completes_task")
        await asyncio.sleep(0.005)
        log.debug("FINISH: completes_task")


    async def raises_exception_task():
        log.debug("START: raises_exception_task")
        await asyncio.sleep(0.005)
        log.debug("EXCEPTION: raises_exception_task")
        raise Exception("Raised by task 3")


    i: int = 0


    async def callback() -> None:
        global i, cancel
        i += 1
        log.debug(f'Callback: i={i}')
        cancel = i == 30


    async def __execute():
        __tasks_to_run: list[Callable[[], Awaitable[None]]] = []
        __internal_loop_sleep_interval = 0.0

        tasks: list[asyncio.Task] = [
            asyncio.create_task(__new_task_handler(task)()) for task in
            [runs_forever_task, completes_task, raises_exception_task]]

        try:
            await asyncio.gather(
                asyncio.create_task(__new_scheduled_task_handler(callback)()),
                asyncio.create_task(__cancellation_handler(tasks)()),
                *tasks)

        except asyncio.CancelledError:
            log.error('Caught CancelledError exception cancelling tasks!')

        except Exception as e:
            log.error(f'Caught the following exception cancelling tasks: {e}!')
            log.stacktrace(e)


    asyncio.run(__execute())

    memory.report_memory_usage_and_free()
