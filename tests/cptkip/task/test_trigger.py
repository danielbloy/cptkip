import cptkip.task.triggered_events_task as triggered_events_task
import cptkip.task.triggered_events_task_async as triggered_events_task_async
import cptkip.task.triggered_task as triggered_task
import cptkip.task.triggered_task_async as triggered_task_async
from cptkip.task.trigger import Trigger


class TestTrigger:

    def test_trigger_resets_once_read(self) -> None:
        trigger = Trigger(True)
        assert trigger()
        assert not trigger()

        trigger.triggered = True
        assert trigger()
        assert not trigger()

        assert not Trigger(False)()

    def test_trigger_is_shared_by_all_triggered_tasks(self) -> None:
        """
        A single Trigger class is used (and re-exported) by all the triggered task
        modules, so existing imports keep working without duplicate classes.
        """
        assert triggered_task.Trigger is Trigger
        assert triggered_task_async.Trigger is Trigger
        assert triggered_events_task.Trigger is Trigger
        assert triggered_events_task_async.Trigger is Trigger
