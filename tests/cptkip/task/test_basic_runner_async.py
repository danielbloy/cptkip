import pytest

from cptkip.task.basic_runner_async import run


class TestBasicRunnerAsync:

    def test_run_with_no_tasks(self):
        """
        Calls run() but passes an empty list of functions. run() should return gracefully.
        """
        run([])

    def test_run_with_one_task(self):
        """
        Calls run() with a single task that terminates immediately having been called once.
        """
        one_count: int = 0

        async def one() -> None:
            nonlocal one_count
            one_count += 1

        run([one])

        assert one_count == 1

    def test_run_with_two_tasks(self):
        """
        Calls run() with two tasks that terminate immediately having been called once.
        """
        one_count: int = 0
        two_count: int = 0

        async def one() -> None:
            nonlocal one_count
            one_count += 1

        async def two() -> None:
            nonlocal two_count
            two_count += 1

        run([one, two])

        assert one_count == 1
        assert two_count == 1

    def test_run_with_task_that_throws_exception(self):
        """
        Calls run() with a task that throws an exception. This will propagate out as
        basic runner has no error handling.
        """

        async def raise_exception() -> None:
            raise Exception

        with pytest.raises(Exception):
            run([raise_exception])
