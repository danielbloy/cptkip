import pytest

from cptkip.task.basic_runner import run


class TestBasicRunner:

    # TODO: Write tests to validate interleaving tasks run as expected.

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

        def one() -> bool:
            nonlocal one_count
            one_count += 1
            return False

        run([one])

        assert one_count == 1

    def test_run_with_two_tasks(self):
        """
        Calls run() with two tasks that terminate immediately having been called once.
        """
        one_count: int = 0
        two_count: int = 0

        def one() -> bool:
            nonlocal one_count
            one_count += 1
            return False

        def two() -> bool:
            nonlocal two_count
            two_count += 1
            return False

        run([one, two])

        assert one_count == 1
        assert two_count == 1

    def test_run_with_three_tasks(self):
        """
        Runs three tasks, each of which completes at a different point in time.
        """
        one_count: int = 0
        two_count: int = 0
        three_count: int = 0

        def one() -> bool:
            nonlocal one_count
            one_count += 1
            return one_count < 11

        def two() -> bool:
            nonlocal two_count
            two_count += 1
            return two_count < 22

        def three() -> bool:
            nonlocal three_count
            three_count += 1
            return three_count < 33

        run([three, one, two])

        assert one_count == 11
        assert two_count == 22
        assert three_count == 33

    def test_run_with_task_that_throws_exception(self):
        """
        Calls run() with a task that throws an exception. This will propagate out as
        basic runner has no error handling.
        """

        def raise_exception() -> bool:
            raise Exception

        with pytest.raises(Exception):
            run([raise_exception])
