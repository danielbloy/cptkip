import asyncio
from time import time

import pytest

from cptkip.core.control import ASYNC_LOOP_SLEEP_INTERVAL
from cptkip.task.triggered_task_async import create

# This is the minimum number of updates per second we expect func to be called.
MIN_UPDATES_PER_SECOND = 100


class ContinueCount:
    def __init__(self, count):
        self.left = count

    def __call__(self) -> bool:
        self.left -= 1
        return self.left >= 0


class ContinueDuration:
    def __init__(self, seconds):
        self.seconds = seconds
        self.__end = None

    def __call__(self) -> bool:
        if self.__end is None:
            self.__end = time() + self.seconds

        return time() < self.__end


class Trigger:
    triggered: bool

    def __init__(self, triggered: bool) -> None:
        self.triggered = triggered

    def __call__(self) -> bool:
        result = self.triggered
        self.triggered = False
        return result


class TestTriggeredTask:

    def test_task_never_called(self) -> None:
        """
        Validates that the returned task terminates straight away
        when the continue_func always returns False.
        """
        called = False

        async def task():
            nonlocal called
            called = True

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, duration=1.0, func=task, continue_func=lambda: False)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())
        assert not called

    def test_task_stops(self) -> None:
        """
        Validates that the returned task terminates when the continue_func returns False.
        """

        continue_fn = ContinueCount(2)

        called = 0

        async def task():
            nonlocal called
            called += 1

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, duration=1.0, func=task, continue_func=continue_fn)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())
        assert called == 2

    def test_task_not_triggered(self) -> None:
        """
        Validates that the task is not called when not triggered.
        """

        continue_fn = ContinueCount(20)

        begin_called = 0
        func_called = 0
        end_called = 0

        async def begin():
            nonlocal begin_called
            begin_called += 1

        async def func():
            nonlocal func_called
            func_called += 1

        async def end():
            nonlocal end_called
            end_called += 1

        trigger = Trigger(triggered=False)
        trigger_task = create(trigger, duration=1.0, begin=begin, func=func, end=end,
                              continue_func=continue_fn)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())
        assert begin_called == 0
        assert func_called == 0
        assert end_called == 0

    def test_task_called_multiple_times(self) -> None:
        """
        Validates that the returned task terminates after having been
        called multiple times.
        """

        continue_fn = ContinueCount(20)

        called = 0

        async def task():
            nonlocal called
            called += 1

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, duration=1.0, func=task, continue_func=continue_fn)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())
        assert called > 2
        assert called == 20

    def test_run_invokes_triggered_task_callback_with_sensible_frequency(self) -> None:
        """
        Validates that func gets called at a reasonable frequency.
        """
        called_count: int = 0
        seconds_to_run: int = 2

        async def task():
            nonlocal called_count
            called_count += 1
            await asyncio.sleep(ASYNC_LOOP_SLEEP_INTERVAL)

        continue_fn = ContinueDuration(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, duration=seconds_to_run, func=task,
                              continue_func=continue_fn)

        begin = time()
        # noinspection PyTypeChecker
        asyncio.run(trigger_task())
        end = time()

        assert (end - begin) < (seconds_to_run * 1.05)
        assert (end - begin) > (seconds_to_run * 0.95)
        assert called_count >= (seconds_to_run * MIN_UPDATES_PER_SECOND)

    def test_triggered_task_errors_with_no_callback(self) -> None:
        """
        Validates an error is raised when create() is invoked
        without a begin, func or end.
        """
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            create(lambda: True, duration=0.1)

    def test_triggered_task_invokes_start_callback(self) -> None:
        """
        Validates that the begin callback is called when the task is triggered.
        """
        called_count: int = 0
        seconds_to_run: int = 2

        async def task():
            nonlocal called_count
            called_count += 1
            await asyncio.sleep(ASYNC_LOOP_SLEEP_INTERVAL)

        continue_fn = ContinueDuration(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, duration=1.0, begin=task, continue_func=continue_fn)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())

        assert called_count == 1

    def test_triggered_task_invokes_run_callback(self) -> None:
        """
        Validates that the func callback is called repeatedly when the task is triggered.
        """
        called_count: int = 0
        seconds_to_run: int = 2

        async def task():
            nonlocal called_count
            called_count += 1
            await asyncio.sleep(ASYNC_LOOP_SLEEP_INTERVAL)

        continue_fn = ContinueDuration(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, duration=1.0, func=task, continue_func=continue_fn)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())

        assert called_count >= (seconds_to_run * MIN_UPDATES_PER_SECOND)

    def test_triggered_task_invokes_stop_callback(self) -> None:
        """
        Validates that the end callback is called when the triggered task expires.
        """
        called_count: int = 0
        seconds_to_run: int = 2

        async def task():
            nonlocal called_count
            called_count += 1
            await asyncio.sleep(ASYNC_LOOP_SLEEP_INTERVAL)

        continue_fn = ContinueDuration(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, duration=1.0, end=task, continue_func=continue_fn)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())

        assert called_count == 1

    def test_triggered_task_callbacks_invoked_in_correct_order(self) -> None:
        """
        Validates that the begin, func and end callbacks are called in the correct
        order when the task is triggered.
        """
        seconds_to_run: int = 2

        begin_time = 0
        end_time = 0
        run_begin_time = -1
        run_end_time = 0

        async def begin():
            nonlocal begin_time
            begin_time = time()
            await asyncio.sleep(ASYNC_LOOP_SLEEP_INTERVAL)

        async def func():
            nonlocal run_begin_time, run_end_time
            await asyncio.sleep(ASYNC_LOOP_SLEEP_INTERVAL)
            if run_begin_time < 0:
                run_begin_time = time()
            run_end_time = time()

        async def end():
            nonlocal end_time
            end_time = time()
            await asyncio.sleep(ASYNC_LOOP_SLEEP_INTERVAL)

        continue_fn = ContinueDuration(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, duration=1.0, begin=begin, func=func, end=end,
                              continue_func=continue_fn)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())

        assert begin_time < run_begin_time
        assert run_begin_time < run_end_time
        assert run_end_time < end_time

    def test_triggered_tasks_do_not_overlap(self) -> None:
        """
        Validates that a second triggered task does not get invoked when it has
        already been triggered and is still running.
        """
        seconds_to_run: int = 2

        begin_count = 0
        end_count = 0

        async def begin():
            nonlocal begin_count
            begin_count += 1
            await asyncio.sleep(ASYNC_LOOP_SLEEP_INTERVAL)

        async def func():
            trigger.triggered = True
            await asyncio.sleep(ASYNC_LOOP_SLEEP_INTERVAL)

        async def end():
            nonlocal end_count
            end_count += 1
            await asyncio.sleep(ASYNC_LOOP_SLEEP_INTERVAL)

        continue_fn = ContinueDuration(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, duration=1.0, begin=begin, func=func, end=end,
                              continue_func=continue_fn)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())

        assert begin_count == 1
        assert end_count == 1

    def test_triggered_task_can_be_retriggered(self) -> None:
        """
        Validates the task can be triggered a second time once the first trigger
        has completed.
        """
        seconds_to_run: int = 2

        begin_count = 0

        async def restart():
            await asyncio.sleep(1.2)
            trigger.triggered = True

        async def begin():
            nonlocal begin_count
            begin_count += 1
            delayed_restart = asyncio.create_task(restart())

        continue_fn = ContinueDuration(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, duration=1.0, begin=begin, continue_func=continue_fn)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())

        assert begin_count == 2
