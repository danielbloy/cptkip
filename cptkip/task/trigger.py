class Trigger:
    """
    A simple trigger that automatically resets once read. Use it as the trigger
    function for triggered_task, triggered_task_async, triggered_events_task and
    triggered_events_task_async: set triggered to True to fire the trigger once.
    """
    triggered: bool

    def __init__(self, triggered: bool) -> None:
        self.triggered = triggered

    def __call__(self) -> bool:
        result = self.triggered
        self.triggered = False
        return result
