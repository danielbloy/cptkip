class Triggerable:
    """Trivial implementation for a triggerable object."""

    def __init__(self):
        self.triggered = False


class TriggerableAlwaysOn:
    """Trivial implementation for a triggerable object that is always triggered."""

    @property
    def triggered(self):
        return True

    @triggered.setter
    def triggered(self, value):
        pass
