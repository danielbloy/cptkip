from asyncio import sleep, CancelledError
from time import monotonic_ns

import cptkip.core.environment as environment
from cptkip.core.control import NS_PER_SECOND, ASYNC_LOOP_SLEEP_INTERVAL, PERIODIC_LOOP_WAIT_RATIO

if environment.is_running_on_desktop():
    from typing import Callable, Awaitable


def create(
        func: Callable[[], Awaitable[None]],
        frequency: int = 0,
        continue_func: Callable[[], bool] | None = None,
        begin: Callable[[], Awaitable[None]] | None = None,
        end: Callable[[], Awaitable[None]] | None = None,
        initial_delay: float = 0.0) -> Callable[[], Awaitable[None]]:
    """
    Creates an asynchronous function that will execute the given function at the
    specified frequency for as long as the continue_func returns true. The initial
    invocation of func can be delayed by setting an initial_delay. If a frequency
    of zero is provided then func will be executed as fast as possible. A frequency
    of less than zero is ignored.

    :param func: The function to call.
    :param frequency: The frequency to execute the function at. Zero indicates as
        fast as possible.
    :param continue_func: If specified, this will be periodically called to confirm
        the func should continue to be called.
    :param begin: If specified, this will be executed once at the beginning
        and before any initial delay. It always runs before continue_func is
        first consulted, so it runs even if continue_func would immediately
        return False - in that case end (if specified) then runs right after.
    :param end: If specified, this will be executed once at the end. This includes
        when the task is cancelled, e.g. by an async runner's continue_func.
    :param initial_delay: If specified, this will delay the first invocation of
        func by the specified number of seconds. A value of less than zero is ignored.
    """

    # Integer division keeps the period exact: on CircuitPython floats are only
    # 30-bit, so (1 / frequency) * NS_PER_SECOND would drift (e.g. 3 Hz gave
    # 333_333_344 ns). A period of at least 1 ns prevents an endless catch-up loop
    # for absurdly high frequencies.
    interval_ns: int = 0
    if frequency > 0:
        interval_ns = max(1, int(NS_PER_SECOND // frequency))
    call_begin: bool = True
    call_end: bool = True

    # The longest single sleep: a fraction of the period so continue_func is still
    # checked regularly. With no frequency the task runs as fast as possible.
    max_sleep_ns = interval_ns // PERIODIC_LOOP_WAIT_RATIO

    def _sleep_time(next_callback_ns: int) -> float:
        """
        Seconds to sleep before the next check: until func is next due, capped at a
        fraction of the period. Previously this always slept for ~1us, busy-waiting.
        """
        if max_sleep_ns <= 0:
            return ASYNC_LOOP_SLEEP_INTERVAL
        remaining_ns = next_callback_ns - monotonic_ns()
        if remaining_ns <= 0:
            return ASYNC_LOOP_SLEEP_INTERVAL
        return min(remaining_ns, max_sleep_ns) / NS_PER_SECOND

    async def handler() -> None:
        nonlocal call_begin, call_end

        if begin and call_begin:
            call_begin = False
            await begin()

        next_callback_ns = monotonic_ns() + int(
            max(initial_delay, 0.0) * NS_PER_SECOND)

        try:
            while not continue_func or continue_func():

                now = monotonic_ns()

                if now >= next_callback_ns:
                    if frequency > 0:
                        # Skip any missed periods in one step rather than looping.
                        next_callback_ns += ((now - next_callback_ns) // interval_ns + 1) * interval_ns
                    await func()

                await sleep(_sleep_time(next_callback_ns))

        except CancelledError:
            # Run end before propagating the cancellation, so cancelling the task
            # (as the async runners do) still gives it the chance to clean up.
            if end and call_end:
                call_end = False
                await end()
            raise

        if end and call_end:
            call_end = False
            await end()

    return handler
