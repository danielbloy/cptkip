import asyncio
from typing import Any

from cptkip.task.triggered_events_task_async import create, Trigger
from tests.cptkip.utilities import count_limiter

# This is the minimum number of updates per second we expect func to be called.
MIN_UPDATES_PER_SECOND = 100


class TestTriggeredEventsTaskAsync:

    def test_task_never_called(self) -> None:
        """
        Validates that the returned task terminates straight away
        when the continue_func always returns False.
        """
        called = False

        async def callback(_: Any):
            nonlocal called
            called = True

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, events=[(0.0,), (0.0,), (0.0,)], callback=callback,
                              continue_func=lambda: False)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())
        assert not called

    def test_task_stops(self) -> None:
        """
        Validates that the returned task terminates when the continue_func returns False.
        """
        # First we limit ourselves to just the first element based on the number of
        # times we call continue_fn
        continue_fn = count_limiter(2)

        values = []

        async def callback(value: Any):
            nonlocal values
            values.append(value)

        trigger = Trigger(triggered=True)
        trigger_task = create(trigger, events=[(0.0, "A"), (1.0, "B"), (2.0, "C")],
                              callback=callback,
                              continue_func=continue_fn)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())
        assert len(values) == 1
        assert values == ["A"]

        # Now we limit ourselves based on the "STOP" value
        keep_going = True
        values = []

        async def callback(value: str) -> None:
            nonlocal values, keep_going
            values.append(value)
            keep_going = value != "STOP"

        trigger = Trigger(triggered=True)
        trigger_task = create(
            trigger,
            events=[(0.0, "A"), (0.1, "STOP"), (0.2, "C")],
            callback=callback,
            continue_func=lambda: keep_going)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())
        assert values == ["A", "STOP"]
