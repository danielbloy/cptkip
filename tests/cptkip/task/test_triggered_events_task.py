from math import trunc
from time import monotonic
from typing import Any

import pytest

from cptkip.task.basic_runner import run
from cptkip.task.limiters import count_limiter, duration_limiter
from cptkip.task.triggered_events_task import create, Trigger


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

    # noinspection bad-argument-type
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
        assert values == ["A", "STOP"]

    def test_task_not_triggered(self) -> None:
        """
        Validates that the task is not called when not triggered.
        """

        continue_fn = count_limiter(20)

        begin_called = 0
        func_called = 0
        end_called = 0

        def begin():
            nonlocal begin_called
            begin_called += 1

        def callback(_: Any):
            nonlocal func_called
            func_called += 1

        def end():
            nonlocal end_called
            end_called += 1

        trigger = Trigger(triggered=False)
        trigger_task = create(trigger, events=[(0.0,), (1.0,), (2.0,)], begin=begin,
                              callback=callback, end=end, continue_func=continue_fn)

        # noinspection PyTypeChecker
        run(trigger_task)
        assert begin_called == 0
        assert func_called == 0
        assert end_called == 0

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

    def test_invokes_end_callback_with_early_exit(self) -> None:
        """
        Validates that the end callback is called when the task is cancelled
        early and the trigger has not expired.
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
            events=[(0.0,), (0.1,), (1.2,)],
            end=end,
            callback=callback,
            continue_func=continue_fn)

        # noinspection PyTypeChecker
        run(trigger_task)

        assert called_count == 1

    def test_callbacks_invoked_in_correct_order(self) -> None:
        """
        Validates that the begin, event and end callbacks are called in the correct
        order when the task is triggered. This also validates that the correct
        value is passed to the callback.
        """
        seconds_to_run: int = 2

        values = []

        def begin():
            values.append("begin")

        def callback(value: str):
            values.append(value)

        def end():
            values.append("end")

        continue_fn = duration_limiter(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(
            trigger,
            # Some of these events are specified in the wrong order
            events=[(0.0, "a"), (1.1, "d"), (0.2, "b"), (0.8, "c"), (1.2, "e")],
            begin=begin,
            end=end,
            callback=callback,
            continue_func=continue_fn)

        # noinspection PyTypeChecker
        run(trigger_task)

        assert values == ["begin", "a", "b", "c", "d", "e", "end"]

    def test_callbacks_at_correct_interval(self) -> None:
        """
        Validates that the event callbacks are called at the correct time
        interval.
        """
        seconds_to_run: int = 2

        values = []
        times = []

        def callback(value: str):
            now = monotonic()
            times.append(now - start)
            values.append(value)

        continue_fn = duration_limiter(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(
            trigger,
            # Some of these events are specified in the wrong order
            events=[(0.0, "a"), (0.23, "b"), (0.80, "c"), (1.1, "d"), (1.2, "e")],
            callback=callback,
            continue_func=continue_fn)

        start = monotonic()
        # noinspection PyTypeChecker
        run(trigger_task)

        assert values == ["a", "b", "c", "d", "e"]

        # Validate that times are correct to within 3 decimal places
        times = [trunc(time * 100) for time in times]
        times = [time / 100 for time in times]
        assert times == [0.00, 0.23, 0.80, 1.10, 1.20]

    def test_correct_callback_is_called(self) -> None:
        """
        Validates that the correct event callback is called.
        """
        seconds_to_run: int = 2

        values = []

        def callback(value: str):
            values.append(f"callback: {value}")

        def a_callback(value: str):
            values.append(f"a_callback: {value}")

        def c_callback(value: str):
            values.append(f"c_callback: {value}")

        def d_callback(value: str):
            values.append(f"d_callback: {value}")

        continue_fn = duration_limiter(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(
            trigger,
            # Some of these events are specified in the wrong order
            events=[
                (0.0, "a", a_callback),
                (0.23, "b"),
                (0.801, "c", c_callback),
                (1.1, "d", d_callback),
                (1.2, "e")
            ],
            callback=callback,
            continue_func=continue_fn)

        # noinspection PyTypeChecker
        run(trigger_task)

        assert values == [
            "a_callback: a",
            "callback: b",
            "c_callback: c",
            "d_callback: d",
            "callback: e"
        ]

    def test_tasks_do_not_overlap(self) -> None:
        """
        Validates that a second triggered task does not get invoked when it has
        already been triggered and is still running.
        """
        seconds_to_run: int = 2

        begin_count = 0
        end_count = 0

        def begin():
            nonlocal begin_count
            begin_count += 1

        def callback(_: Any):
            trigger.triggered = True

        def end():
            nonlocal end_count
            end_count += 1

        continue_fn = duration_limiter(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(
            trigger,
            events=[(0.0,), (0.1,), (0.2,), (0.3,), (0.4,), (0.5,), (1.0,)],
            begin=begin,
            end=end,
            callback=callback,
            continue_func=continue_fn)

        # noinspection PyTypeChecker
        run(trigger_task)

        assert begin_count == 1
        assert end_count == 1

    def test_task_can_be_retriggered(self) -> None:
        """
        Validates the task can be triggered a second time once the first trigger
        has completed.
        """
        seconds_to_run: int = 2

        begin_count = 0

        def restart():
            nonlocal restart_time

            now = monotonic()
            if now >= restart_time:
                trigger.triggered = True
                restart_time = now + 0.7

            return continue_fn()

        def begin():
            nonlocal begin_count
            begin_count += 1

        def callback(_: Any):
            pass

        continue_fn = duration_limiter(seconds_to_run)

        trigger = Trigger(triggered=True)
        trigger_task = create(
            trigger,
            events=[(0.0,), (0.1,), (0.2,), (0.3,), (0.4,), (0.5,)],
            begin=begin,
            callback=callback,
            continue_func=continue_fn)

        # noinspection PyTypeChecker
        restart_time = monotonic() + 0.7
        run(trigger_task, restart)

        assert begin_count == 3
