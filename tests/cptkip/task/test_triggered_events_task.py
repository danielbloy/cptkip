from typing import Any

import pytest

from cptkip.task.basic_runner import run
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

# TODO: Finish tests
