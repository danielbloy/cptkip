import asyncio
from typing import Any

import pytest

from cptkip.task.triggered_events_task_async import create, Trigger
from tests.cptkip.utilities import count_limiter

# This is the minimum number of updates per second we expect func to be called.
MIN_UPDATES_PER_SECOND = 100


class TestTriggeredEventsTaskAsync:

    def test_error_when_no_event_callback(self) -> None:
        """
        Validates that callback must be specified if an event does not
        contain an event callback.
        """

        async def callback(_: Any):
            pass

        with pytest.raises(ValueError):
            create(lambda: False, events=[(0.0,), ])

        create(lambda: False, events=[(0.0,)], callback=callback)
        create(lambda: False, events=[(0.0, None, callback)])

        with pytest.raises(ValueError):
            create(lambda: False, events=[(0.0,), (0.0,), (0.0,)])

        with pytest.raises(ValueError):
            create(lambda: False, events=[(0.0, None, callback), (0.0,), (0.0, None, callback)])

        create(lambda: False, events=[(0.0, None, callback), (0.0,), (0.0, None, callback)],
               callback=callback)

    def test_event_contains_tuples(self) -> None:
        """
        Validates that events must contain tuples with 1, 2 or 3 elements.
        """

        async def callback(_: Any):
            pass

        with pytest.raises(ValueError):
            create(lambda: False, events=[0])

        with pytest.raises(ValueError):
            create(lambda: False, events=[(0,), "W"])

        # Single tuple value is okay if int or float
        create(lambda: False, events=[(0,)], callback=callback)
        create(lambda: False, events=[(0.0,)], callback=callback)
        create(lambda: False, events=[(1,)], callback=callback)
        create(lambda: False, events=[(1.1,)], callback=callback)

        # But fails if another type.
        with pytest.raises(ValueError):
            create(lambda: False, events=[(None,)])
        with pytest.raises(ValueError):
            create(lambda: False, events=[("W",)])
        with pytest.raises(ValueError):
            create(lambda: False, events=[([],)])

        # Dual tuple value is okay
        create(lambda: False, events=[(0, None)], callback=callback)

        # Triple tuple value is okay if callable (even if the wrong type of callable.
        create(lambda: False, events=[(0, "A", lambda: False)])

        # Triple fails if not callable
        with pytest.raises(ValueError):
            create(lambda: False, events=[(0, "A", 2.3)])

        # Fails if more than 4 items
        with pytest.raises(ValueError):
            create(lambda: False, events=[(0, "A", callback, "extra")])

        # It is valid to mix them.
        create(lambda: False, events=[(0,), (4, "D"), (0, "A", callback)], callback=callback)

        # Its also fine if it contains no entries
        create(lambda: False, events=[])

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

    def test_task_not_triggered(self) -> None:
        """
        Validates that the task is not called when not triggered.
        """

        continue_fn = count_limiter(20)

        begin_called = 0
        func_called = 0
        end_called = 0

        async def begin():
            nonlocal begin_called
            begin_called += 1

        async def callback(_: Any):
            nonlocal func_called
            func_called += 1

        async def end():
            nonlocal end_called
            end_called += 1

        trigger = Trigger(triggered=False)
        trigger_task = create(trigger, events=[(0.0,), (1.0,), (2.0,)], begin=begin,
                              callback=callback, end=end, continue_func=continue_fn)

        # noinspection PyTypeChecker
        asyncio.run(trigger_task())
        assert begin_called == 0
        assert func_called == 0
        assert end_called == 0
