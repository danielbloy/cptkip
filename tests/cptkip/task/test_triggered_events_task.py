from typing import Any

import pytest

from cptkip.task.basic_runner import run
from cptkip.task.triggered_events_task import create, Trigger
from cptkip.utilities import count_limiter, duration_limiter


class TestTriggeredEventsTask:

    def test_error_when_no_event_callback(self) -> None:
        """
        Validates that callback must be specified if an event does not
        contain an event callback.
        """

        def callback(_: Any):
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

        def callback(_: Any):
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

        def callback(obj: Any):
            nonlocal called
            called = True

        trigger = Trigger(triggered=True)
        trigger_task = create(
            trigger,
            events=[(0.0,), (0.0,), (0.0,)],
            callback=callback,
            continue_func=lambda: False)

        # noinspection PyTypeChecker
        run(trigger_task)
        assert not called

    def test_task_stops(self) -> None:
        """
        Validates that the returned task terminates when the continue_func returns False.
        """

        # First we limit ourselves to just the first element based on the number of
        # times we call continue_fn
        continue_fn = count_limiter(4)

        values = []

        def callback(value: str) -> None:
            nonlocal values
            values.append(value)

        trigger = Trigger(triggered=True)
        trigger_task = create(
            trigger,
            events=[(0.0, "A"), (1.0, "B"), (2.0, "C")],
            callback=callback,
            continue_func=continue_fn)

        # noinspection PyTypeChecker
        run(trigger_task)
        assert len(values) == 1
        assert values == ["A"]

        # Now we limit ourselves based on the "STOP" value
        keep_going = True
        values = []

        def callback(value: str) -> None:
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
        run(trigger_task)
        assert len(values) == 2
        assert values == ["A", "STOP"]

    # TODO: Make sure each event is called exactly once.
    # TODO: Make sure the correct value is passed back to the callback.
    # TODO: Make sure the correct callback is called.
    # TODO: Make sure the events are called in the correct order (even when specified out of order).

    def test_invokes_begin_callback(self) -> None:
        """
        Validates that the begin callback is called when the task is triggered.
        """
        called_count: int = 0
        seconds_to_run: int = 1

        def begin():
            nonlocal called_count
            called_count += 1

        def callback(_: str) -> None:
            pass

        continue_fn = duration_limiter(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(
            trigger,
            events=[(0.0,), (0.1,), (1.2,)],
            begin=begin,
            callback=callback,
            continue_func=continue_fn)

        # noinspection PyTypeChecker
        run(trigger_task)

        assert called_count == 1

    def test_invokes_end_callback(self) -> None:
        """
        Validates that the end callback is called when the triggered task expires.
        """
        called_count: int = 0
        seconds_to_run: int = 1

        def end():
            nonlocal called_count
            called_count += 1

        def callback(_: str) -> None:
            pass

        continue_fn = duration_limiter(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(
            trigger,
            events=[(0.0,), (0.1,), (0.2,)],
            end=end,
            callback=callback,
            continue_func=continue_fn)

        # noinspection PyTypeChecker
        run(trigger_task)

        assert called_count == 1
