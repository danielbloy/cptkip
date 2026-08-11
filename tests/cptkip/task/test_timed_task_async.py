import pytest


# TODO: implement
@pytest.mark.skip(reason="not converted yet")
class TestTriggerTimedEvents:
    def test_calling_start(self) -> None:
        """
        Validates that calling start works when called once, twice or more times.
        In these tests, there are no events to fire so it is a basic test. More
        complex tests are performed later.
        """
        trigger = TriggerTimedEvents()
        assert not trigger.running
        assert len(trigger.events) == 0

        # Start the trigger
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 0

        # Calling start a second time should have no effect
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 0

        # And calling it a third time should have no effect
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 0

    def test_calling_start_multiple_times(self) -> None:
        """
        Validates that calling start works when called once, twice or more times.
        In these tests there are events to fire. It also validates that calling
        start multiple times does not affect the timing of events.
        """
        trigger = TriggerTimedEvents()
        trigger.add_event(0, 90)
        trigger.add_event(99, 99)
        assert not trigger.running
        assert len(trigger.events) == 2

        # Start the trigger which should immediately fire one event.
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 2
        events = trigger.run()
        assert trigger.running
        assert len(events) == 1
        assert events[0].event == 90

        # Starting the trigger again should result in no more additional events.
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 2
        events = trigger.run()
        assert len(events) == 0

    def test_calling_stop_when_not_started(self) -> None:
        """
        Validates that calling stop works even when the trigger is not running.
        """
        trigger = TriggerTimedEvents()
        assert not trigger.running
        assert len(trigger.events) == 0

        # Stop the trigger, nothing should happen.
        trigger.stop()
        assert not trigger.running
        assert len(trigger.events) == 0

        # Stop the trigger again, again nothing should happen.
        trigger.stop()
        assert not trigger.running
        assert len(trigger.events) == 0

    def test_calling_stop_when_running(self) -> None:
        """
        Validates that calling stop on a running trigger will cancel any events
        that are queued up to run.
        """
        trigger = TriggerTimedEvents()
        trigger.add_event(0, 90)
        trigger.add_event(99, 99)
        assert not trigger.running
        assert len(trigger.events) == 2

        # Start the trigger which should immediately make one event ready to fire (but don't call run)
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 2

        # Now stop the trigger which cancels the events. (we actually call reset() here to test it calls stop())
        trigger.reset()
        assert not trigger.running
        assert len(trigger.events) == 2

        # Call run() which should return no events.
        events = trigger.run()
        assert not trigger.running
        assert len(events) == 0

    def test_starting_and_stopping_multiple_times(self) -> None:
        """
        Validates that calling starting and stopping the trigger multiple times
        results in the events being triggered correctly each time.
        """
        trigger = TriggerTimedEvents()
        trigger.add_event(0, 90)
        trigger.add_event(0.1, 91)
        assert not trigger.running
        assert len(trigger.events) == 2

        # Start the trigger which should immediately fire one event.
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 2
        events = trigger.run()
        assert trigger.running
        assert len(events) == 1
        assert events[0].event == 90

        # Wait long enough that we should have another event ready to fire.
        time.sleep(0.2)

        # Stop the trigger, which cancels any remaining events
        trigger.stop()
        assert not trigger.running
        assert len(trigger.events) == 2

        # Call run which returns nothing
        events = trigger.run()
        assert not trigger.running
        assert len(events) == 0

        # Call start again and we should see a single event.
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 2
        events = trigger.run()
        assert trigger.running
        assert len(events) == 1
        assert events[0].event == 90

    def test_running_without_any_events(self) -> None:
        """
        Validates that the trigger can be run without any events registered.
        """
        trigger = TriggerTimedEvents()
        assert not trigger.running
        assert len(trigger.events) == 0

        # Start the trigger, this should indicate that the trigger is running.
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 0

        # Call run, which will detect there are no events and will stop the trigger.
        events = trigger.run()
        assert not trigger.running
        assert len(events) == 0

        # Now we will check that stop works with no events.
        # Start the trigger again, this should indicate that the trigger is running.
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 0

        trigger.stop()
        assert not trigger.running

    def test_running_with_a_single_event(self) -> None:
        """
        Validates that the trigger can be run with just a single event registered.
        """
        trigger = TriggerTimedEvents()
        trigger.add_event(0.1, 90)
        assert not trigger.running
        assert len(trigger.events) == 1

        # Start the trigger, this should indicate that the trigger is running.
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 1

        # Call run which will not see any expired events and everything continues to run
        events = trigger.run()
        assert trigger.running
        assert len(events) == 0

        # Pause long enough to guarantee the event will trigger
        time.sleep(0.2)

        # Call run again, which will detect there are is a single event which has fired
        # and return it. The trigger will also be marked as not running at this point.
        events = trigger.run()
        assert not trigger.running
        assert len(events) == 1
        assert events[0].event == 90

    def test_running_with_multiple_events_with_same_time(self) -> None:
        """
        Validates that the trigger can be run with multiple events registered
        for the same time.
        """
        trigger = TriggerTimedEvents()
        trigger.add_event(0.05, 91)
        trigger.add_event(0.05, 90)
        assert not trigger.running
        assert len(trigger.events) == 2

        # Start the trigger, this should indicate that the trigger is running.
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 2

        # Pause long enough to guarantee the events will trigger
        time.sleep(0.15)

        # Call run, which will detect there are two events which have fired and
        # return them. The trigger will also be marked as not running at this point.
        events = trigger.run()
        assert not trigger.running
        assert len(events) == 2
        assert set([event.event for event in events]) == {90, 91}

    def test_running_with_multiple_events_with_different_times(self) -> None:
        """
        Validates that the trigger can be run with multiple events registered
        for multiple times.
        """
        trigger = TriggerTimedEvents()
        trigger.add_event(0, 90)
        trigger.add_event(0.08, 13)
        trigger.add_event(0.1, 81)
        trigger.add_event(0.1, 82)
        trigger.add_event(0.3, 103)
        assert not trigger.running
        assert len(trigger.events) == 5

        # Start the trigger, this should indicate that the trigger is running.
        trigger.start()
        assert trigger.running
        assert len(trigger.events) == 5

        # The first event fires straight away.
        events = trigger.run()
        assert trigger.running
        assert len(events) == 1
        assert events[0].event == 90

        # Pause long enough to guarantee the next events will trigger but leaving 1.
        time.sleep(0.2)

        # Call run, which will detect there are three events which have fired and
        # return them. The trigger will still be running at this point.
        events = trigger.run()
        assert trigger.running
        assert len(events) == 3
        assert set([event.event for event in events]) == {13, 81, 82}

        # Pause long enough to guarantee the last event will trigger but leaving 1.
        time.sleep(0.2)

        # Call run, which will detect there is a single event which has fired and
        # return it. The trigger will also be marked as not running at this point.
        events = trigger.run()
        assert not trigger.running
        assert len(events) == 1
        assert events[0].event == 103


class TestOneTimeOnOffTask:
    def test_errors_with_less_than_1_cycle(self) -> None:
        """
        Validates an error is raised when new_one_time_on_off_task() is invoked
        with cycles of less than 1.
        """

        def on_duration():
            return 0.1

        def off_duration():
            return 0.1

        async def on():
            pass

        async def off():
            pass

        async def finish():
            pass

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            new_one_time_on_off_task(0, on_duration, off_duration, on, off, finish)

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            new_one_time_on_off_task(-1, on_duration, off_duration, on, off, finish)

    def test_errors_with_no_on_or_off_duration(self) -> None:
        """
        Validates an error is raised when new_one_time_on_off_task() is invoked
        with either of the on or off duration not specified.
        """

        def on_duration():
            return 0.1

        def off_duration():
            return 0.1

        async def on():
            pass

        async def off():
            pass

        async def finish():
            pass

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            new_one_time_on_off_task(1, None, off_duration, on, off, finish)

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            new_one_time_on_off_task(1, on_duration, None, on, off, finish)

    def test_errors_with_no_on_off_or_finish(self) -> None:
        """
        Validates an error is raised when new_one_time_on_off_task() is invoked
        with one of the on, off or finish functions are not specified.
        """

        def on_duration():
            return 0.1

        def off_duration():
            return 0.1

        async def on():
            pass

        async def off():
            pass

        async def finish():
            pass

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            new_one_time_on_off_task(1, on_duration, off_duration, None, None, None)

        # These should all be okay.
        # noinspection PyTypeChecker
        new_one_time_on_off_task(1, on_duration, off_duration, None, off, None)
        # noinspection PyTypeChecker
        new_one_time_on_off_task(1, on_duration, off_duration, on, None, None)
        # noinspection PyTypeChecker
        new_one_time_on_off_task(1, on_duration, off_duration, None, None, finish)

    def test_task_never_called(self) -> None:
        """
        Validates that the returned task terminates straight away
        when the terminate_func always returns true.
        """

        cancellable = Cancellable()
        cancel_fn = terminate_on_cancel(cancellable)
        cancellable.cancel = True

        on_called = False

        async def on_task():
            nonlocal on_called
            on_called = True

        off_called = False

        async def off_task():
            nonlocal off_called
            off_called = True

        finish_called = False

        async def finish_task():
            nonlocal finish_called
            finish_called = True

        on_off_task = (
            new_one_time_on_off_task(5, lambda: 1, lambda: 1,
                                     on_task, off_task, finish_task, cancel_fn))

        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert not on_called
        assert not off_called
        assert not finish_called

    def test_task_stops(self) -> None:
        """
        Validates that the returned task terminates
        when the terminate_func returns true.
        """

        cancellable = CancellableCount(2)
        cancel_fn = terminate_on_cancel(cancellable)

        on_called = 0

        async def on_task():
            nonlocal on_called
            on_called += 1

        off_called = 0

        async def off_task():
            nonlocal off_called
            off_called += 1

        finish_called = 0

        async def finish_task():
            nonlocal finish_called
            finish_called += 1

        # NOTE: The on and off duration intervals are much longer than the cancel polling intervals
        #       so we only expect the initial on event to be called.
        on_off_task = (
            new_one_time_on_off_task(5, lambda: 1, lambda: 1,
                                     on_task, off_task, finish_task, cancel_fn))

        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert on_called == 1
        assert off_called == 0
        assert finish_called == 0
        assert cancellable.cancel

    def test_creates_correct_number_of_events(self) -> None:
        """
        Validates that the correct number of events are created and in the correct order.
        This also validates that the events are fired in the correct order and the correct
        time. We do not do variable timings as that is done later.
        """

        def check_event_order(count, on_duration, off_duration) -> None:
            cancel_fn = never_terminate

            on_events = []

            async def on_task():
                nonlocal on_events
                on_events.append(time.monotonic_ns())

            off_events = []

            async def off_task():
                nonlocal off_events
                off_events.append(time.monotonic_ns())

            finish_events = []

            async def finish_task():
                nonlocal finish_events
                finish_events.append(time.monotonic_ns())

            on_off_task = (
                new_one_time_on_off_task(count, lambda: on_duration, lambda: off_duration,
                                         on_task, off_task, finish_task, cancel_fn))

            # noinspection PyTypeChecker
            asyncio.run(on_off_task())
            assert len(on_events) == count
            assert len(off_events) == count
            assert len(finish_events) == 1

            # Check the on and off events are contiguous respective to themselves
            # with a reasonable difference of +/- 10%.
            for idx in range(count - 1):
                assert on_events[idx] < on_events[idx + 1]
                assert (on_events[idx + 1] - on_events[idx]) <= (
                        on_duration + off_duration) * NANO * 1.1
                assert (on_events[idx + 1] - on_events[idx]) >= (
                        on_duration + off_duration) * NANO * 0.9

                assert off_events[idx] < off_events[idx + 1]
                assert (off_events[idx + 1] - off_events[idx]) <= (
                        on_duration + off_duration) * NANO * 1.1
                assert (off_events[idx + 1] - off_events[idx]) >= (
                        on_duration + off_duration) * NANO * 0.9

            # Check the on to off events are sent in the correct order and within
            # a reasonable difference of +/- 10%.
            for idx in range(count):
                assert on_events[idx] < off_events[idx]
                assert (off_events[idx] - on_events[idx]) <= (on_duration * NANO * 1.1)
                assert (off_events[idx] - on_events[idx]) >= (on_duration * NANO * 0.9)

            # Check the off to on events are sent in the correct order and within
            # a reasonable difference of +/- 10%.
            for idx in range(count - 1):
                assert off_events[idx] < on_events[idx + 1]
                assert (on_events[idx + 1] - off_events[idx]) <= (off_duration * NANO * 1.1)
                assert (on_events[idx + 1] - off_events[idx]) >= (off_duration * NANO * 0.9)

            # Check that the finish event is after the last off event and within
            # a reasonable difference of +/- 10%
            assert off_events[count - 1] < finish_events[0]
            assert (finish_events[0] - off_events[count - 1]) <= (off_duration * NANO * 1.1)
            assert (finish_events[0] - off_events[count - 1]) >= (off_duration * NANO * 0.9)

        check_event_order(1, 0.1, 0.1)
        check_event_order(3, 0.1, 0.2)
        check_event_order(5, 0.2, 0.1)

    def test_creates_events_with_variable_on_durations(self) -> None:
        """
        Validates that the on times can be variable
        """
        durations = [0.10, 0.15, 0.20, 0.25, 0.30]
        duration_idx = -1

        def next_duration() -> float:
            nonlocal durations, duration_idx
            duration_idx += 1
            return durations[duration_idx]

        on_events = []

        async def on_task():
            nonlocal on_events
            on_events.append(time.monotonic_ns())

        off_events = []

        async def off_task():
            nonlocal off_events
            off_events.append(time.monotonic_ns())

        finish_events = []

        async def finish_task():
            nonlocal finish_events
            finish_events.append(time.monotonic_ns())

        on_off_task = (
            new_one_time_on_off_task(5, next_duration, lambda: 0.1, on=on_task, off=off_task,
                                     finish=finish_task))

        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert len(on_events) == 5
        assert len(off_events) == 5
        assert len(finish_events) == 1

        # Validate that each on event is progressively bigger based on the passed in timing value.
        for idx in range(5):
            assert on_events[idx] < off_events[idx]
            assert (off_events[idx] - on_events[idx]) <= (durations[idx] * NANO * 1.1)
            assert (off_events[idx] - on_events[idx]) >= (durations[idx] * NANO * 0.9)

        # Validate that each off event is consistent.
        for idx in range(4):
            assert off_events[idx] < on_events[idx + 1]
            assert (on_events[idx + 1] - off_events[idx]) <= (0.1 * NANO * 1.1)
            assert (on_events[idx + 1] - off_events[idx]) >= (0.1 * NANO * 0.9)

        # Check that the finish event is after the last off event and within
        # a reasonable difference of +/- 10%
        assert off_events[4] < finish_events[0]
        assert (finish_events[0] - off_events[4]) <= (0.1 * NANO * 1.1)
        assert (finish_events[0] - off_events[4]) >= (0.1 * NANO * 0.9)

    def test_creates_events_with_variable_off_durations(self) -> None:
        """
        Validates that the on times can be variable
        """
        durations = [0.10, 0.15, 0.20, 0.25, 0.30]
        duration_idx = -1

        def next_duration() -> float:
            nonlocal duration_idx
            duration_idx += 1
            return durations[duration_idx]

        on_events = []

        async def on_task():
            nonlocal on_events
            on_events.append(time.monotonic_ns())

        off_events = []

        async def off_task():
            nonlocal off_events
            off_events.append(time.monotonic_ns())

        finish_events = []

        async def finish_task():
            nonlocal finish_events
            finish_events.append(time.monotonic_ns())

        on_off_task = (
            new_one_time_on_off_task(5, lambda: 0.1, next_duration, on=on_task, off=off_task,
                                     finish=finish_task))

        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert len(on_events) == 5
        assert len(off_events) == 5
        assert len(finish_events) == 1

        # Validate that each on event is consistent.
        for idx in range(5):
            assert on_events[idx] < off_events[idx]
            assert (off_events[idx] - on_events[idx]) <= (0.1 * NANO * 1.1)
            assert (off_events[idx] - on_events[idx]) >= (0.1 * NANO * 0.9)

        # Validate that each on event is progressively bigger based on the passed in timing value.
        for idx in range(4):
            assert off_events[idx] < on_events[idx + 1]
            assert (on_events[idx + 1] - off_events[idx]) <= (durations[idx] * NANO * 1.1)
            assert (on_events[idx + 1] - off_events[idx]) >= (durations[idx] * NANO * 0.9)

        # Check that the finish event is after the last off event and within
        # a reasonable difference of +/- 10%
        assert off_events[4] < finish_events[0]
        assert (finish_events[0] - off_events[4]) <= (durations[4] * NANO * 1.1)
        assert (finish_events[0] - off_events[4]) >= (durations[4] * NANO * 0.9)

    def test_only_works_once(self) -> None:
        """
        Validates that once used, the task does not work a second time,
        """
        on_called = 0

        async def on_task():
            nonlocal on_called
            on_called += 1

        off_called = 0

        async def off_task():
            nonlocal off_called
            off_called += 1

        finish_called = 0

        async def finish_task():
            nonlocal finish_called
            finish_called += 1

        # NOTE: The on and off duration intervals are much longer than the cancel polling intervals
        #       so we only expect the initial on event to be called.
        on_off_task = (
            new_one_time_on_off_task(5, lambda: 0.01, lambda: 0.01,
                                     on_task, off_task, finish_task))

        # Run the first time.
        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert on_called == 5
        assert off_called == 5
        assert finish_called == 1

        # Reset and run again, no events should be fired
        on_called = 0
        off_called = 0
        finish_called = 0

        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert on_called == 0
        assert off_called == 0
        assert finish_called == 0

    def test_when_only_on_event_provided(self) -> None:
        """
        Validates that only the on events get fired.
        """
        on_called = 0

        async def on_task():
            nonlocal on_called
            on_called += 1

        on_off_task = (
            new_one_time_on_off_task(5, lambda: 0.01, lambda: 0.01, on=on_task))

        # Run the first time.
        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert on_called == 5

    def test_when_only_off_event_provided(self) -> None:
        """
        Validates that only the off events get fired.
        """
        off_called = 0

        async def off_task():
            nonlocal off_called
            off_called += 1

        on_off_task = (
            new_one_time_on_off_task(5, lambda: 0.01, lambda: 0.01, off=off_task))

        # Run the first time.
        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert off_called == 5

    def test_when_only_finish_event_provided(self) -> None:
        """
        Validates that only the finish event get fired.
        """
        finish_called = 0

        async def finish_task():
            nonlocal finish_called
            finish_called += 1

        on_off_task = (
            new_one_time_on_off_task(5, lambda: 0.01, lambda: 0.01, finish=finish_task))

        # Run the first time.
        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert finish_called == 1

    def test_when_only_on_and_off_events_provided(self) -> None:
        """
        Validates that only the on and off events get fired.
        """
        on_called = 0

        async def on_task():
            nonlocal on_called
            on_called += 1

        off_called = 0

        async def off_task():
            nonlocal off_called
            off_called += 1

        on_off_task = (
            new_one_time_on_off_task(5, lambda: 0.01, lambda: 0.01, on=on_task, off=off_task))

        # Run the first time.
        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert on_called == 5
        assert off_called == 5

    def test_when_only_on_and_finish_events_provided(self) -> None:
        """
        Validates that only the on and finish events get fired.
        """
        on_called = 0

        async def on_task():
            nonlocal on_called
            on_called += 1

        finish_called = 0

        async def finish_task():
            nonlocal finish_called
            finish_called += 1

        on_off_task = (
            new_one_time_on_off_task(5, lambda: 0.01, lambda: 0.01, on=on_task, finish=finish_task))

        # Run the first time.
        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert on_called == 5
        assert finish_called == 1

    def test_when_off_and_finish_events_provided(self) -> None:
        """
        Validates that only the on and finish events get fired.
        """
        off_called = 0

        async def off_task():
            nonlocal off_called
            off_called += 1

        finish_called = 0

        async def finish_task():
            nonlocal finish_called
            finish_called += 1

        on_off_task = (
            new_one_time_on_off_task(5, lambda: 0.01, lambda: 0.01, off=off_task,
                                     finish=finish_task))

        # Run the first time.
        # noinspection PyTypeChecker
        asyncio.run(on_off_task())
        assert off_called == 5
        assert finish_called == 1
