from time import monotonic


class TriggerTimedEvents:
    """
    This class is used to trigger events that need to happen at specified times after the
    trigger is started. There is no way to pause a TriggerTimedEvents once it is triggered,
    though it can be stopped/reset.

    Events that are triggered are returned by the run() function. This does a simple check
    to see how much time has elapsed since the trigger was started and return all Events
    that have elapsed. Events are only triggered once during a "run" of the tigger.

    Multiple different events can be added for the same time and will all be fired; though
    the order those events are returned from run() is not guaranteed.

    A TriggerTimedEvents can be used in conjunction with a new_triggered_task() to generate
    the events based on an initial trigger event.
    """

    class Event:
        def __init__(self, trigger_time: float, event: int):
            self.trigger_time = trigger_time
            self.event = event

    def __init__(self):
        self.__running = False
        self.__start_time = 0
        self.__events_remaining = None
        self.events = []

    def start(self):
        """
        Starts the trigger which will result in the timed events being
        returned by the run() method. This method is safe to call
        multiple times when running and will not affect the triggered
        events whilst running.
        """
        if self.__running:
            return

        self.__start_time = monotonic()
        self.__running = True
        self.__events_remaining = self.events.copy()

    def stop(self):
        """
        Stops the trigger if it is running. This will cancel any events that
        were queued up ready to be triggered. As with start(), this method
        is safe to call multiple times when running.
        """
        if not self.__running:
            return

        self.__start_time = 0
        self.__running = False
        del self.__events_remaining

    def reset(self):
        """
        Simply calls stop().
        """
        self.stop()

    @property
    def running(self):
        """
        Returns whether this trigger is running or not.
        """
        return self.__running

    def run(self) -> [Event]:
        """
        Runs the trigger and returns a list of the events that have "fired" since the
        last time run() is called. If the trigger is not running then an empty list
        is returned. If the number of triggerable events has been exhausted then the
        trigger will be automatically stopped.
        """
        if not self.running:
            return []

        # If all events have been exhausted then stop running
        if self.__events_remaining is None or len(self.__events_remaining) <= 0:
            self.stop()
            return []

        # Get all items that need to be fired.
        now = monotonic()
        diff = now - self.__start_time
        events_to_fire = [event for event in self.__events_remaining if diff >= event.trigger_time]

        # Remove those that have been fired
        for event in events_to_fire:
            self.__events_remaining.remove(event)

        if len(self.__events_remaining) <= 0:
            self.stop()

        return events_to_fire

    def add_event(self, trigger_time: float, event: int):
        """
        Adds an event that is to be triggered at the specified number of seconds
        after the trigger has started. Multiple events can be setup for the same
        trigger time and multiple events can use the same event identifier.

        :param trigger_time: The time in second after the trigger is started that
                             the event is desired to be triggered. Multiple events
                             can be added for the same time value and all will get
                             fired.
        :param event:        An integer identifier for the event. This does not
                             need to be unique.
        """
        self.events.append(self.Event(trigger_time, event))
